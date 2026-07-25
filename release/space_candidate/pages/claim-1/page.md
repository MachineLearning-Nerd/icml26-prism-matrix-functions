# Claim 1 — adaptive polynomial mechanism

## Exact contract

Section 3 Part II, Section 4.1 Equations (2)–(4), Table 1, and Appendix A.1
define the fifth-order polar update

```text
R = I - XᵀX
g₂(R; α) = I + ½R + αR²
X_next = X g₂(R; α),   α ∈ [3/8, 29/20]
```

The coefficient minimizes the next residual Frobenius norm over eigenvalues of
`R`; no explicit input singular-value interval enters that fit. The appendix
prints `X²` in one rectangular objective, which is dimensionally undefined;
we use `XᵀX`, consistent with the residual definition and Table 1.

Source: arXiv HTML retrieved 2026-07-24 with explicit User-Agent; SHA-256
`9876b930c97063af87fbfc8eb51e577920d2047d76abd4f71c1f63570b9a4866`.

## Evidence

**VERIFIED — HIGH confidence.**

The full-dimension spectral route covered the paper shapes
`15000×15000`, `20000×5000`, `100000×2000`, and `8000×4000`.
The independent dense route covered 12 matrices and 60 iteration states:

| Check | Observed | Acceptance |
| --- | ---: | ---: |
| Identifiable alpha comparisons | 52 | ≥12 |
| Max dense-vs-quartic alpha difference | 1.8114e-8 | ≤1e-5 |
| Max next-residual difference | 8.8818e-16 | ≤1e-7 |
| Distinct alpha profiles | 9 | ≥4 |
| Samples improving | 12/12 | 12/12 |

The dense primary fit directly minimizes the matrix objective. Its independent
checker reconstructs the global quartic from residual eigenvalues. All dense
objectives match the independent optimum. Seeds were `202601` and `202602`
(dense) and `202601`–`202603` (full dimension).

The negative control replaces fitted alpha with the constant `3/8`; it yields
one profile and exits `7`.

- [Executable verifier](/code/dense_prism_certificate.py)
- [Full-dimension verifier](/code/spectral_prism.py)
- [Claim contract](/evidence/claim1/claim_contract.json)
- [Raw summary](/evidence/claim1/raw_result.json)
- [Checker output](/evidence/claim1/checker_output.txt)
- [Negative-control output](/evidence/claim1/negative_control_output.txt)

Limit: this verifies the named adaptive fitting mechanism, not the separate
sketching guarantee or accelerator timing claims.
