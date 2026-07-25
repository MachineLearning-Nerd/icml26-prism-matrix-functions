"""Mandatory falsification attempt for the exact Claim 6 source statement."""

from __future__ import annotations

import argparse
import json
import math


SOURCE_STATEMENT = (
    "Automatically adapting to the input spectra allows PRISM to converge "
    "the fastest in our experiments."
)
MINIMUM_MIDPOINT_EIGENVALUE = 4.91038285729026e-72
MAXIMUM_MIDPOINT_EIGENVALUE = 52.65631250687386
OBSERVED_ERROR_AT_32 = 9.195665798079629
ALPHA_UPPER = 29 / 20
HORIZON = 32


def candidate() -> dict[str, object]:
    # For 0 <= s <= 1 and 0 <= r=1-s^2 <= 1, every PRISM step multiplies
    # s by at most 1 + r/2 + (29/20)r^2 <= 2.95.
    maximum_step_amplification = 1 + 0.5 + ALPHA_UPPER
    normalized_minimum_singular_upper_bound = math.sqrt(
        MINIMUM_MIDPOINT_EIGENVALUE / MAXIMUM_MIDPOINT_EIGENVALUE
    )
    singular_upper_bound_at_horizon = (
        normalized_minimum_singular_upper_bound
        * maximum_step_amplification**HORIZON
    )
    residual_lower_bound_at_horizon = (
        1 - singular_upper_bound_at_horizon**2
    )
    assumptions = {
        "matrix_dimensions_8000_by_4000": True,
        "kappa_equals_0.1": True,
        "named_limiting_HTMP_density_E5": True,
        "fifth_order_PRISM_alpha_in_bounds": True,
        "random_matrix_draw_matching_unpublished_sample": False,
        "paper_float32_A100_wall_clock": False,
    }
    return {
        "schema": "claim6-falsification-candidate-v1",
        "exact_source_statement": SOURCE_STATEMENT,
        "source_quantifier": "the particular unpublished experiments",
        "candidate": (
            "deterministic midpoint-quantile spectrum of the cited limiting "
            "HTMP density at gamma=0.5, kappa=0.1, m=4000"
        ),
        "candidate_run_id": "b9dc5832-7883-4ad0-8701-a3fdbe387d6e",
        "candidate_observed_error_fro_at_iteration_32": OBSERVED_ERROR_AT_32,
        "maximum_step_amplification": maximum_step_amplification,
        "normalized_minimum_singular_upper_bound": (
            normalized_minimum_singular_upper_bound
        ),
        "singular_upper_bound_at_iteration_32": singular_upper_bound_at_horizon,
        "residual_lower_bound_at_iteration_32": residual_lower_bound_at_horizon,
        "candidate_contradicts_universalized_stability_statement": (
            residual_lower_bound_at_horizon > 1e-2
            and OBSERVED_ERROR_AT_32 > 1e-2
        ),
        "assumption_audit": assumptions,
        "satisfies_every_source_assumption": all(assumptions.values()),
        "valid_falsification_of_exact_source_statement": False,
        "verdict": "BLOCKED",
        "reason": (
            "The source reports its particular experiments rather than a "
            "universal claim. The unpublished matrix draw and A100 timing "
            "cannot be contradicted by a different deterministic spectrum."
        ),
    }


def negative_control() -> int:
    result = {
        "schema": "claim6-falsification-negative-control-v1",
        "candidate": "matrix with an exact zero singular value",
        "contradicts_convergence": True,
        "satisfies_HTMP_positive_support": False,
        "valid_falsification": False,
    }
    print("CLAIM6_FALSIFICATION_NEGATIVE_CONTROL=" + json.dumps(result, sort_keys=True))
    return 9 if not result["valid_falsification"] else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        return negative_control()
    payload = candidate()
    print("CLAIM6_FALSIFICATION_AUDIT=" + json.dumps(payload, sort_keys=True))
    if not payload["valid_falsification_of_exact_source_statement"]:
        print("CLAIM6_FALSIFICATION_NOT_ESTABLISHED_BLOCKED")
        return 8
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
