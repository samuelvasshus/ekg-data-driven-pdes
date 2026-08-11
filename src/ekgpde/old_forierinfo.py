import numpy as np

def old_fourier_least_squares_info(
    time_series: np.ndarray,
    t_vals: np.ndarray,
    polynomal_degree_right: int,
    sample_rate: float = 128.0,
    

) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute forier coefficients and correspnding angular frequencies
    Real signal, therefore rfft and rfftfreq with same length.
    Takes care of nyquist frequency.
    also returns array of foriertransform of a_n*t^n foriercoeficients of polynomal on right side

    returns u_hat, w, f_hat_vals

    F = foriertransform:
    f_hat_vals = [F(1), F(t)...]

    """
    u_hat = np.fft.rfft(time_series)
    lenght_forier_coeficient = len(u_hat)
    polynomal_transform_vals = np.zeros(( polynomal_degree_right + 1, lenght_forier_coeficient), dtype=complex,)

    for i in range (polynomal_degree_right + 1):
        polynomal_transform_vals[i] = np.fft.rfft(t_vals**i)




    return u_hat, 2*np.pi*np.fft.rfftfreq(len(time_series), 1/sample_rate), polynomal_transform_vals