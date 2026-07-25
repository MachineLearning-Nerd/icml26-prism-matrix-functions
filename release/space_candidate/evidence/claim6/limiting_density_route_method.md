# Limiting-density HTMP route

This route independently implements the closed-form HTMP density in Equation
E.5 of Hodgkinson, Wang, and Mahoney (2025), the source cited by PRISM.

The density is integrated in log-eigenvalue coordinates over a fixed grid.
The `dx = x dlog(x)` Jacobian is explicit and is mutation-tested. Four thousand
deterministic midpoint quantiles define the spectrum at the paper's column
dimension; taking square roots and Frobenius-normalizing reconstructs the
singular values used by the polar iteration.

The route uses all three displayed kappa values and the same six marker-width
first-hit brackets fixed for the finite-sampler calibration. It exits nonzero
if the density does not normalize, if any numerical invariant fails, or if any
published anchor is missed.
