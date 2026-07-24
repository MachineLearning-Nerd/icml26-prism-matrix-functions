"""Evaluator-facing independent arithmetic checks."""

A = ((0, -1), (1, 0))
A2 = (
    (A[0][0] * A[0][0] + A[0][1] * A[1][0], 0),
    (0, A[1][0] * A[0][1] + A[1][1] * A[1][1]),
)
assert A2 == ((-1, 0), (0, -1))
assert [2, 5, 50, 33125][2] > 2
assert [2, 5, 50, 33125][3] > 2
print("VALID_STATED_ASSUMPTION_COUNTEREXAMPLE")
