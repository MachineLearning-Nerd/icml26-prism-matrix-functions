# Claim 6 — Gaussian and HTMP robustness

## Exact contract

Section 6.1, Figures 3–4, and Appendix D report the authors' degree-5
experiments on Gaussian shapes `15000×15000`, `20000×5000`, `100000×2000`
(`n/m∈{1,4,50}`) and HTMP `8000×4000` matrices with
`κ∈{0.1,0.5,100}`. The source says adaptive PRISM converges fastest in those
experiments and describes its speed as stable relative to PolarExpress.

Source: arXiv:2601.22137 HTML retrieved 2026-07-24, SHA-256
`9876b930c97063af87fbfc8eb51e577920d2047d76abd4f71c1f63570b9a4866`.

The paper publishes float32/A100 plots but no raw table, seed, executable,
practical sketch dimension, stopping rule, or exact HTMP draw.

## Four routes and result

**BLOCKED — LOW confidence.**

1. Five defensible finite HTMP parameter mappings were calibrated against all
   six plot anchors; none reproduced them all.
2. Direct limiting-density quadrature yielded a deterministic `κ=.1` spectrum
   with Frobenius residual `9.1957` at iteration 32.
3. The exact arXiv archive (SHA-256
   `2567d8a2378a09a18f1bd8dbd645a5785a1a2bd89af5458c1410a0b383483e4d`)
   contains 50 files and four required plots, but no executable, raw curve
   data, or seed.
4. The falsification route bounds the smallest singular value after 32 steps
   by `3.3047e-22`, contradicting a universalized stability statement. It is
   not a valid falsification of the exact particular-experiment wording because
   the unpublished random draw and A100 timing assumptions are unmatched.

The independent checker passes. An exact-zero-singular-value counterexample is
rejected because it violates positive HTMP support.

- [Falsification verifier](/code/claim6_falsification_audit.py)
- [Independent checker](/code/check_claim6_falsification.py)
- [Finite calibration route](/code/htmp_calibration.py)
- [Limiting-density route](/code/htmp_limiting_density.py)
- [Archive route](/code/audit_arxiv_reproducibility.py)
- [Contract](/evidence/claim6/claim_contract.json)
- [Raw summary](/evidence/claim6/raw_result.json)
- [Checker output](/evidence/claim6/checker_output.txt)
- [Negative control](/evidence/claim6/negative_control_output.txt)

Unblocker: exact generator/executable, random seeds or matrices, sketch
dimension, raw curves, precision/timing protocol, and original wall-clock data.
