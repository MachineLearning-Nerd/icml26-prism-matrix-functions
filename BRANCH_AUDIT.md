# Branch audit

This audit records the research history before the repository cleanup. The
former `orx/` namespace came from the experiment runner; it is renamed to the
clean `research/` namespace. The publication branch is renamed from `master`
to `main`.

| Former branch | Clean branch | Tip before cleanup | Relationship to old `master` | What it does |
| --- | --- | --- | --- | --- |
| `master` | `main` | `887ae0c` | Publication tip | Reader-facing README, report, notebook, current evidence, and gate metadata. |
| `orx/judged-5-of-12-baseline` | `research/judged-5-of-12-baseline` | `f65e4dc` | Ancestor | Freezes the judged 6×6 baseline and the locked Python environment. |
| `orx/intended-domain-theorem-certificate` | `research/intended-domain-theorem-certificate` | `f65e4dc` | Ancestor | Baseline node for the intended-domain theorem audit; it shares the frozen baseline tip. |
| `orx/stated-domain-theorem-counterexamples` | `research/stated-domain-theorem-counterexamples` | `592a809` | Ancestor | Records the exact stated-domain policy and introduces the rational Theorem 1–2 counterexamples. |
| `orx/efficient-dense-prism-mechanism-certificate` | `research/efficient-dense-prism-mechanism-certificate` | `e04018a` | Ancestor | Adds the direct dense mechanism certificate and independent quartic comparison. |
| `orx/full-dimension-spectral-prism-reconstruction` | `research/full-dimension-spectral-prism-reconstruction` | `f908a3f` | Ancestor | Adds the full-dimension singular-value-coordinate reconstruction. |
| `orx/dense-scaled-prism-reconstruction` | `research/dense-scaled-prism-reconstruction` | `efb9372` | **Divergent** | Adds an independent dense PRISM reconstruction and its own route contracts. Preserved because it is not contained in the publication tip. |
| `orx/calibrated-full-size-convergence-horizons` | `research/calibrated-full-size-convergence-horizons` | `2a14d25` | Ancestor | Calibrates finite HTMP sampler interpretations and convergence horizons. |
| `orx/limiting-density-htmp-reconstruction` | `research/limiting-density-htmp-reconstruction` | `275bd0c` | Ancestor | Reconstructs a limiting HTMP density for a Claim 6 stress test. |
| `orx/htmp-archival-reproducibility-audit` | `research/htmp-archival-reproducibility-audit` | `3851c25` | Ancestor | Audits the paper archive and records missing Claim 6 source artifacts. |
| `orx/claim-6-mandatory-falsification-route` | `research/claim-6-mandatory-falsification-route` | `a1ca7bf` | Ancestor | Adds the assumption-matching Claim 6 falsification route and rejects an invalid substitute counterexample. |
| `orx/claims-4-and-5-four-route-closure` | `research/claims-4-and-5-four-route-closure` | `5961825` | Ancestor | Closes Claims 4–5 with source, artifact, feasibility, and falsification routes. |
| `orx/integrated-evaluator-visible-candidate` | `research/integrated-evaluator-visible-candidate` | `8fcf992` | Ancestor | Integrates the fail-closed claim ledger and evaluator-visible evidence surface. |
| `orx/publication-ready-report-and-space-surface` | `research/publication-ready-report-and-space-surface` | `887ae0c` | Publication tip | Adds the technical report, static Space candidate, and final result-schema correction. |

## Cleanup policy

- `main` is the only default publication branch.
- Every former `orx/` branch receives a descriptive `research/` name so the
  experiment lineage remains inspectable.
- No divergent branch is deleted merely because it is not part of `main`.
- The old names, tips, and roles remain documented here after the remote rename.
- The current runner does not execute the historical 6×6 toy verifier.
