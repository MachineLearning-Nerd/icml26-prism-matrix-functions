# Claim 6 limitations and deviations

- Full paper matrix dimensions and distribution parameters are used, but only
  their singular values are materialized. Dense GEMM wall-clock speed is not
  reproduced.
- The paper's undisclosed seeds are replaced by three declared seeds.
- The paper does not disclose its practical sketch dimension. Exact PRISM
  fitting is used; sketch sensitivity is delegated to the dense sibling.
- The paper reports float32/A100. This route uses float64/HF CPU and therefore
  evaluates convergence, not hardware timing.
- The cited HTMP sampler has a printed indexing error. The PSD bidiagonal
  reconstruction is used and the literal formula is tested as a negative
  control.
- Because the paper's words “stable” and “degrades” lack a numerical
  threshold, the contract predeclares a multi-threshold first-hit analysis.
  Alignment under that operationalization is scoped evidence, not a universal
  proof or an exact recovery of undisclosed plot data.
