# Claim 2 — printed Theorem 1

## Exact contract and assumptions

Theorem 1 is universally quantified over real square `A` with
`0 < ||A||₂ ≤ 1`, symmetric `A²`, `X₀=A`, degree `d=1`, and exact residual
minimization over `α∈[1/2,1]`. It concludes convergence to `sign(A)` and

```text
||I-X_k²||₂ ≤ ||I-A²||₂^(2^(k-2)).
```

Source anchor `Thmtheorem1`; HTML SHA-256
`9876b930c97063af87fbfc8eb51e577920d2047d76abd4f71c1f63570b9a4866`.

## Exact rational counterexample

**FALSIFIED — HIGH confidence.**

Take `A=[[0,-1],[1,0]]`. Then `A` is real square, `||A||₂=1`, and
`A²=-I` is symmetric. The alpha objective is exact and deterministic.

| k | Exact residual norm | Printed bound |
| ---: | ---: | ---: |
| 0 | 2 | — |
| 1 | 5 | — |
| 2 | 50 | 2 |
| 3 | 33125 | 4 |

The violation at `k=2` is `50 > 2`. All arithmetic is a machine-checkable
integer/rational certificate; no seed or tolerance is used. The independent
checker reconstructs the assumptions and trajectory. A mutated expected
residual fails with exit code `5`.

- [Executable certificate](/code/theorem_counterexample.py)
- [Independent checker](/code/check_theorem_counterexample.py)
- [Contract](/evidence/claim2/claim_contract.json)
- [Raw result](/evidence/claim2/raw_result.json)
- [Checker output](/evidence/claim2/checker_output.txt)
- [Negative control](/evidence/claim2/negative_control_output.txt)

Limit: this falsifies the printed domain. It does not claim failure after adding
an unstated positive-semidefinite condition on `A²`.
