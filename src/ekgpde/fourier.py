import numpy as np

def Forier_Least_square_info(time_series):
    return np.fft.fft(time_series), 2*np.pi*np.fft.rfftfreq(time_series)
