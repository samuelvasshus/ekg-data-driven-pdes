#Kode for å hente data inn generert av Chat-gpt

from pathlib import Path

import numpy as np
import wfdb


# =========================
# Settings you can change
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

OUTPUT_PATH = Path("data/processed/nsrdb_18_records_10s.npz")


def load_ecg_segment(
    record_name: str,
    database_name: str,
    start_second: float,
    duration_seconds: float,
    lead_index: int = 0,
) -> tuple[np.ndarray, np.ndarray, float]:
    """
    Load one ECG segment from a PhysioNet/WFDB database.

    Parameters
    ----------
    record_name:
        Name of the ECG record to load.
    database_name:
        Name of the PhysioNet database, for example ``"nsrdb"``.
    start_second:
        Start time of the segment in seconds.
    duration_seconds:
        Duration of the segment in seconds.
    lead_index:
        Index of the ECG lead to load.

    Returns
    -------
    time:
        One-dimensional array containing time values in seconds.
    signal:
        One-dimensional array containing ECG signal values.
    sampling_rate:
        Sampling rate of the signal in Hz.

    Raises
    ------
    ValueError
        If the selected lead index is not available for the record.
    """
    header = wfdb.rdheader(record_name, pn_dir=database_name)
    sampling_rate = float(header.fs)

    start_sample = int(start_second * sampling_rate)
    end_sample = int((start_second + duration_seconds) * sampling_rate)

    record = wfdb.rdrecord(
        record_name,
        pn_dir=database_name,
        sampfrom=start_sample,
        sampto=end_sample,
    )

    if lead_index >= record.p_signal.shape[1]:
        raise ValueError(
            f"lead_index={lead_index} is not available for record {record_name}. "
            f"This record has {record.p_signal.shape[1]} leads."
        )

    signal = record.p_signal[:, lead_index]
    time = np.arange(len(signal)) / sampling_rate + start_second

    return time, signal, sampling_rate


def load_all_ecg_segments(
    record_names: list[str],
    database_name: str,
    start_second: float,
    duration_seconds: float,
    lead_index: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """
    Load ECG segments from several records into one NumPy array.

    Parameters
    ----------
    record_names:
        List of ECG record names.
    database_name:
        Name of the PhysioNet database.
    start_second:
        Start time of each segment in seconds.
    duration_seconds:
        Duration of each segment in seconds.
    lead_index:
        Index of the ECG lead to load.

    Returns
    -------
    ecg_signals:
        Two-dimensional array with shape ``(n_records, n_samples)``.
        Each row corresponds to one ECG time series.
    time:
        One-dimensional array containing the time values in seconds.
    record_names_array:
        One-dimensional array containing the record names in the same order
        as the rows of ``ecg_signals``.
    sampling_rate:
        Sampling rate of the ECG signals in Hz.

    Notes
    -----
    This function assumes that all records have the same sampling rate and
    that the extracted segments have the same number of samples.
    """
    signals = []
    time = None
    sampling_rate = None

    for record_name in record_names:
        current_time, signal, current_sampling_rate = load_ecg_segment(
            record_name=record_name,
            database_name=database_name,
            start_second=start_second,
            duration_seconds=duration_seconds,
            lead_index=lead_index,
        )

        if time is None:
            time = current_time
            sampling_rate = current_sampling_rate

        signals.append(signal)

        print(
            f"Loaded record {record_name}: "
            f"{len(signal)} samples, "
            f"{current_sampling_rate:.1f} Hz"
        )

    ecg_signals = np.asarray(signals)
    record_names_array = np.asarray(record_names)

    return ecg_signals, time, record_names_array, sampling_rate


def save_ecg_dataset(
    output_path: Path,
    ecg_signals: np.ndarray,
    time: np.ndarray,
    record_names: np.ndarray,
    sampling_rate: float,
    start_second: float,
    duration_seconds: float,
) -> None:
    """
    Save the imported ECG dataset as a compressed NumPy file.

    Parameters
    ----------
    output_path:
        Path where the dataset should be saved.
    ecg_signals:
        Two-dimensional array with shape ``(n_records, n_samples)``.
    time:
        One-dimensional array containing time values in seconds.
    record_names:
        One-dimensional array containing record names.
    sampling_rate:
        Sampling rate in Hz.
    start_second:
        Start time of the extracted interval in seconds.
    duration_seconds:
        Duration of the extracted interval in seconds.

    Returns
    -------
    None
        The dataset is saved to disk.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    np.savez_compressed(
        output_path,
        ecg_signals=ecg_signals,
        time=time,
        record_names=record_names,
        sampling_rate=sampling_rate,
        start_second=start_second,
        duration_seconds=duration_seconds,
    )

    print(f"\nSaved dataset to: {output_path}")


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
        start_second=START_SECOND,
        duration_seconds=DURATION_SECONDS,
    )


if __name__ == "__main__":
    main()