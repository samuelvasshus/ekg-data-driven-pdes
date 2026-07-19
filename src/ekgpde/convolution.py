import numpy as np

def convolution_gaussian(
        time_series: np.ndarray,
        sigma: float,
    )->np.ndarray:
    """
    computes discrete convolution timeseries*g(t) where g is sample from normal ditsrobution. 
    """
    x = np.arange(-2, 3)

    #No need to flip distrobution since symmetric. 
    weights = np.exp(-0.5 * (x / sigma) ** 2)
    weights = weights/weights.sum()

    
    time_series_expanded = np.pad(time_series, pad_width=2, mode="constant", constant_values=0)
    convolution_result=np.zeros(len(time_series_expanded))
    for i in range (len(time_series)):
        sliced = time_series_expanded[i:i+5]
        convolution_result[i + 2] = np.dot(sliced, weights)

    convolution_result = convolution_result[2:(len(convolution_result)-2)]


    return convolution_result
