import numpy as np
import numpy.typing as npt

def gaussian_smooth(
        time_series: npt.NDArray[np.float64],
        sigma: float,
        half_width: int,
    )->np.ndarray:
    """Smooth a 1D signal by convolving it with a truncated, normalized Gaussian kernel.

    Each output sample is a weighted average of the input sample and its
    `half_width` neighbours on each side, with weights exp(-k^2 / (2 sigma^2)).
    This acts as a low-pass filter, damping high-frequency noise before
    differentiation.

    Args:
        time_series (npt.NDArray[np.float64]): Signal to smooth.
        sigma (float): Width of the Gaussian, in samples (not seconds). Must be > 0.
        half_width (int):  Smoothed signal, same length as `time_series`. Boundaries are
        handled by repeating the edge values, so the first and last
        `half_width` samples are less reliable.

    Returns:
        np.ndarray: _description_
    """
    time_series = np.asarray(time_series, dtype=np.float64)
    if time_series.ndim != 1:
        raise ValueError(f"time_series must be 1D, got shape {time_series.shape}")
    if sigma <= 0:
        raise ValueError(f"sigma must be positive, got {sigma}")
    if half_width < 0:
        raise ValueError(f"half_width must be non-negative, got {half_width}")

    offsets = np.arange(-half_width, half_width + 1, dtype=np.float64)

    weights = np.exp(-0.5 * (offsets / sigma) ** 2) #Gaussian symmetric, property preserved
    weights = weights/weights.sum() #Scales sum to 1, property preserved
    
    time_series_padded = np.pad(time_series, pad_width = half_width, mode="edge") 
    time_series_smoothed = np.zeros(len(time_series_padded))
    
    for i in range (len(time_series)):
        sliced = time_series_padded[i:i+2*half_width+1]
        time_series_smoothed[i + half_width] = np.dot(sliced, weights)

    time_series_smoothed = time_series_smoothed[half_width:(len(time_series_smoothed)-half_width)]

    return time_series_smoothed
