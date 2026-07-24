"""Exact proof certificate falsifying the stated domains of Theorems 1 and 2.

All arithmetic in the counterexample trajectory is rational. No sampled
matrix, tolerance, or fitted threshold is used.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / ".openresearch/artifacts/claim2/counterexample.json"


def h(residual: Fraction, alpha: Fraction) -> Fraction:
    """Scalar residual recurrence from Appendix B.2/B.3."""
    return 1 - (1 - residual) * (1 + alpha * residual) ** 2


def main() -> int:
    certificate = json.loads(CERTIFICATE.read_text())
    alpha = Fraction(1, 2)
    residuals = [Fraction(2)]
    for _ in range(3):
        residuals.append(h(residuals[-1], alpha))

    n = certificate["theorem_2_parameters"]["n"]
    delta = certificate["theorem_2_parameters"]["delta"]
    horizon = certificate["theorem_2_parameters"]["k"]
    p_min = math.ceil(
        48
        * (
            math.log(n)
            + math.log(1 / delta)
            + math.log(horizon)
            + 27.6
        )
    )

    result = {
        "schema": "prism-stated-domain-counterexample-v1",
        "matrix_A": [[0, -1], [1, 0]],
        "assumptions": {
            "dimension": 2,
            "spectral_norm_A": 1,
            "spectral_norm_positive": True,
            "spectral_norm_at_most_one": True,
            "A_squared": [[-1, 0], [0, -1]],
            "A_squared_symmetric": True,
            "degree": 1,
            "alpha_interval": ["1/2", "1"],
        },
        "alpha_star_each_checked_step": "1/2",
        "residual_spectral_norms": [int(value) for value in residuals],
        "theorem_1": {
            "checked_k": 2,
            "actual": int(residuals[2]),
            "claimed_bound": 2,
            "contradiction": residuals[2] > 2,
            "verdict": "FALSIFIED",
        },
        "theorem_2": {
            "checked_k": 3,
            "statement_p_min": p_min,
            "actual": int(residuals[3]),
            "claimed_bound": 2,
            "failure_probability": 1.0,
            "allowed_failure_probability": delta,
            "contradiction": residuals[3] > 2 and 1.0 > delta,
            "verdict": "FALSIFIED",
        },
        "non_circularity": {
            "formula_derived_sample_used_as_evidence": False,
            "sampled_sketch_used_as_evidence": False,
            "reason": "For R=rI, the sketched objective is |h(r,alpha)| times ||S||_F, so every nonzero sketch has the same minimizer. A Gaussian sketch is nonzero almost surely.",
        },
    }

    expected = json.loads(
        (ROOT / ".openresearch/artifacts/claim2/raw_result.json").read_text()
    )
    if result != expected:
        print("COUNTEREXAMPLE_RESULT_MISMATCH")
        print(json.dumps(result, sort_keys=True))
        return 2
    if not result["theorem_1"]["contradiction"]:
        return 3
    if not result["theorem_2"]["contradiction"]:
        return 4
    print("COUNTEREXAMPLE_RESULT=" + json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
