import numpy as np
import matplotlib.pyplot as plt

from ekgpde.convolution import convolution_gaussian
from ekgpde.fourier import fourier_least_squares_info
from ekgpde import parameters


data = np.load("data/processed/nsrdb_18_records_10s.npz")

ecg_signals = data["ecg_signals"]
time_original = data["time"]
record_names = data["record_names"]

# Bruk første halvdel av signalet
time = time_original[:len(time_original) // 2]

dt = time[1] - time[0]
sample_rate = 1 / dt


for series_index in range(3):

    # ---------------------------------------------------
    # HENT OG GLATT SIGNAL
    # ---------------------------------------------------

    time_series_original = ecg_signals[series_index]

    time_series_original = convolution_gaussian(
        time_series_original,
        2,
        3
    )

    time_series = time_series_original[
        :len(time_series_original) // 2
    ]

    record_name = record_names[series_index]


    # ---------------------------------------------------
    # FFT AV ORIGINALSIGNALET
    # ---------------------------------------------------

    u_hat = np.fft.rfft(time_series)

    frequencies = np.fft.rfftfreq(
        len(time_series),
        d=dt
    )

    omegas = 2 * np.pi * frequencies


    # ---------------------------------------------------
    # GAMMEL METODE:
    # FFT(u) * (i omega)^n
    # ---------------------------------------------------

    number_of_orders = (
        parameters.degree_of_differential_equation
    )

    old_method = np.zeros(
        (
            number_of_orders + 1,
            len(u_hat)
        ),
        dtype=complex
    )

    for derivative_order in range(
        number_of_orders + 1
    ):

        old_method[derivative_order] = (
            u_hat
            * (1j * omegas) ** derivative_order
        )


    # ---------------------------------------------------
    # NY METODE:
    # numerisk derivert -> FFT
    # ---------------------------------------------------

    new_method, omegas_new, DFT_right_side = (
        fourier_least_squares_info(
            time_series,
            time,
            parameters.polynomal_degree_right,
            sample_rate=sample_rate
        )
    )


    # ===================================================
    # PLOTT 1:
    # FFT MAGNITUDE OG FASE AV ORIGINALSIGNALET
    # ===================================================

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(14, 9),
        constrained_layout=True
    )

    fig.suptitle(
        f"Fourier analysis - record {record_name}",
        fontsize=16
    )


    # Magnitude
    axes[0].plot(
        frequencies,
        np.abs(u_hat)
    )

    axes[0].set_title(
        "Magnitude of FFT of original signal"
    )

    axes[0].set_xlabel(
        "Frequency [Hz]"
    )

    axes[0].set_ylabel(
        "|u_hat|"
    )

    axes[0].set_xlim(
        0,
        sample_rate / 2
    )

    axes[0].grid(True)


    # Fase
    axes[1].plot(
        frequencies,
        np.angle(u_hat)
    )

    axes[1].set_title(
        "Phase of FFT of original signal"
    )

    axes[1].set_xlabel(
        "Frequency [Hz]"
    )

    axes[1].set_ylabel(
        "Phase [rad]"
    )

    axes[1].set_xlim(
        0,
        sample_rate / 2
    )

    axes[1].grid(True)

    plt.show()


    # ===================================================
    # PLOTT 2:
    # SAMMENLIGN MAGNITUDE FOR DERIVASJONSMETODENE
    # ===================================================

    fig, axes = plt.subplots(
        number_of_orders,
        1,
        figsize=(14, 4 * number_of_orders),
        constrained_layout=True
    )

    if number_of_orders == 1:
        axes = [axes]

    fig.suptitle(
        (
            "Magnitude comparison of derivative methods - "
            f"record {record_name}"
        ),
        fontsize=16
    )


    for derivative_order in range(
        1,
        number_of_orders + 1
    ):

        ax = axes[
            derivative_order - 1
        ]


        # Gammel metode
        ax.plot(
            frequencies,
            np.abs(
                old_method[
                    derivative_order
                ]
            ),
            label=r"FFT(u) $\cdot (i\omega)^n$",
            linewidth=2
        )


        # Ny metode
        ax.plot(
            frequencies,
            np.abs(
                new_method[
                    derivative_order
                ]
            ),
            label="Numerical derivative -> FFT",
            linewidth=2,
            linestyle="--"
        )


        ax.set_title(
            f"Derivative order {derivative_order}"
        )

        ax.set_xlabel(
            "Frequency [Hz]"
        )

        ax.set_ylabel(
            "Magnitude"
        )

        ax.set_xlim(
            0,
            sample_rate / 2
        )

        ax.grid(True)

        ax.legend()

    plt.show()


    # ===================================================
    # PLOTT 3:
    # FASEFORSKJELL MELLOM METODENE
    # ===================================================

    fig, axes = plt.subplots(
        number_of_orders,
        1,
        figsize=(14, 4 * number_of_orders),
        constrained_layout=True
    )

    if number_of_orders == 1:
        axes = [axes]

    fig.suptitle(
        (
            "Phase difference between derivative methods - "
            f"record {record_name}"
        ),
        fontsize=16
    )


    for derivative_order in range(
        1,
        number_of_orders + 1
    ):

        ax = axes[
            derivative_order - 1
        ]


        # Faseforskjell modulo 2*pi
        phase_difference = np.abs(
            np.angle(
                old_method[derivative_order]
                * np.conj(
                    new_method[derivative_order]
                )
            )
        )


        # Gjør faseforskjellen om til prosent
        # av én hel periode
        phase_difference_percent = (
            phase_difference
            / (2 * np.pi)
            * 100
        )


        ax.plot(
            frequencies,
            phase_difference_percent,
            linewidth=2
        )


        ax.set_title(
            f"Derivative order {derivative_order}"
        )

        ax.set_xlabel(
            "Frequency [Hz]"
        )

        ax.set_ylabel(
            "Phase difference [% of full cycle]"
        )

        ax.set_xlim(
            0,
            sample_rate / 2
        )

        # Maksimal mulig korteste faseforskjell
        # er pi = 50 % av en hel syklus
        ax.set_ylim(
            0,
            50
        )

        ax.grid(True)

    plt.show()