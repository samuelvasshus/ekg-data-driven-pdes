#Chat gpt for testing av importert data

import numpy as np

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

