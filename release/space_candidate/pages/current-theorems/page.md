# Claims 2–3 — exact stated-domain falsification

Current verifier: `repro/src/theorem_counterexample.py` with the independent
implementation `repro/src/check_theorem_counterexample.py`. These supersede
the historical 6×6 verifier for Claims 2 and 3.

## Exact claims and assumptions

Theorem 1 quantifies over real square `A` satisfying only
`0 < ||A||_2 <= 1` and symmetric `A^2`, with `d=1` and the exact
residual-minimizing `alpha in [1/2,1]`. It claims

`||I-X_k^2||_2 <= ||I-A^2||_2^(2^(k-2))`.

Theorem 2 uses the same matrix domain, i.i.d. `N(1,1/p)` sketch entries and
`p >= 48(log n + log(1/delta) + log k + 27.6)`. It claims the analogous
`2^(k-3)` bound with probability at least `1-delta`.

Source: arXiv:2601.22137v1, anchors `Thmtheorem1`, `Thmtheorem2`, and
`A2.SS3`; archived HTML SHA-256
`9876b930c97063af87fbfc8eb51e577920d2047d76abd4f71c1f63570b9a4866`.

## Proof certificate and raw result

Take

```text
A = [[0,-1],
     [1, 0]]
```

Then `A^T A=I`, so `||A||_2=1`, and `A^2=-I` is symmetric. All printed
matrix assumptions hold. Exact rational arithmetic gives:

| step k | `||I-X_k^2||_2` |
|---:|---:|
| 0 | 2 |
| 1 | 5 |
| 2 | 50 |
| 3 | 33125 |

For Claim 2 at `k=2`, the claimed bound is `2`; actual is `50`.
For Claim 3 with `n=2`, `delta=0.1`, `k=3`, the printed formula gives
`p_min=1522`; the claimed bound is `2`, but actual is `33125`.

For `R=rI`, the sketched loss is exactly
`|h(r,alpha)| ||S||_F`, so every nonzero sketch selects the same
`alpha=1/2`. Gaussian sketches are nonzero almost surely; Claim 3 therefore
fails with probability one, not merely in a finite sample.

- Raw machine-readable result:
  [`raw_result.json`](../../evidence/claim2/raw_result.json)
- Claim 2 contract:
  [`claim_contract.json`](../../evidence/claim2/claim_contract.json)
- Claim 3 contract:
  [`claim_contract.json`](../../evidence/claim3/claim_contract.json)
- Independent checker output:
  [`checker_output.txt`](../../evidence/claim2/checker_output.txt)
- Negative-control output:
  [`negative_control_output.txt`](../../evidence/claim2/negative_control_output.txt)
- Executable verifier:
  [`theorem_counterexample.py`](../../code/theorem_counterexample.py)
- Independent checker:
  [`check_theorem_counterexample.py`](../../code/check_theorem_counterexample.py)

Fixed command:

```text
uv run --frozen --python 3.11 python repro/src/run_reproduction.py
```

## Verdict and limitation

- Claim 2: **FALSIFIED**
- Claim 3: **FALSIFIED** (quadratic-preservation conjunct)

This falsifies the theorems exactly as printed. It does not claim failure on
the narrower, unstated domain where `A^2` is positive semidefinite and the
sketch is centered. The intended-domain sibling experiment audits that
charitable interpretation separately.
