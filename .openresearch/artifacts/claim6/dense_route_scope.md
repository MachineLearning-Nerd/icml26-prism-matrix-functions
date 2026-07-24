# Claim 6 dense-route scope

This route covers all six named distribution parameters with explicit dense
matrix arithmetic, three seeds, exact fitting, and a randomized-sketch
sensitivity run. Shapes are scaled down to keep CPU cost bounded. It can
validate that the full-dimension singular-value-coordinate calculation uses
the correct matrix polynomial, but it cannot independently establish the
paper-scale convergence or wall-clock comparison.

The route is therefore corroborating evidence for Claim 6, never a standalone
`VERIFIED` result.
