import numpy as np


def derivative(
        time_series: np.ndarray,
        index: int,
        power: int,
        dt: float,
) -> int:
    if (power == 0):
        return time_series[index]
    elif (power==1):
        return (time_series[index + 1]-time_series[index])/dt
    elif (power==2):
        #print("deriv2")
        return (time_series[index + 2]-2*time_series[index + 1] + time_series[index])/(dt**2)
        
    elif power == 3:
        #print("KK")
        
        return (
            time_series[index + 3]
            - 3 * time_series[index + 2]
            + 3 * time_series[index + 1]
            - time_series[index]
        ) / dt**3

    elif power == 4:
        return (
            time_series[index + 4]
            - 4 * time_series[index + 3]
            + 6 * time_series[index + 2]
            - 4 * time_series[index + 1]
            + time_series[index]
        ) / dt**4

    
    else:
        
        raise ValueError("power must be between 0 and 4")