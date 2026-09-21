import numpy as np
import numpy.typing as npt
from ekgpde.differentiation import differentiate

def polynomial_transforms(
    t_vals: npt.NDArray[np.float64],
    degree: int,
) -> npt.NDArray[np.complex128]:
    """Fourier transform of the right-hand side terms 1, t, t^2, ..., t^degree.

    Returns:
        Array of shape (degree + 1, len(t_vals)//2 + 1): [F(1), F(t), ...].
    """
    return np.array([np.fft.rfft(t_vals**k) for k in range(degree + 1)])

#periodic assumption
def spectral_derivatives(
    time_series: npt.NDArray[np.float64],
    t_vals: npt.NDArray[np.float64],
    order: int,
    polynomial_degree: int,
) -> tuple[npt.NDArray[np.complex128], npt.NDArray[np.float64], npt.NDArray[np.complex128]]:
    """Fourier transforms of u, u', ..., u^(order) using the rule F(u^(n)) = (iω)^n F(u).

    Args:
        time_series: Uniformly sampled signal u.
        t_vals: Sample times, same length as time_series.
        order: Highest derivative order.
        polynomial_degree: Degree of the right-hand side polynomial.

    Returns:
        u_hat_derivs: Shape (order + 1, N//2 + 1), rows F(u), F(u'), ...
        omegas: Angular frequencies ω, in rad/s.
        polynomial_hats: Shape (polynomial_degree + 1, N//2 + 1), rows F(1), F(t), ...
    """
    dt = t_vals[1] - t_vals[0]
    u_hat = np.fft.rfft(time_series)
    
    omegas = 2*np.pi*np.fft.rfftfreq(len(time_series), dt)
    u_hat_derivs = np.array([(1j*omegas)**n * u_hat for n in range(order + 1)])
    
    return u_hat_derivs, omegas, polynomial_transforms(t_vals, polynomial_degree)

#non-periodic requirement
def finite_difference_derivatives(
    time_series: npt.NDArray[np.float64],
    t_vals: npt.NDArray[np.float64],
    order: int,
    polynomial_degree: int,
) -> tuple[npt.NDArray[np.complex128], npt.NDArray[np.float64], npt.NDArray[np.complex128]]:
    """Fourier transforms of u, u', ..., u^(order), with derivatives computed by
    central finite differences in time before transforming.
    
    Args:
        time_series: Uniformly sampled signal u.
        t_vals: Sample times, same length as time_series.
        order: Highest derivative order.
        polynomial_degree: Degree of the right-hand side polynomial.

    Returns:
        u_hat_derivs: Shape (order + 1, N//2 + 1), rows F(u), F(u'), ...
        omegas: Angular frequencies ω, in rad/s.
        polynomial_hats: Shape (polynomial_degree + 1, N//2 + 1), rows F(1), F(t), ...
    """
    dt = t_vals[1] - t_vals[0]
    u_derivs = np.array([
        [differentiate(time_series, i, n, dt) for i in range(len(time_series))]
        for n in range(order + 1)
    ])
    u_hat_derivs = np.fft.rfft(u_derivs, axis=1)
    omegas = 2*np.pi*np.fft.rfftfreq(len(time_series), dt)
    return u_hat_derivs, omegas, polynomial_transforms(t_vals, polynomial_degree)