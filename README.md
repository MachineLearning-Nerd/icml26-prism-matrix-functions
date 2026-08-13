# ICML 2026 — PRISM: Adaptive Matrix Functions

Independent reproduction audit for *PRISM: Distribution-free Adaptive
Computation of Matrix Functions for Accelerating Neural Network Training*.

Paper: [arXiv:2601.22137v1](https://arxiv.org/abs/2601.22137) ·
[OpenReview:hwhvjhXC0m](https://openreview.net/forum?id=hwhvjhXC0m)

## Current verdict

Overall status: **INCONCLUSIVE — VERIFIED SCOPED FINDINGS WITH BLOCKED
PAPER-LEVEL EXPERIMENTS**.

| Claim | Verdict | What is actually established |
| --- | --- | --- |
| C1 | `VERIFIED_SCOPED` | The adaptive residual-polynomial fitting mechanism is reproduced: direct dense minimization agrees with an independently derived spectral quartic. This does not verify every matrix-function or training claim. |
| C2 | `FALSIFIED_AS_PRINTED` | The printed Theorem 1 bound fails for the exact rational matrix `A=[[0,-1],[1,0]]`, which satisfies the stated assumptions. |
| C3 | `FALSIFIED_AS_PRINTED` | On that same matrix, the sketch objective is only a positive scalar multiple of the exact objective, so the Theorem 2 minimizer and the C2 failure are unchanged with probability one. The separate cost conjunct is not assessed by this counterexample. |
| C4 | `BLOCKED` | The Shampoo/ResNet timing claim cannot be reproduced or falsified at paper level without the exact models, data protocol, integration, seeds, and timing artifacts. |
| C5 | `BLOCKED` | The Muon/GPT loss comparison cannot be reproduced or falsified at paper level without the exact model, data, checkpoints, seeds, and raw trajectories. |
| C6 | `BLOCKED` | The Gaussian/HTMP robustness claim cannot be tied to a reconstructed run because the exact random draws, code, curves, and timing protocol are unavailable. |

The strict publication gate is **not passed**. The live judged score recorded
in the evidence is **5/12**; the **5–8/12** range is a forecast, not a new
judge result.

## What the paper proposes

PRISM combines polynomial fitting with randomized iterative sketching to adapt
matrix-function iterations to the spectrum observed at runtime, without
requiring explicit spectral or singular-value bounds. The paper discusses
matrix sign, square-root, inverse-root, inverse, and Chebyshev-style uses, and
reports applications to Shampoo and Muon training.

This repository tests those statements at the level supported by the public
source. It keeps theorem counterexamples, mechanism certificates, blocked
experiment audits, and historical evidence separate.

## Claim-to-evidence map

### C1 — adaptive polynomial mechanism

Produced by:

- `repro/src/dense_prism_certificate.py`: direct dense objective minimization
  versus an independently reconstructed residual-eigenvalue quartic;
- `repro/src/spectral_prism.py`: singular-value-coordinate path covering the
  paper's larger dimension regimes;
- `release/space_candidate/evidence/claim1/`: raw results, checker output,
  method, limitations, and negative control.

Observed result: 12 dense samples, 60 states, 52 identifiable coefficient
comparisons, maximum coefficient discrepancy `1.81e-8`, next-residual
discrepancy `8.88e-16`, and nine distinct adaptive profiles. A fixed-coefficient
negative control fails as intended.

### C2 — printed Theorem 1

Produced by `repro/src/theorem_counterexample.py` and independently checked by
`repro/src/check_theorem_counterexample.py`.

The exact matrix

```text
A = [[0, -1],
     [1,  0]]
```

has `||A||₂ = 1` and symmetric `A² = -I`, satisfying the printed assumptions.
Exact rational iteration produces residual norms `2, 5, 50, 33125`; the
corresponding printed bounds include `2` and `4`. The claim is therefore
marked `FALSIFIED_AS_PRINTED`, without asserting anything about a stronger
unstated positive-semidefinite assumption.

### C3 — printed Theorem 2

Produced by the same exact counterexample plus its sketch-independence
argument and checker. Since the residual matrix is a scalar multiple of the
identity, an oblivious sketch multiplies the alpha objective by a positive
random scalar and cannot change its minimizer. The theorem's convergence
guarantee fails on the same stated-domain matrix with probability one. The
arithmetic-cost statement is not separately falsified here.

### C4 — Shampoo/ResNet experiment

Produced by `repro/src/training_claims_closure.py` and
`repro/src/check_training_claims_closure.py` through four routes: source audit,
artifact audit, CPU feasibility lower bounds, and assumption-matching
falsification. The exact Shampoo implementation, model/data protocol, seeds,
raw curves, and timing setup are not public in sufficient detail. The result
is `BLOCKED`; CPU feasibility numbers are explicitly not proxies.

### C5 — Muon/GPT-2-Large experiment

Produced by the same training-claims closure and checker. The reported losses
cannot be independently generated without the exact model, FineWeb ordering,
optimizer integration, checkpoints, seeds, and raw trajectories. An optimistic
CPU lower bound is recorded as a feasibility constraint only. The result is
`BLOCKED`.

### C6 — Gaussian/HTMP robustness experiment

Produced by `repro/src/claim6_falsification_audit.py` and
`repro/src/check_claim6_falsification.py`. The audit covers finite-generator
calibration, limiting-density reconstruction, archive completeness, and a
mandatory assumption-matching falsification route. A reconstructed limiting
density that does not converge is not a falsification of the authors'
unpublished random draw, so the result remains `BLOCKED`.

## Reproduce the current audit

```bash
uv sync --frozen --python 3.11
uv run --frozen --python 3.11 python repro/src/run_reproduction.py
```

The runner is fail-closed. It executes the theorem counterexample, independent
checker and negative control, full-dimension and dense mechanism checks,
archive audit, Claim 6 audit, training-claims closure, and their negative
controls. The historical toy verifier is not part of this command.

The long or uncertain CPU routes were run with Hugging Face `cpu-upgrade`; the
repository does not present those feasibility runs as full-scale reproduction.

## Repository layout

- `repro/src/` — current executable audit and independent checkers.
- `.openresearch/artifacts/` — claim contracts, raw outputs, controls, and
  limitations used by the audit.
- `release/space_candidate/` — evaluator-visible evidence snapshot and static
  claim pages.
- `reports/prism-reproduction/report.md` — illustrated technical report.
- `notebooks/prism_claims.py` — self-contained notebook surface.
- `STATUS.md` — current verdict boundary and production paths.
- `BRANCH_AUDIT.md` — old-to-new branch names and branch roles.
- `SOURCE_MANIFEST.md` — paper version, source boundaries, citation, and thanks.
- `repro/src/verify_prism.py` — historical rejected 6×6 toy/proxy verifier;
  retained only for provenance and excluded from the current gate.

## Branch map

The repository's former `orx/` branches are renamed to the clean `research/`
namespace. `main` is the reader-facing publication surface. The independent
dense branch is retained because it is genuinely divergent work rather than a
stale ancestor; its role and relationship to `main` are recorded in
`BRANCH_AUDIT.md`.

| Clean branch | Role |
| --- | --- |
| `main` | Publication surface and current gate. |
| `research/judged-5-of-12-baseline` | Frozen historical judged baseline and locked environment. |
| `research/intended-domain-theorem-certificate` | Baseline branch for the intended-domain theorem audit. |
| `research/stated-domain-theorem-counterexamples` | Exact assumptions and rational Theorem 1–2 counterexamples. |
| `research/efficient-dense-prism-mechanism-certificate` | Dense mechanism certificate and independent quartic check. |
| `research/full-dimension-spectral-prism-reconstruction` | Full-dimension singular-value-coordinate reconstruction. |
| `research/dense-scaled-prism-reconstruction` | Divergent independent dense reconstruction; retained for lineage. |
| `research/calibrated-full-size-convergence-horizons` | Calibration of finite HTMP sampler interpretations. |
| `research/limiting-density-htmp-reconstruction` | Limiting-density HTMP reconstruction. |
| `research/htmp-archival-reproducibility-audit` | Archive/source completeness audit for Claim 6. |
| `research/claim-6-mandatory-falsification-route` | Assumption-matching Claim 6 falsification route. |
| `research/claims-4-and-5-four-route-closure` | Four-route closure for the two training claims. |
| `research/integrated-evaluator-visible-candidate` | Cumulative evaluator-visible candidate. |
| `research/publication-ready-report-and-space-surface` | Final report and static Space surface before `main`. |

## Citation

```bibtex
@article{yang2026prism,
  title={PRISM: Distribution-free Adaptive Computation of Matrix Functions for Accelerating Neural Network Training},
  author={Yang, Shenghao and Wang, Zhichao and Balabanov, Oleg and Erichson, N. Benjamin and Mahoney, Michael W.},
  journal={arXiv preprint arXiv:2601.22137},
  year={2026},
  doi={10.48550/arXiv.2601.22137}
}
```

## Thank you

Thank you to Shenghao Yang, Zhichao Wang, Oleg Balabanov, N. Benjamin
Erichson, and Michael W. Mahoney for making the PRISM paper available for
independent study. This repository is an independent reproducibility audit; it
does not represent the authors' implementation, approval, or endorsement.

## Related files

- [Technical report](reports/prism-reproduction/report.md)
- [Current evaluator-visible verification](release/space_candidate/pages/current-verification/page.md)
- [Source manifest](SOURCE_MANIFEST.md)
- [Status](STATUS.md)
- [Branch audit](BRANCH_AUDIT.md)
