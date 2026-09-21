# Data

This project uses ECG recordings from the
[MIT-BIH Normal Sinus Rhythm Database](https://physionet.org/content/nsrdb/1.0.0/),
version 1.0.0, hosted by PhysioNet.

## Directory structure


- `raw/`: Original downloaded data, kept unchanged.
- `interim/`: Extracted ECG segments produced from the source database.
- `processed/`: Filtered, normalized, or otherwise model-ready datasets.

## Creating the dataset

From the repository root, run:

```bash
python3 scripts/import_ecg.py
```
