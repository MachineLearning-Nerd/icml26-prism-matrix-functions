# Dense route limitations

- Dense dimensions are scaled down, so this route validates implementation
  equivalence and sketch behavior rather than paper-scale convergence.
- The paper omits its practical sketch dimension and uses the phrase Gaussian
  sketch inconsistently with Theorem 2's printed nonzero mean. This route uses
  the standard OSE convention `N(0,1/p)`.
- Float64 is used to make an exact dense-versus-spectral checker meaningful.
- The HTMP matrix uses a bidiagonal beta-Laguerre factor, so its singular
  vectors are structured. Polynomial residual trajectories depend only on
  singular values; sketch outcomes do depend on the basis, which is why they
  are treated as sensitivity evidence only.
