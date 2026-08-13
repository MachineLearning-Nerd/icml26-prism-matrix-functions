# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_681ef1637360", "created_at": "2026-07-22T03:59:20+00:00", "title": "Executive summary"}
-->
## Executive summary

> **ARCHIVED REJECTED BASELINE.** The original snapshot reported 6/6 checks
> from a toy/proxy verifier. That result was not a paper-level reproduction.

The current audit has a split result: Claim 1 is `VERIFIED_SCOPED`; Claims 2–3
are `FALSIFIED_AS_PRINTED` on an exact stated-domain counterexample; and Claims
4–6 are `BLOCKED` because the published artifacts do not identify the exact
training and robustness runs. The strict publication gate is not passed.

## Scope & cost

| | This reproduction | Full replication |
|---|---|---|
| Scope | all claims, clean-room | same |
| Hardware | CPU (numpy) | same |
| Time | <1 min | same |
| Cost | $0 | $0 |
| Outcome | verified | — |
