"""Independent structural checker for the four-route training disposition."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / ".openresearch/artifacts/training_claims/closure_contract.json"


def main() -> int:
    contract = json.loads(PATH.read_text())
    checks = {
        "exactly_four_routes": contract["completed_routes"] == [1, 2, 3, 4],
        "three_before_falsification": contract["mandatory_falsification_after"] == 3,
        "claim4_blocked": contract["claim4"]["verdict"] == "BLOCKED",
        "claim5_blocked": contract["claim5"]["verdict"] == "BLOCKED",
        "claim4_not_falsified": not contract["claim4"]["valid_falsification"],
        "claim5_not_falsified": not contract["claim5"]["valid_falsification"],
        "claim4_unblocker_concrete": len(contract["claim4"]["unblockers"]) >= 4,
        "claim5_unblocker_concrete": len(contract["claim5"]["unblockers"]) >= 4,
    }
    result = {
        "schema": "training-claims-closure-independent-check-v1",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    print("TRAINING_CLAIMS_INDEPENDENT_CHECK=" + json.dumps(result, sort_keys=True))
    return 0 if result["all_checks_pass"] else 5


if __name__ == "__main__":
    raise SystemExit(main())
