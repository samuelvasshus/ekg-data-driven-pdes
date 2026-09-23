# ekg-data-driven-pdes
Data-driven identification of differential equations from ECG signals.
Given a measured ECG time series u(t), we fit a linear ODE

    c₀·u + c₁·u′ + … + cₙ·u⁽ⁿ⁾ + a₀ + a₁·t + … = 0

by least squares in Fourier space, then simulate the identified ODE and compare it with the ECG.

##Reports
📄 **[Statusrapport for EKG-prosjektet (PDF)](docs/statusrapport.pdf)**

## Pipeline

| Step | Module | What it does |
|---|---|---|
| 1. Data | `data.py` | Download ECG segments from PhysioNet and save/load them as `.npz` |
| 2. Preprocessing | `preprocessing.py` | Gaussian smoothing to damp noise before differentiation |
| 3. Derivatives | `differentiation.py` | Central finite differences of any order |
| 4. Fourier transform | `spectral.py` | Fourier transforms of u, u′, u″, … via `(iω)ⁿ` (assumes periodicity) or finite differences (no periodicity needed) |
| 5. Linear system | `linear_system.py` | Build the real system A x ≈ b, one row per frequency, with one coefficient fixed to 1 |
| 6. Solve | `solve_least_squares.py` | Least-squares solution and fit cost |

Model settings (polynomial degree, ODE order) are in `parameters.py`.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . numpy matplotlib wfdb
python scripts/import_ecg.py
```

Plotting and experiment scripts are in `scripts/`.
