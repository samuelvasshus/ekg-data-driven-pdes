from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from ekgpde.convolution import convolution_gaussian
from ekgpde.fourier import fourier_least_squares_info
from ekgpde.build_A_b_x import build
from ekgpde.solve_least_squares import solve_least_square
from ekgpde.derivative import derivative

from ekgpde import parameters

data = np.load("data/processed/nsrdb_18_records_10s.npz")

print(data.files)

ecg_signals = data["ecg_signals"]
time_original = data["time"]
time = time_original[0:int(len(time_original)/2)]
record_names = data["record_names"]
sampling_rate = data["sampling_rate"]
#len(ecg_signals)
for series_index in range(5):
    time_series_original = ecg_signals[series_index]
    time_series = time_series_original[0:int(len(time_series_original)/2)]
    time_series_original = convolution_gaussian(time_series_original, 5, 10)
    record_name = record_names[series_index]
    time_series = convolution_gaussian(time_series, 5, 10)



    coeficient_equal_1 = 1
   
    DFT_coef, omegas, DFT_right_side = fourier_least_squares_info(time_series,time, parameters.polynomal_degree_right) 

    A, b = build(DFT_coef, omegas, DFT_right_side, parameters.polynomal_degree_right,coeficient_equal_1)

    u_coeficients, cost = solve_least_square(A, b, coeficient_equal_1)

    print("Cost:")
    print(cost)

    #2. ordens
    # Y_(n+1) = y'(n)*delta_t + Y_n = [y_t, -(a_1 + a_2*y + a_3*y_t) ]*delta_t


    Y_coef = np.zeros((len(u_coeficients)), dtype=complex)
    for i in range (len(u_coeficients)):
        Y_coef[i] = u_coeficients[i]
    #kortere intervaller enn puls i EKG

    dt = time[1]- time[0]
    t = 0

    #Y = np.array([time_series[0], derivative(time_series, 0, 1, dt)])
    #print("Deriv value:")
    #print(derivative(time_series, 0, 1, dt))
    Y = np.array([time_series[0], 0])
    Y_vals = [Y.copy()]

    t = time[0]
    t_vals = np.array([time[0]])
    #Lite effektivt siden lager nye arrayer hele tiden. Kan fikses senere hvis det blir problem.
    print("Y_0/ Y, Y_t, Y_tt:")
    print([Y[0], Y[1], -(Y_coef[0] + Y_coef[1]*Y[0] + Y_coef[2]*Y[1] )]) 
    while (t<(time_original[-1])):
        #/Y_coef[3]
        Y = np.array([Y[1], -(Y_coef[0] + Y_coef[1]*Y[0] + Y_coef[2]*Y[1] )])*dt + Y 
        Y_vals.append(Y.copy())
        t += dt
        t_vals = np.append(t_vals, t)
    Y_vals = np.array(Y_vals)



    #Chat GPT for plotting:
    plt.figure(figsize=(14, 6))

    plt.plot(time_original, time_series_original, label="EKG-signal")

    plt.plot(
        t_vals,
        np.real(Y_vals[:, 0]),
        label="Differensialligning",
    )

    prediction_start = time[-1]

    plt.axvline(
        x=prediction_start,
        linestyle="--",
        linewidth=2,
        label="Start på prediksjon",
    )

    plt.text(
        prediction_start + 0.1,
        plt.ylim()[1] * 0.9,
        "Etter denne linjen\npredikerer differensiallikningen videre",
        verticalalignment="top",
        fontsize=11,
        bbox={
            "facecolor": "white",
            "alpha": 0.8,
            "edgecolor": "gray",
        },
    )

    #Chat GPT to write corresponding diff eqn
    terms = []

    for i, coefficient in enumerate(Y_coef):
        if np.isclose(coefficient, 0):
            continue

        if i == 0:
            term = f"{abs(coefficient):.3g}"
        elif i == 1:
            term = f"{abs(coefficient):.3g}Y"
        elif i == 2:
            term = f"{abs(coefficient):.3g}Y_t"
        else:
            term = f"{abs(coefficient):.3g}Y_{{t^{i - 1}}}"

        if len(terms) == 0:
            terms.append(("-" if coefficient < 0 else "") + term)
        else:
            terms.append((" - " if coefficient < 0 else " + ") + term)

    equation_text = "$" + "".join(terms) + " = 0$"

    plt.text(
        0.02,
        0.98,
        equation_text,
        transform=plt.gca().transAxes,
        verticalalignment="top",
        fontsize=12,
        bbox={"facecolor": "white", "alpha": 0.8},
    )



    plt.xlabel("Tid [s]")
    plt.ylabel("Amplitude")
    plt.title(f"EKG-signal og løsning av differensialligning: {record_name}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


