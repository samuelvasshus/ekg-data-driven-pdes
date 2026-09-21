from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from ekgpde.spectral import spectral_derivatives
from ekgpde.linear_system import build_linear_system
from ekgpde.solve_least_squares import solve_least_squares

from ekgpde import parameters

data = np.load("data/processed/nsrdb_18_records_10s.npz")

print(data.files)

ecg_signals = data["ecg_signals"]
time = data["time"]
record_names = data["record_names"]
sampling_rate = data["sampling_rate"]


time_series = ecg_signals[0]
record_name = record_names[0]


coeficient_equal_1 = 1
DFT_coef, omegas, DFT_right_side = spectral_derivatives(time_series, time, 2, parameters.polynomal_degree_right) 

A, b = build_linear_system(DFT_coef, DFT_right_side, parameters.polynomal_degree_right, coeficient_equal_1)

u, cost = solve_least_squares(A, b, coeficient_equal_1)

print("u:")
print(u.shape)
print(u)

print("cost:")
print(np.shape(cost))
print(cost)