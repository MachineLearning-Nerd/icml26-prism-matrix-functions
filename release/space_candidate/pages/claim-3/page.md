# Claim 3 — printed Theorem 2

## Exact contract and assumptions

Theorem 2 uses the same printed matrix domain as Theorem 1 and states, with
probability at least `1-δ` over independent Gaussian sketches with entries
printed as `N(1,1/p)`, that the convergence bound holds when

```text
p ≥ 48(log n + log(1/δ) + log k + 27.6).
```

The proof instead contains `+41.4`; this source inconsistency is recorded, not
silently repaired. Source anchors `Thmtheorem2` and `A2.SS3`.

## Counterexample

**FALSIFIED — HIGH confidence.**

For the exact matrix from Claim 2, `R_k = r_k I`. Consequently every sketched
Frobenius objective is a positive random scalar times the same one-dimensional
objective, so the minimizing alpha and the divergent trajectory are
sketch-independent whenever the sketch is nonzero. With Gaussian sketches that
event has probability one.

At `n=2`, `δ=0.1`, `k=3`, the printed integer threshold is `p_min=1522`.
The residual is `33125`; the claimed bound is `2`. Failure probability is `1`,
greater than allowed `0.1`. This falsifies the convergence-preservation
conjunct; it does not dispute the separate arithmetic-cost expression.

- [Executable certificate](/code/theorem_counterexample.py)
- [Independent checker](/code/check_theorem_counterexample.py)
- [Contract](/evidence/claim3/claim_contract.json)
- [Raw result](/evidence/claim3/raw_result.json)
- [Checker output](/evidence/claim2/checker_output.txt)
- [Negative-control output](/evidence/claim3/negative_control_output.txt)
