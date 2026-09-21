from math import comb

import numpy as np
import numpy.typing as npt


def _forward_difference(
    time_series: npt.NDArray[np.float64],
    start: int,
    order: int,
    dt: float,
) -> float:
    """Pascal forward difference over time_series[start], ..., time_series[start + order]."""
    total = 0.0
    for j in range(order + 1):
        coefficient = (-1)**(order - j)*comb(order, j)
        total += coefficient * time_series[start + j]
    return total/dt**order


def differentiate(
    time_series: npt.NDArray[np.float64],
    index: int,
    order: int,
    dt: float,
) -> float: #Seems be more resilient to noise than forward_difference, look at this more in detail
    """Estimate the derivative of a given order at one point, using the Pascal
    formula centred on `index` (one-sided near the ends).

    Args:
        time_series (npt.NDArray[np.float64]): Uniformly sampled signal.
        index (int): Position to differentiate at.
        order (int): Derivative order (0 returns the value itself).
        dt (float): Time between samples, in seconds.

    Returns:
        float: Estimate of the `order`-th derivative at `index`.
    """
    length = len(time_series)
    if order < 0:
        raise ValueError(f"order must be non-negative, got {order}")
    if length <= 2*order:
        raise ValueError(f"time_series needs more than {2*order} samples for order {order}, got {length}")
    if not 0 <= index < length:
        raise IndexError(f"index {index} out of range for time_series of length {length}")

    half_width = (order + 1)//2

    if index - half_width < 0:
        return _forward_difference(time_series, index, order, dt)
    if index + half_width >= length:
        return _forward_difference(time_series, index - order, order, dt)

    if order % 2 == 0:
        return _forward_difference(time_series, index - half_width, order, dt)
    return 0.5*(
        _forward_difference(time_series, index - half_width, order, dt)
        + _forward_difference(time_series, index - half_width + 1, order, dt)
    )
