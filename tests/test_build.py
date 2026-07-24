from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from ekgpde.fourier import fourier_least_squares_info
from ekgpde.build_A_b_x import build

from ekgpde import parameters

data = np.load("data/processed/nsrdb_18_records_10s.npz")

print(data.files)

ecg_signals = data["ecg_signals"]
time = data["time"]
record_names = data["record_names"]
sampling_rate = data["sampling_rate"]


time_series = ecg_signals[0]
record_name = record_names[0]



DFT_coef, omegas, DFT_right_side = fourier_least_squares_info(time_series,time, parameters.polynomal_degree_right) 

A, b = build(DFT_coef, omegas, DFT_right_side, parameters.polynomal_degree_right,1)

print("A:")
print(A.shape)
print(A)

print("b:")
print(b.shape)
print(b)

DFT_coef, omegas, DFT_right_side = np.ones(5, dtype=complex), np.ones(5, dtype=complex), np.ones(5, dtype=complex)


A1, b1 = build(DFT_right_side, omegas, DFT_right_side, parameters.polynomal_degree_right,1)

print("A1:")
print(A1.shape)
print(A1)

print("b1:")
print(b1.shape)
print(b1)