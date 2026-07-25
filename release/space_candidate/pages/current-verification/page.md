# Current verification

This is the evaluator entrypoint for commit `8fcf992` and cumulative HF
`cpu-upgrade` run `e4e9a9cb-ecf6-4b09-8115-f75845800d12`.

Fixed command:

```text
uv run --frozen --python 3.11 python repro/src/run_reproduction.py
```

Pinned environment: Python 3.11 and the bundled
[`pyproject.toml`](/environment/pyproject.toml) +
[`uv.lock`](/environment/uv.lock). Pre-run estimate: six worker cores and
2–3 minutes. Actual: 64 logical CPUs visible, six worker processes requested,
248.763 seconds of runner time, 4m47s total HF job duration.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Claim 1](#/claim-1) | [verifier](/code/dense_prism_certificate.py) | yes | [JSON](/evidence/claim1/raw_result.json) | [output](/evidence/claim1/checker_output.txt) | [output](/evidence/claim1/negative_control_output.txt) | yes | VERIFIED |
| 2 | [Claim 2](#/claim-2) | [verifier](/code/theorem_counterexample.py) | yes | [JSON](/evidence/claim2/raw_result.json) | [output](/evidence/claim2/checker_output.txt) | [output](/evidence/claim2/negative_control_output.txt) | yes | FALSIFIED |
| 3 | [Claim 3](#/claim-3) | [verifier](/code/theorem_counterexample.py) | yes | [JSON](/evidence/claim3/raw_result.json) | [output](/evidence/claim2/checker_output.txt) | [output](/evidence/claim3/negative_control_output.txt) | yes | FALSIFIED |
| 4 | [Claim 4](#/claim-4) | [verifier](/code/training_claims_closure.py) | yes | [JSON](/evidence/claim4/raw_result.json) | [output](/evidence/claim4/checker_output.txt) | [output](/evidence/claim4/negative_control_output.txt) | yes | BLOCKED |
| 5 | [Claim 5](#/claim-5) | [verifier](/code/training_claims_closure.py) | yes | [JSON](/evidence/claim5/raw_result.json) | [output](/evidence/claim5/checker_output.txt) | [output](/evidence/claim5/negative_control_output.txt) | yes | BLOCKED |
| 6 | [Claim 6](#/claim-6) | [verifier](/code/claim6_falsification_audit.py) | yes | [JSON](/evidence/claim6/raw_result.json) | [output](/evidence/claim6/checker_output.txt) | [output](/evidence/claim6/negative_control_output.txt) | yes | BLOCKED |

Every current verifier has an explicit nonzero failure path. For BLOCKED
routes, the cumulative runner requires the designated route exit code `8`,
checker exit code `0`, and mutation exit code `9`.

The old page titled “Verification run” is a **Historical rejected baseline**.
It is superseded by the code and revision linked above.
