"""Download ECG segments from PhysioNet and save them locally."""

from pathlib import Path

import numpy as np
import numpy.typing as npt
import wfdb


def load_ecg_segment(
    record_name: str,
    database_name: str,
    start_second: float,
    duration_seconds: float,
    lead_index: int = 0,
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64], float]:
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
        If required signal metadata is missing or the selected lead is not
        available for the record.
    """
    if start_second < 0:
        raise ValueError("start_second must be non-negative")
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")
    if lead_index < 0:
        raise ValueError("lead_index must be non-negative")

    header = wfdb.rdheader(record_name, pn_dir=database_name)
    header_sampling_rate = header.fs
    if header_sampling_rate is None:
        raise ValueError(
            f"No sampling rate was found for record {record_name}."
        )
    sampling_rate = float(header_sampling_rate)

    start_sample = int(start_second * sampling_rate)
    end_sample = int((start_second + duration_seconds) * sampling_rate)

    record = wfdb.rdrecord(
        record_name,
        pn_dir=database_name,
        sampfrom=start_sample,
        sampto=end_sample,
    )

    if isinstance(record, wfdb.MultiRecord):
        record = record.multi_to_single(physical=True)

    signal_data = record.p_signal
    if signal_data is None:
        raise ValueError(
            f"No physical signal data was returned for record {record_name}."
        )

    if not 0 <= lead_index < signal_data.shape[1]:
        raise ValueError(
            f"lead_index={lead_index} is not available for record {record_name}. "
            f"This record has {signal_data.shape[1]} leads."
        )

    signal = np.asarray(signal_data[:, lead_index], dtype=np.float64)
    time = np.arange(len(signal), dtype=np.float64) / sampling_rate + start_second

    return time, signal, sampling_rate


def load_all_ecg_segments(
    record_names: list[str],
    database_name: str,
    start_second: float,
    duration_seconds: float,
    lead_index: int = 0,
) -> tuple[
    npt.NDArray[np.float64],
    npt.NDArray[np.float64],
    npt.NDArray[np.str_],
    float,
]:
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
    if not record_names:
        raise ValueError("record_names must contain at least one record")

    time, first_signal, sampling_rate = load_ecg_segment(
        record_name=record_names[0],
        database_name=database_name,
        start_second=start_second,
        duration_seconds=duration_seconds,
        lead_index=lead_index,
    )
    signals = [first_signal]

    print(
        f"Loaded record {record_names[0]}: "
        f"{len(first_signal)} samples, "
        f"{sampling_rate:.1f} Hz"
    )

    for record_name in record_names[1:]:
        current_time, signal, current_sampling_rate = load_ecg_segment(
            record_name=record_name,
            database_name=database_name,
            start_second=start_second,
            duration_seconds=duration_seconds,
            lead_index=lead_index,
        )

        if not np.isclose(current_sampling_rate, sampling_rate):
            raise ValueError(
                f"Record {record_name} has sampling rate "
                f"{current_sampling_rate}, expected {sampling_rate}."
            )
        if signal.shape != first_signal.shape:
            raise ValueError(
                f"Record {record_name} has {len(signal)} samples, "
                f"expected {len(first_signal)}."
            )
        if not np.array_equal(current_time, time):
            raise ValueError(
                f"Record {record_name} has time values that differ from the "
                "first record."
            )

        signals.append(signal)

        print(
            f"Loaded record {record_name}: "
            f"{len(signal)} samples, "
            f"{current_sampling_rate:.1f} Hz"
        )

    ecg_signals = np.stack(signals)
    record_names_array = np.asarray(record_names, dtype=np.str_)

    return ecg_signals, time, record_names_array, sampling_rate


def save_ecg_dataset(
    output_path: Path,
    ecg_signals: npt.NDArray[np.float64],
    time: npt.NDArray[np.float64],
    record_names: npt.NDArray[np.str_],
    sampling_rate: float,
    database_name: str,
    lead_index: int,
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
    database_name:
        Name of the source PhysioNet database.
    lead_index:
        Index of the selected ECG lead.
    start_second:
        Start time of the extracted interval in seconds.
    duration_seconds:
        Duration of the extracted interval in seconds.

    Returns
    -------
    None
        The dataset is saved to disk.
    """
    if ecg_signals.ndim != 2:
        raise ValueError("ecg_signals must be a two-dimensional array")
    if time.ndim != 1:
        raise ValueError("time must be a one-dimensional array")
    if record_names.ndim != 1:
        raise ValueError("record_names must be a one-dimensional array")
    if ecg_signals.shape[0] != len(record_names):
        raise ValueError("record_names must contain one name per ECG signal")
    if ecg_signals.shape[1] != len(time):
        raise ValueError("time must contain one value per ECG sample")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    np.savez_compressed(
        output_path,
        ecg_signals=ecg_signals,
        time=time,
        record_names=record_names,
        sampling_rate=sampling_rate,
        database_name=database_name,
        lead_index=lead_index,
        start_second=start_second,
        duration_seconds=duration_seconds,
    )

    print(f"\nSaved dataset to: {output_path}")


def load_ecg_dataset(
    input_path: Path,
) -> tuple[
    npt.NDArray[np.float64],
    npt.NDArray[np.float64],
    npt.NDArray[np.str_],
    float,
]:
    """Load and validate the arrays required by the modelling pipeline."""
    required_fields = {"ecg_signals", "time", "record_names", "sampling_rate"}

    with np.load(input_path) as data:
        missing_fields = required_fields.difference(data.files)
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"Dataset is missing required fields: {missing}")

        ecg_signals = np.asarray(data["ecg_signals"], dtype=np.float64)
        time = np.asarray(data["time"], dtype=np.float64)
        record_names = np.asarray(data["record_names"], dtype=np.str_)
        sampling_rate = float(data["sampling_rate"].item())

    if ecg_signals.ndim != 2:
        raise ValueError("Stored ecg_signals must be a two-dimensional array")
    if time.ndim != 1 or ecg_signals.shape[1] != len(time):
        raise ValueError("Stored time values do not match the ECG samples")
    if record_names.ndim != 1 or ecg_signals.shape[0] != len(record_names):
        raise ValueError("Stored record names do not match the ECG signals")

    return ecg_signals, time, record_names, sampling_rate
