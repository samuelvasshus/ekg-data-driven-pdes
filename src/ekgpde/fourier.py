import numpy as np


def forier_least_square_info(
    time_series: np.ndarray,
    sample_rate: float = 128.0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute forier coefficients and correspnding angular frequencies
    Real signal, therefore rfft and rfftfreq with same length.
    Takes care of nyquist frequency. 

    """
    return np.fft.rfft(time_series), 2*np.pi*np.fft.rfftfreq(len(time_series), 1/sample_rate)
