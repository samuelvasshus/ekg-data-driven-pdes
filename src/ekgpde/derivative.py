import numpy as np


def derivative(
        time_series: np.ndarray,
        index: int,
        power: int,
        dt: float,
) -> int:
    if (power==1):
        return (time_series[index + 1]-time_series[index])/dt
    elif (power==2):
        return (time_series[index + 2]-2*time_series[index + 1] + time_series[index])/(dt**2)
    else:
        return 0