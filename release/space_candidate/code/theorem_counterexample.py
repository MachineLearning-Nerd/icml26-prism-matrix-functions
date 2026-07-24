"""Evaluator copy. Canonical source: repro/src/theorem_counterexample.py."""

from fractions import Fraction


def h(residual: Fraction, alpha: Fraction) -> Fraction:
    return 1 - (1 - residual) * (1 + alpha * residual) ** 2


residuals = [Fraction(2)]
for _ in range(3):
    residuals.append(h(residuals[-1], Fraction(1, 2)))

assert residuals == [2, 5, 50, 33125]
assert residuals[2] > 2
assert residuals[3] > 2
print("CLAIM_2=FALSIFIED CLAIM_3=FALSIFIED")
