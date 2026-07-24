# Independent dense route

This sibling does not import the spectral implementation. It constructs
rectangular matrices explicitly, forms `R=I-X^T X`, minimizes the dense next
residual with SciPy's bounded scalar optimizer, and applies the matrix
polynomial directly.

An independent checker takes the SVD once, derives the quartic coefficients in
singular-value coordinates, solves all stationary points plus endpoints, and
propagates the singular values. Alpha and residual trajectories must agree
with dense arithmetic to `1e-7`.

The randomized route draws a fresh `p x m` Gaussian matrix with entries
`N(0,1/p)` at every iteration and minimizes the actual dense sketched
residual. The practical `p=64` is a predeclared sensitivity setting, not an
attempt to guess the undisclosed sketch dimension used by the paper.

Dense dimensions are CPU-feasible substitutes:

| Family | Parameter | Dense shape |
|---|---:|---:|
| Gaussian | 1 | 256 x 256 |
| Gaussian | 4 | 512 x 128 |
| Gaussian | 50 | 3200 x 64 |
| HTMP | 0.1, 0.5, 100 | 256 x 128 |

The full paper dimensions are evaluated in the sibling spectral route.
