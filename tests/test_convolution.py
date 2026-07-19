#Chat gpt for testing av importert kovolusjon data

import numpy as np
import matplotlib.pyplot as plt
from ekgpde.convolution import convolution_gaussian

data = np.load("data/processed/nsrdb_18_records_10s.npz")

print(data.files)

ecg_signals = data["ecg_signals"]
time = data["time"]
record_names = data["record_names"]
sampling_rate = data["sampling_rate"]

print(ecg_signals.shape)
print(time.shape)
print(record_names)
print(sampling_rate)

print(ecg_signals)
print(time)

n_records = ecg_signals.shape[0]

for i in range(5):
    signal = ecg_signals[i]

    # Hvis signalet har flere kanaler, velg kanal 0
    if signal.ndim == 2:
        signal = signal[:, 0]

    signal = convolution_gaussian(signal, 10)

    plt.figure(figsize=(14, 5))
    plt.plot(time, signal)

    plt.title(f"ECG signal {i + 1}: {record_names[i]}")
    plt.xlabel("Time [s]")
    plt.ylabel("ECG")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


