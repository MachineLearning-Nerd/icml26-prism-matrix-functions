# Claim 6 evaluation

- Verdict: **BLOCKED**
- Confidence: **LOW**
- Verification routes completed: `3`
- Mandatory falsification route completed: `1`
- Cumulative run: `e4e9a9cb-ecf6-4b09-8115-f75845800d12`
- Git revision: `8fcf992`

The full-dimension spectral reconstruction did not meet the predeclared
alignment rule: PRISM did not reach RMS residual `0.01` for every condition and
seed, and it was not uniformly no slower than PolarExpress. That result is not
a falsification because the exact HTMP draw, executable, sketch dimension,
seed, and timing protocol used for the paper figures are unpublished.

Three materially different verification routes were completed: calibrated
finite-sampler mappings, direct limiting-density reconstruction, and archival
artifact recovery. The mandatory fourth route proves nonconvergence for one
deterministic limiting-density spectrum but rejects it as a falsification of
the exact statement, which only reports the authors' particular experiments.
The independent checker passed and an assumption-violating zero-singular-value
candidate was rejected.
