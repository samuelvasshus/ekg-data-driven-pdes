import numpy as np
import numpy.typing as npt


def build_linear_system(
    u_hat_derivs: npt.NDArray[np.complex128],
    polynomial_hats: npt.NDArray[np.complex128],
    polynomial_degree: int,
    fixed_column: int,
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Build the real least-squares system A x = b for the ODE coefficients.

    Args:
        u_hat_derivs: Rows F(u), F(u'), ..., from spectral.py.
        polynomial_hats: Rows F(1), F(t), ..., from spectral.py.
        polynomial_degree: Degree of the right-hand side polynomial.
        fixed_column: Index, in the column order above, of the coefficient fixed to 1.

    Returns:
        A_real: Real matrix, 2 * (number of frequencies) rows, one column per
            free coefficient.
        b_real: Real right-hand side.
    """
    number_of_terms = polynomial_degree + 1 + len(u_hat_derivs)
    number_of_frequencies = len(u_hat_derivs[0])
    A = np.zeros((number_of_terms, number_of_frequencies), dtype = np.complex128)

    for k in range(polynomial_degree + 1):
        A[k, :] = polynomial_hats[k]

    for n in range(len(u_hat_derivs)):
        A[polynomial_degree + 1 + n, :] = u_hat_derivs[n]

    A = np.transpose(A)  # one row per frequency, one column per term

    A_real = np.vstack([A.real, A.imag]) # divide complex and real system

    #fix final coef to 1 and move to rhs side of equation
    b_real = -A_real[:, fixed_column].copy() 
    A_real = np.delete(A_real, fixed_column, axis=1)

    return A_real, b_real