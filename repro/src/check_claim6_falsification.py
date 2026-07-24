"""Independent checker for the Claim 6 falsification disposition."""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / ".openresearch/artifacts/claim6/falsification_candidate.json"


def main() -> int:
    payload = json.loads(PATH.read_text())
    expected_step = 1 + 0.5 + 29 / 20
    expected_s0 = math.sqrt(
        payload["minimum_midpoint_eigenvalue"]
        / payload["maximum_midpoint_eigenvalue"]
    )
    expected_sk = expected_s0 * expected_step ** payload["horizon"]
    expected_residual = 1 - expected_sk**2
    checks = {
        "amplification_exact": math.isclose(
            payload["maximum_step_amplification"], expected_step, rel_tol=0, abs_tol=1e-15
        ),
        "initial_bound_exact": math.isclose(
            payload["normalized_minimum_singular_upper_bound"],
            expected_s0,
            rel_tol=1e-14,
        ),
        "horizon_bound_exact": math.isclose(
            payload["singular_upper_bound_at_horizon"],
            expected_sk,
            rel_tol=1e-14,
        ),
        "nonconvergence_proved_for_candidate": expected_residual > 1e-2,
        "assumption_violation_recorded": not payload["assumptions"][
            "same_unpublished_random_draw"
        ],
        "source_not_universal": payload["source_quantifier"]
        == "particular unpublished experiments",
        "blocked_not_falsified": payload["verdict"] == "BLOCKED",
    }
    result = {
        "schema": "claim6-falsification-independent-check-v1",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    print("CLAIM6_FALSIFICATION_INDEPENDENT_CHECK=" + json.dumps(result, sort_keys=True))
    return 0 if result["all_checks_pass"] else 5


if __name__ == "__main__":
    raise SystemExit(main())
