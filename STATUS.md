# Reproduction status

Overall status: **INCONCLUSIVE — VERIFIED SCOPED FINDINGS WITH BLOCKED PAPER-LEVEL EXPERIMENTS**.

The current audit separates mathematical/mechanism checks from claims about
particular large training and robustness experiments. It does not convert a
toy result, a feasibility lower bound, or a reconstruction with different
random draws into a paper-level pass.

| Claim | Status | How the result is produced |
| --- | --- | --- |
| C1 — adaptive polynomial mechanism | `VERIFIED_SCOPED` | `repro/src/dense_prism_certificate.py` compares direct dense minimization with an independent spectral quartic; `spectral_prism.py` checks the full-dimension coordinate path. |
| C2 — printed Theorem 1 bound | `FALSIFIED_AS_PRINTED` | `repro/src/theorem_counterexample.py` and `check_theorem_counterexample.py` evaluate the exact rational matrix `[[0,-1],[1,0]]` and its residual sequence. |
| C3 — printed Theorem 2 sketching guarantee | `FALSIFIED_AS_PRINTED` | The same counterexample is sketch-independent because its residual objective is a scalar multiple of the identity; the independent checker verifies the failure path. |
| C4 — Shampoo/ResNet timing | `BLOCKED` | `repro/src/training_claims_closure.py` and its checker run source, artifact, feasibility, and falsification routes; missing model/data/integration/timing artifacts prevent a paper-level verdict. |
| C5 — Muon/GPT-2-Large loss comparison | `BLOCKED` | The same four-route closure records missing exact model/data/checkpoint/trajectory details and a CPU lower bound that is not a proxy. |
| C6 — Gaussian/HTMP robustness | `BLOCKED` | `repro/src/claim6_falsification_audit.py` and its checker audit calibration, limiting density, archive, and assumption-matching falsification routes; reconstructed draws do not identify the authors' unpublished run. |

The strict publication gate is **not passed**. The live judged score recorded
in the repository is `5/12`; the `5–8/12` range is only a forecast.

The old `repro/src/verify_prism.py` remains labeled as a historical rejected
toy verifier and is excluded from `run_reproduction.py`.
