# Claim 1 source audit

Source: ar5iv HTML for arXiv:2601.22137, retrieved 2026-07-24 with
`OpenResearch-Reproduction/1.0 (contact: local-user; paper 2601.22137)`.
SHA-256: `9876b930c97063af87fbfc8eb51e577920d2047d76abd4f71c1f63570b9a4866`.

The imported judge wording points to Section 4.1, but the complete mechanism
spans Section 3 Part II, Equations (2)-(4), Table 1, and Appendix A.1.
For a polar factor, the paper defines

`R_k = I - X_k^T X_k`,

`g_2(R; alpha) = I + (1/2) R + alpha R^2`,

and recommends `alpha in [3/8, 29/20]`. The exact fit minimizes the squared
Frobenius norm of the next residual. Because the residual is symmetric, this is
a nonlinear least-squares fit over its eigenvalues. No singular-value bounds
for the input matrix enter this objective.

The polar equation printed in Appendix A.1 contains `X_k^2` inside its fitting
objective even though the same paragraph defines `R_k=I-X_k^T X_k`.
For rectangular matrices `X_k^2` is dimensionally undefined. This reproduction
uses `X_k^T X_k`, consistent with Table 1 and the residual definition, and
flags the correction rather than treating the typo as executable mathematics.

The paper does not disclose a practical sketch dimension for Figures 3-4.
This route therefore tests the exact (unsketched) spectrum-fitting mechanism.
Sketch fidelity is addressed separately and is not silently inferred here.
