import numpy as np

def Forier_info(time_series):
    return np.fft.fft(time_series), np.fft.rfft(time_series)
