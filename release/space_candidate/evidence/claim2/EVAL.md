# Claim 2 evaluation

- Verdict: **FALSIFIED**
- Primary certificate: `counterexample.json`
- Exact result: `raw_result.json`
- Primary verifier: `repro/src/theorem_counterexample.py`
- Independent checker: `repro/src/check_theorem_counterexample.py`
- Negative control: `negative_control.json` (must exit nonzero)
- Fixed command: `uv run --frozen --python 3.11 python repro/src/run_reproduction.py`
- Random seed: none; all trajectory arithmetic is rational
- Limitation: this falsifies the printed theorem domain. It does not assert
  failure after adding the unstated condition `A^2` positive semidefinite.
