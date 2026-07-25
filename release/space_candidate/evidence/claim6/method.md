# Claim 6 method

For each of the six exact paper dimensions and three deterministic seeds, the
verifier samples the singular values from the corresponding real
beta-Laguerre ensemble:

- Gaussian: beta 1.
- HTMP: beta `kappa/m`.

It normalizes by the matrix Frobenius norm and runs 24 iterations of:

1. fifth-order PRISM with an exact bounded residual fit;
2. classical fifth-order Newton-Schulz (`alpha=3/8`);
3. PolarExpress Algorithm 1 reconstructed from the authors' public source.

Every iteration records Frobenius and RMS residuals. First-hit iterations are
computed independently for RMS thresholds 0.1, 0.01, and 0.001. The primary
contract uses 0.01; the other two thresholds are a calibration sweep against a
convenient single threshold. Results report all 18 paired samples, not only a
representative curve.

The computation parallelizes six independent samples. No dense matrix or GPU
is used. The spectral trajectory is exact for polynomial iterations, while
dense wall-clock behavior is explicitly outside this route.
