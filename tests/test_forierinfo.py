from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from ekgpde.fourier import fourier_least_squares_info

DATA_PATH = Path("data/processed/nsrdb_18_records_10s.npz")

data = np.load(DATA_PATH)
record_names = data["record_names"]
ecg_signals = data["ecg_signals"]
sample_rate = float(data["sampling_rate"])

time_series = ecg_signals[0]
record_name = record_names[0]

DFT_coef, omegas = fourier_least_squares_info(time_series) 

print("Shape and DFT_coef")
print(DFT_coef.shape)
print(DFT_coef)

print("omegas")
print(omegas.shape)
print(omegas)
