# Claim 1 method

The polar update is unitarily invariant. If `A=U diag(s) V^T`, the matrix
iteration is exactly represented by

`s <- s * (1 + 0.5*(1-s^2) + alpha*(1-s^2)^2)`.

For a candidate alpha, each next residual eigenvalue is a quadratic in alpha.
The squared Frobenius objective is therefore a quartic. The verifier constructs
all quartic coefficients, finds all real stationary points in the permitted
interval, compares them with both endpoints, and selects the global minimizer.
As a separate numerical check, its objective must be no worse than a fixed
1001-point grid.

The spectra are sampled from exact real beta-Laguerre tridiagonal ensembles.
This gives the singular values of the corresponding Gaussian or HTMP matrix
without allocating dense matrices. Three predeclared seeds and all paper
dimensions are used. The alpha trajectory itself is the adaptation evidence.

The PolarExpress control is reconstructed from
NoahAmsel/PolarExpress revision
`6f1bb73a2e1b724c92f90303845c045e7d32c892`, including its `1e-3` lower
bound, 1% safety factor, and 0.02 cushion.
