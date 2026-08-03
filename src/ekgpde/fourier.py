import numpy as np

from ekgpde import parameters
from ekgpde.derivative import derivative

def fourier_least_squares_info(
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

    returns u_hat_derivs, w, f_hat_vals

    F = foriertransform:
    f_hat_vals = [F(1), F(t)...]

    """
    degree_diff_eqn = parameters.degree_of_differential_equation + 1
    u_derivs = np.zeros((degree_diff_eqn, len(time_series)))
    u_hat_derivs = np.zeros((degree_diff_eqn, len(time_series)//2 + 1), dtype=complex)
    for i in range(len(u_derivs)):
        for a in range(len(time_series)):
            if (a > len(time_series)-i-1):
                            u_derivs[i][a] = deriv_order_i = derivative(time_series, len(time_series)-i-1, i, 1/sample_rate)
            else:
                deriv_order_i = derivative(time_series, a, i, 1/sample_rate)
                u_derivs[i][a] = deriv_order_i
             
        
        
        u_hat_derivs[i] = np.fft.rfft(u_derivs[i])

    lenght_forier_coeficient = len(u_hat_derivs[0])
    polynomal_transform_vals = np.zeros(( polynomal_degree_right + 1, lenght_forier_coeficient), dtype=complex,)

    for i in range (polynomal_degree_right + 1):
        polynomal_transform_vals[i] = np.fft.rfft(t_vals**i)




    return u_hat_derivs, 2*np.pi*np.fft.rfftfreq(len(time_series), 1/sample_rate), polynomal_transform_vals
