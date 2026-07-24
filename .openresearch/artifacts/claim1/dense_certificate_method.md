# Direct dense PRISM mechanism certificate

The primary implementation constructs `R = I - X.T @ X`, evaluates
`X(I + R/2 + alpha R^2)` with dense matrix products, and minimizes the exact
next-residual Frobenius loss over `[3/8, 29/20]`.

The independent checker diagonalizes `R`, expands the same loss as a quartic
in `alpha`, enumerates every real stationary point in the interval plus both
endpoints, and selects the global minimum.

After convergence the quartic can be numerically flat, so coefficient equality
is required only while the optimal objective exceeds the predeclared
`1e-12` identifiability floor. At every iteration, including flat ones, the
direct objective and next residual must still match the independent optimum.
This closes the failure in the rejected 49-minute dense route, which compared
non-identifiable coefficients.

The negative control replaces every fitted coefficient with `3/8`; it must
fail the spectrum-adaptation requirement by producing one profile.
