#!/usr/bin/env python3
"""Audit tracked files for public-release hygiene."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOWNSTREAM = ROOT / "experiments" / "downstream"
EXPECTED_DOWNSTREAM_NOTEBOOKS = 41

FORBIDDEN = {
    "Hangul text": re.compile(r"[\uac00-\ud7a3]"),
    "AI-conversation marker": re.compile(
        r"ChatGPT|OpenAI|AI assistant|prompt from|conversation with",
        re.IGNORECASE,
    ),
    "internal drafting marker": re.compile(
        r"reviewer-facing|paper-grade|paper-ready|submitted paper|next experiment|"
        r"strong result would be|internal note",
        re.IGNORECASE,
    ),
    "user-specific local path": re.compile(r"/home/[^/]+/|/Users/[^/]+/"),
}


def tracked_files() -> list[Path]:
    output = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT
    ).decode("utf-8")
    return [ROOT / item for item in output.split("\0") if item]


def main() -> int:
    failures: list[str] = []
    notebooks = sorted(DOWNSTREAM.glob("*.ipynb"))
    if len(notebooks) != EXPECTED_DOWNSTREAM_NOTEBOOKS:
        failures.append(
            f"expected {EXPECTED_DOWNSTREAM_NOTEBOOKS} downstream notebooks, "
            f"found {len(notebooks)}"
        )

    for path in tracked_files():
        # This file necessarily contains the marker patterns it audits.
        if path.resolve() == Path(__file__).resolve():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue

        relative = path.relative_to(ROOT)
        for label, pattern in FORBIDDEN.items():
            if pattern.search(text):
                failures.append(f"{relative}: {label}")

        if path.suffix == ".ipynb":
            try:
                notebook = json.loads(text)
            except json.JSONDecodeError as error:
                failures.append(f"{relative}: invalid notebook JSON ({error})")
                continue
            if path.parent == DOWNSTREAM:
                for index, cell in enumerate(notebook.get("cells", [])):
                    if cell.get("outputs"):
                        failures.append(f"{relative}: saved output in cell {index}")
                    if cell.get("execution_count") is not None:
                        failures.append(
                            f"{relative}: execution count in cell {index}"
                        )

    if failures:
        print("FAIL public-release audit")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS public-release audit")
    print(f"- downstream notebooks: {len(notebooks)}")
    print("- forbidden text markers: 0")
    print("- saved downstream outputs: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
