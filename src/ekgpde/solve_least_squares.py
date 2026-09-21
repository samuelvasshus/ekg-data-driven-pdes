import numpy as np
import numpy.typing as npt

def solve_least_squares(
    A: npt.NDArray[np.float64],
    b: npt.NDArray[np.float64],
    fixed_column: int,
) -> tuple[npt.NDArray[np.float64], float]:
    """Solve the least-squares problem A x ≈ b and reinsert the fixed coefficient.

    Args:
        A: Real matrix from build_linear_system, fixed column removed.
        b: Real right-hand side from build_linear_system.
        fixed_column: Index of the coefficient that was fixed to 1, same as
            passed to build_linear_system.

    Returns:
        coefficients: All ODE coefficients, in the column order of
            build_linear_system, with 1 at fixed_column.
        cost: Sum of squared residuals ||A x - b||^2.
    """
    x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    cost = float(np.sum((A @ x - b)**2))
    coefficients = np.insert(x, fixed_column, 1.0)
    return coefficients, cost