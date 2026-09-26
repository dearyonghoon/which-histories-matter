"""Reference PRR architecture, feature, target, and trust-calibration helpers.

This module mirrors the inference-critical architecture used by the final PRR
checkpoints and the equations in the paper.  Large training/evaluation pipelines
remain in experiments/prr_long_horizon/.
"""
from __future__ import annotations
import math
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

EPS = 1e-8
RETRIEVAL_SEQ_LEN = 96
EMB_DIM = 64
ENC_HIDDEN = 128
RERANK_HIDDEN = 384
RERANK_DROPOUT = 0.1
FEATURE_CLIP = 8.0


def centered_pattern(x: np.ndarray) -> np.ndarray:
    """Centered cosine representation; for univariate windows this induces Pearson ranking."""
    x = np.asarray(x, np.float32)
    xc = x - x.mean(axis=-1, keepdims=True)
    n = np.linalg.norm(xc, axis=-1, keepdims=True)
    return np.where(n > EPS, xc / np.maximum(n, EPS), 0.0).astype(np.float32)


def context7(x: np.ndarray) -> np.ndarray:
    """Seven past-only statistics used by PRR-Stat and retained in full PRR."""
    x = np.asarray(x, np.float32)
    short = max(8, x.shape[-1] // 4)
    m = x.mean(axis=-1)
    s = x.std(axis=-1) + EPS
    f1 = (x[..., -1] - m) / s
    f2 = (x[..., -short:].mean(axis=-1) - m) / s
    f3 = (x[..., -1] - x[..., -short]) / s
    f4 = (x[..., -1] - x[..., 0]) / s
    df = np.diff(x, axis=-1)
    ds = np.diff(x[..., -short:], axis=-1)
    f5 = (ds.std(axis=-1) + EPS) / (df.std(axis=-1) + EPS)
    t = np.linspace(-1.0, 1.0, x.shape[-1], dtype=np.float32)
    t = t - t.mean()
    f6 = (np.sum(t * (x - m[..., None]), axis=-1) / (np.sum(t*t) + EPS)) / s
    a, b = x[..., :-1], x[..., 1:]
    a = a - a.mean(axis=-1, keepdims=True)
    b = b - b.mean(axis=-1, keepdims=True)
    f7 = np.sum(a*b, axis=-1) / (np.sqrt(np.sum(a*a, axis=-1) * np.sum(b*b, axis=-1)) + EPS)
    return np.stack([f1,f2,f3,f4,f5,f6,f7], axis=-1).astype(np.float32)


class TemporalEncoder1D(nn.Module):
    def __init__(self, hidden: int = ENC_HIDDEN, emb_dim: int = EMB_DIM):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(1, hidden//2, 5, stride=2, padding=2), nn.GELU(),
            nn.Conv1d(hidden//2, hidden, 5, stride=2, padding=2), nn.GELU(),
            nn.Conv1d(hidden, hidden, 3, stride=2, padding=1), nn.GELU(),
            nn.AdaptiveAvgPool1d(1),
        )
        self.proj = nn.Linear(hidden, emb_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.ndim == 2:
            x = x[:, None, :]
        h = self.net(x).squeeze(-1)
        return F.normalize(self.proj(h), dim=-1)


def _inverse_softplus(x: float) -> float:
    return math.log(math.exp(float(x)) - 1.0)


class WideFusionReranker(nn.Module):
    """285-D fusion residual reranker used by final PRR checkpoints."""
    def __init__(self, emb_dim: int = EMB_DIM, hidden: int = RERANK_HIDDEN, dropout: float = RERANK_DROPOUT):
        super().__init__()
        in_dim = 1 + 4 * (7 + emb_dim)  # 285 when emb_dim=64
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.LayerNorm(hidden), nn.GELU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden), nn.LayerNorm(hidden), nn.GELU(), nn.Dropout(dropout),
            nn.Linear(hidden, 1),
        )
        self.raw_alpha = nn.Parameter(torch.tensor(_inverse_softplus(0.1), dtype=torch.float32))

    def forward(self, feat: torch.Tensor, base: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        delta = self.net(feat).squeeze(-1)
        score = base + F.softplus(self.raw_alpha) * delta
        return score.masked_fill(~mask, -1e9)


def soft_future_target(distance: np.ndarray, tau: float = 0.5) -> np.ndarray:
    """Query-wise standardized future-distance target used for listwise supervision."""
    d = np.asarray(distance, np.float32)
    mu = d.mean(axis=-1, keepdims=True)
    sd = np.maximum(d.std(axis=-1, keepdims=True), 1e-6)
    z = (d - mu) / sd
    logits = -z / float(tau)
    logits = logits - logits.max(axis=-1, keepdims=True)
    p = np.exp(logits)
    return (p / np.maximum(p.sum(axis=-1, keepdims=True), 1e-12)).astype(np.float32)


def interpolate_direct_prr(direct: np.ndarray, retrieval: np.ndarray, beta: float) -> np.ndarray:
    return np.asarray(direct) + float(beta) * (np.asarray(retrieval) - np.asarray(direct))


def select_validation_beta(direct: np.ndarray, retrieval: np.ndarray, truth: np.ndarray,
                           grid=(0.0,0.025,0.05,0.075,0.10,0.15,0.20)) -> float:
    """Select condition-specific trust on validation only; smallest beta breaks exact ties."""
    vals = []
    for beta in grid:
        pred = interpolate_direct_prr(direct, retrieval, beta)
        vals.append((float(np.mean((pred-truth)**2)), float(beta)))
    vals.sort(key=lambda x: (x[0], x[1]))
    return vals[0][1]
