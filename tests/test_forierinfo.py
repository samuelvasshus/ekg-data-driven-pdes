from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from ekgpde.spectral import finite_difference_derivatives
from ekgpde import parameters

DATA_PATH = Path("data/processed/nsrdb_18_records_10s.npz")

data = np.load(DATA_PATH)
record_names = data["record_names"]
ecg_signals = data["ecg_signals"]
sample_rate = float(data["sampling_rate"])
time = data["time"]


time_series = ecg_signals[0]
record_name = record_names[0]

DFT_coef, omegas, DFT_right_side = finite_difference_derivatives(time_series, time, parameters.degree_of_differential_equation, parameters.polynomal_degree_right) 

print("Shape and DFT_coef")
print(DFT_coef.shape)
print(DFT_coef)

print("omegas")
print(omegas.shape)
print(omegas)

print("Shape and DFT right side")
print(DFT_right_side.shape)
print(DFT_right_side)

