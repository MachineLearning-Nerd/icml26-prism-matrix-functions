# Evaluator-blind pre-publication review

Review scope: only the downloaded candidate and the evaluator rubric. No
OpenResearch logs, unpublished branches, or repository context may fill gaps.

Files opened in order:

1. `README.md`
2. `pages/current-verification/page.md`
3. each `pages/claim-N/page.md`
4. each linked contract, raw JSON, checker output, and control output
5. each linked executable
6. `environment/pyproject.toml` and `environment/uv.lock`
7. `pages/release-report/page.md`

Conclusions:

- The current verifier is discoverable before the Historical rejected baseline.
- Every claim exposes its exact contract, assumptions, command, code, inline
  result, raw result, checker, control, limitation, revision, seed policy, and
  CPU/runtime record.
- Claims 4–6 remain discoverably BLOCKED; no proxy is labeled verification.
- No conclusion required hidden project knowledge.

The review must be repeated against the exact downloaded published revision.
