from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from ekgpde.fourier import fourier_least_squares_info
from ekgpde.build_A_b_x import build
from ekgpde.solve_least_squares import solve_least_square
from ekgpde.derivative import derivative

from ekgpde import parameters

data = np.load("data/processed/nsrdb_18_records_10s.npz")

print(data.files)

ecg_signals = data["ecg_signals"]
time = data["time"]
record_names = data["record_names"]
sampling_rate = data["sampling_rate"]
#len(ecg_signals)
for series_index in range(1):
    time_series = ecg_signals[series_index]
    record_name = record_names[series_index]



    coeficient_equal_1 = 1
    DFT_coef, omegas, DFT_right_side = fourier_least_squares_info(time_series,time, parameters.polynomal_degree_right) 

    A, b = build(DFT_coef, omegas, DFT_right_side, parameters.polynomal_degree_right,coeficient_equal_1)

    u_coeficients, cost = solve_least_square(A, b, coeficient_equal_1)

    #2. ordens
    # Y_(n+1) = y'(n)*delta_t + Y_n = [y_t, -(a_1 + a_2*y + a_3*y_t) ]*delta_t


    Y_coef = np.zeros((len(u_coeficients)), dtype=complex)
    for i in range (len(u_coeficients)):
        Y_coef[i] = u_coeficients[i]
    #kortere intervaller enn puls i EKG

    dt = time[1]- time[0]
    t = 0

    Y = np.array([time_series[0], derivative(time_series, 0, 1, dt)])
    Y_vals = [Y.copy()]

    t = time[0]
    t_vals = np.array([time[0]])
    #Lite effektivt siden lager nye arrayer hele tiden. Kan fikses senere hvis det blir problem. 
    while (t<(time[-1])):
        Y = np.array([Y[1], -(Y_coef[0] + Y_coef[1]*Y[0] + Y_coef[2]*Y[1] )])*dt + Y 
        Y_vals.append(Y.copy())
        t += dt
        t_vals = np.append(t_vals, t)
    Y_vals = np.array(Y_vals)



    #Chat GPT for plotting:
    plt.figure(figsize=(14, 6))

    plt.plot(time, time_series, label="EKG-signal")

    plt.plot(
        t_vals,
        np.real(Y_vals[:, 0]),
        label="Differensialligning",
    )

    plt.xlabel("Tid [s]")
    plt.ylabel("Amplitude")
    plt.title(f"EKG-signal og løsning av differensialligning: {record_name}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


