import numpy as np

def convolution_gaussian(
        time_series: np.ndarray,
        sigma: float,
        convolution_degree: int,
    )->np.ndarray:
    """
    computes discrete convolution timeseries*g(t) where g is sample from normal ditsrobution. 
    """
    x = np.arange(-convolution_degree, convolution_degree+1)

    #No need to flip distrobution since symmetric. 
    weights = np.exp(-0.5 * (x / sigma) ** 2)
    weights = weights/weights.sum()

    
    time_series_expanded = np.pad(time_series, pad_width=convolution_degree, mode="constant", constant_values=0)
    convolution_result=np.zeros(len(time_series_expanded))
    for i in range (len(time_series)):
        sliced = time_series_expanded[i:i+2*convolution_degree+1]
        convolution_result[i + convolution_degree] = np.dot(sliced, weights)

    convolution_result = convolution_result[convolution_degree:(len(convolution_result)-convolution_degree)]
    print(weights)

    return convolution_result
