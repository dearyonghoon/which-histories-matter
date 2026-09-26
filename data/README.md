# Data

This package does not redistribute benchmark datasets.

The aligned long-horizon experiments use six public datasets:

- ETTh1
- Weather
- Electricity
- Traffic
- Exchange
- Solar

Place them under `data/` using the following layout, or set `PRR_DATA_ROOT` to a directory with the same structure.

```text
data/
├── ETT-small/ETTh1.csv
├── weather/weather.csv
├── electricity/electricity.csv
├── traffic/traffic.csv
├── exchange_rate/exchange_rate.csv
└── Solar/solar_AL.txt
```

The final aligned protocol uses retrieval lookback 96, a common memory-window stride of 8 for Pearson / PRR-Stat / full PRR, and horizons `{96, 192, 336, 720}`. Frozen evaluation anchors require at least 512 preceding observations. ETTh1 uses the fixed chronological boundaries `train_end=8640`, `val_end=11520`, and `test_end=len(data)=17420`, leaving 5,900 observations in the test region. The other datasets use chronological 70/10/20 splits. All channel normalization statistics are fitted on the training period only.
