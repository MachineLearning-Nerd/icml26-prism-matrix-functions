# Claim 1 evaluation

- Verdict: **VERIFIED**
- Confidence: **HIGH**
- Full-dimension route: six paper conditions, three seeds, five iterations
- Dense independent certificate: 12 samples, 60 states, 52 identifiable alpha
  comparisons
- Maximum identifiable alpha discrepancy: `1.8113822664034274e-08`
- Maximum next-residual discrepancy: `8.881784197001252e-16`
- Distinct fitted-alpha profiles: `9`
- Fixed-alpha mutation exit code: `7`
- Cumulative run: `e4e9a9cb-ecf6-4b09-8115-f75845800d12`
- Git revision: `8fcf992`

The dense route computes the exact matrix update directly and compares its
bounded minimizer against an independently reconstructed quartic objective
from the residual-matrix eigenvalues. The full-dimension route uses the paper's
matrix sizes in singular-value coordinates. Neither route supplies a spectral
or singular-value bound to the fit.

This verifies the named adaptive fitting mechanism. It does not verify the
paper's separate sketching theorem or its experimental timing claims.
