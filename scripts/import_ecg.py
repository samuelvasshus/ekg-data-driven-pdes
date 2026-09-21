"""Download the configured ECG segments from PhysioNet."""

from pathlib import Path

from ekgpde.data import load_all_ecg_segments, save_ecg_dataset

# =========================
# Adjustable parameters
# =========================

DATABASE_NAME = "nsrdb"

RECORD_NAMES = [
    "16265",
    "16272",
    "16273",
    "16420",
    "16483",
    "16539",
    "16773",
    "16786",
    "16795",
    "17052",
    "17453",
    "18177",
    "18184",
    "19088",
    "19090",
    "19093",
    "19140",
    "19830",
]

START_SECOND = 60.0
DURATION_SECONDS = 20.0
LEAD_INDEX = 0

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / f"nsrdb_{len(RECORD_NAMES)}_records_{DURATION_SECONDS:g}s.npz"
)


def main() -> None:
    """
    Import 18 ECG time series and save them as one NumPy array.

    The resulting array has shape ``(18, n_samples)``, where each row is one
    ECG time series from one record.
    """
    ecg_signals, time, record_names, sampling_rate = load_all_ecg_segments(
        record_names=RECORD_NAMES,
        database_name=DATABASE_NAME,
        start_second=START_SECOND,
        duration_seconds=DURATION_SECONDS,
        lead_index=LEAD_INDEX,
    )

    print("\nFinal array information:")
    print(f"ecg_signals.shape = {ecg_signals.shape}")
    print(f"time.shape = {time.shape}")
    print(f"Number of records = {len(record_names)}")
    print(f"Sampling rate = {sampling_rate:.1f} Hz")

    save_ecg_dataset(
        output_path=OUTPUT_PATH,
        ecg_signals=ecg_signals,
        time=time,
        record_names=record_names,
        sampling_rate=sampling_rate,
        database_name=DATABASE_NAME,
        lead_index=LEAD_INDEX,
        start_second=START_SECOND,
        duration_seconds=DURATION_SECONDS,
    )


if __name__ == "__main__":
    main()
