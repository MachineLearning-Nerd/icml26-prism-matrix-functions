# Claim 1 limitations and deviations

- This route uses exact singular-value-coordinate arithmetic. It is
  mathematically identical to the dense polynomial trajectory in exact
  arithmetic, but it cannot reproduce dense GEMM timing or rounding order.
- Arithmetic is float64 rather than the paper's float32. A separate dense
  experiment checks the coordinate equivalence at CPU-feasible dimensions.
- The paper omits the practical sketch dimension used in Figures 3-4. This
  route tests the exact fitting objective, not an undisclosed sketch.
- The dimensionally invalid `X_k^2` in Appendix A.1 is corrected to
  `X_k^T X_k`, following the residual definition and Table 1.
- Finite experiments corroborate the mechanism on the claimed empirical
  families; they are not a proof of a universal performance statement.
