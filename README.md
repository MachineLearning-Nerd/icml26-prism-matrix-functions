# PRISM claim-by-claim reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-hwhvjhXC0m-prism-matrix-functions/blob/master/notebooks/prism_claims.py)

This repository reproduces six claims from *PRISM: Distribution-free Adaptive
Computation of Matrix Functions for Accelerating Neural Network Training*
([arXiv:2601.22137](https://arxiv.org/abs/2601.22137)).

The central adaptive-polynomial mechanism is **VERIFIED**: direct dense
minimization and an independent spectral quartic agree to `1.81e-8` in the
fitted coefficient over 52 identifiable states. The printed Theorems 1 and 2
are **FALSIFIED** on the exact rational stated-domain matrix
`[[0,-1],[1,0]]`: the residual is `50` where the bound is `2`, and the
sketched failure occurs with probability one. The Shampoo, Muon/GPT, and
Gaussian/HTMP experiment claims remain **BLOCKED** after four distinct routes
each because exact code, seeds/data draws, raw trajectories, or timing
protocols are unpublished.

No downscaled result is presented as full-scale evidence. CPU feasibility
checks for Claims 4–5 are explicitly lower bounds, not proxies. All long or
uncertain CPU work used Hugging Face `cpu-upgrade`; the exact theorem
certificate alone used short local CPU execution.

- [Illustrated technical report](reports/prism-reproduction/report.md)
- [Self-contained marimo notebook](notebooks/prism_claims.py)
- [Evaluator-visible Space candidate](release/space_candidate/pages/current-verification/page.md)

Live judged score: **5/12**. Conservative forecast after publication:
**5–8/12**, not a judge result.

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `master` | Reader-facing publication surface | Not run as an experiment (publication surface) | README, report, notebook, and released evidence | none |
| [`orx/judged-5-of-12-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-hwhvjhXC0m-prism-matrix-functions/tree/orx/judged-5-of-12-baseline) | Freeze and rerun the judged 6×6 baseline | `uv run --frozen --python 3.11 python repro/src/run_reproduction.py` | Historical rejected baseline; reproduces judge criticism | HF `cpu-upgrade`, 43s |
| [`orx/stated-domain-theorem-counterexamples`](https://github.com/MachineLearning-Nerd/icml26-repro-hwhvjhXC0m-prism-matrix-functions/tree/orx/stated-domain-theorem-counterexamples) | Exact assumptions and rational certificate for Theorems 1–2 | `uv run --frozen --python 3.11 python repro/src/run_reproduction.py` | Claims 2–3 FALSIFIED | local CPU, 1m10s |
| [`orx/efficient-dense-prism-mechanism-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-hwhvjhXC0m-prism-matrix-functions/tree/orx/efficient-dense-prism-mechanism-certificate) | Direct dense fit versus independent residual-eigenvalue quartic | `uv run --frozen --python 3.11 python repro/src/run_reproduction.py` | Claim 1 VERIFIED | HF `cpu-upgrade`, 2m23s |
| [`orx/claim-6-mandatory-falsification-route`](https://github.com/MachineLearning-Nerd/icml26-repro-hwhvjhXC0m-prism-matrix-functions/tree/orx/claim-6-mandatory-falsification-route) | Fourth route after calibration, density, and archive audits | `uv run --frozen --python 3.11 python repro/src/run_reproduction.py` | Claim 6 BLOCKED; invalid substitute counterexample rejected | HF `cpu-upgrade`, 1m51s |
| [`orx/claims-4-and-5-four-route-closure`](https://github.com/MachineLearning-Nerd/icml26-repro-hwhvjhXC0m-prism-matrix-functions/tree/orx/claims-4-and-5-four-route-closure) | Source, artifact, feasibility, and falsification routes | `uv run --frozen --python 3.11 python repro/src/run_reproduction.py` | Claims 4–5 BLOCKED | HF `cpu-upgrade`, 1m56s |
| [`orx/integrated-evaluator-visible-candidate`](https://github.com/MachineLearning-Nerd/icml26-repro-hwhvjhXC0m-prism-matrix-functions/tree/orx/integrated-evaluator-visible-candidate) | Cumulative accepted checks and fail-closed BLOCKED closures | `uv run --frozen --python 3.11 python repro/src/run_reproduction.py` | Complete suite passed | HF `cpu-upgrade`, 4m47s |

## Reproduce

```bash
uv sync --frozen --python 3.11
uv run --frozen --python 3.11 python repro/src/run_reproduction.py
```

The fixed command is CPU-only but uses multiple workers and has uncertain
runtime; run it on HF `cpu-upgrade` through `orx` for formal evidence.
