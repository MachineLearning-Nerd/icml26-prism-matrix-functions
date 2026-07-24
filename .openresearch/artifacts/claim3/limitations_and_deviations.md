# Claim 3 limitations and deviations

The counterexample resolves the theorem's worst-case convergence-preservation
conjunct. It does not dispute that multiplying a `p x n` sketch by dense
matrices costs `O(p n^2)`, nor does it benchmark that cost.

The proof uses the sketch distribution and threshold exactly as printed in
Theorem 2. It also records, but does not rely on, the appendix's unexplained
change from constant `27.6` to `41.4` and the nonzero Gaussian mean.
