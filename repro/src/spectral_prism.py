"""Full-dimension, singular-value-coordinate reproduction for Claims 1 and 6.

The polar iterations are unitarily invariant: if A = U diag(s) V.T, every
odd polynomial update changes only ``s``.  This lets us reproduce the paper's
exact matrix dimensions without allocating its 100000 x 2000 dense matrix.
It does not reproduce dense GEMM wall-clock time.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

import numpy as np
from scipy.linalg import eigvalsh_tridiagonal


SEEDS = (202601, 202602, 202603)
HORIZON = 24
THRESHOLDS = (1e-1, 1e-2, 1e-3)
ALPHA_BOUNDS = (3 / 8, 29 / 20)
POLAR_EXPRESS_SOURCE_SHA = "6f1bb73a2e1b724c92f90303845c045e7d32c892"


@dataclass(frozen=True)
class Condition:
    family: str
    parameter: float
    n: int
    m: int


CONDITIONS = (
    Condition("gaussian", 1.0, 15_000, 15_000),
    Condition("gaussian", 4.0, 20_000, 5_000),
    Condition("gaussian", 50.0, 100_000, 2_000),
    Condition("htmp", 0.1, 8_000, 4_000),
    Condition("htmp", 0.5, 8_000, 4_000),
    Condition("htmp", 100.0, 8_000, 4_000),
)


def optimal_quintic(lower: float, upper: float) -> tuple[float, float, float]:
    """PolarExpress's simplified Remez solver, reconstructed from its source."""
    if 1 - 5e-6 <= lower / upper:
        return (
            (15 / 8) / upper,
            (-10 / 8) / upper**3,
            (3 / 8) / upper**5,
        )
    q = (3 * lower + upper) / 4
    r = (lower + 3 * upper) / 4
    error = math.inf
    old_error = None
    while old_error is None or abs(old_error - error) > 1e-15:
        old_error = error
        lhs = np.array(
            [
                [lower, lower**3, lower**5, 1],
                [q, q**3, q**5, -1],
                [r, r**3, r**5, 1],
                [upper, upper**3, upper**5, -1],
            ],
            dtype=np.float64,
        )
        a, b, c, error = np.linalg.solve(lhs, np.ones(4))
        discriminant = math.sqrt(9 * b**2 - 20 * a * c)
        q, r = np.sqrt(
            (-3 * b + np.array([-1.0, 1.0]) * discriminant) / (10 * c)
        )
    return float(a), float(b), float(c)


def polar_express_coefficients(iterations: int = 10) -> list[tuple[float, ...]]:
    """Exact defaults from NoahAmsel/PolarExpress at the recorded source SHA."""
    lower = 1e-3
    upper = 1.0
    safety_factor = 1.01
    cushion = 0.02
    coefficients: list[tuple[float, ...]] = []
    for iteration in range(iterations):
        a, b, c = optimal_quintic(max(lower, cushion * upper), upper)
        if cushion * upper > lower:
            p_lower = a * lower + b * lower**3 + c * lower**5
            p_upper = a * upper + b * upper**3 + c * upper**5
            rescaler = 2 / (p_lower + p_upper)
            a, b, c = a * rescaler, b * rescaler, c * rescaler
        if iteration < iterations - 1:
            a /= safety_factor
            b /= safety_factor**3
            c /= safety_factor**5
        coefficients.append((float(a), float(b), float(c)))
        lower = a * lower + b * lower**3 + c * lower**5
        upper = 2 - lower
    return coefficients


def beta_laguerre_singular_values(
    condition: Condition, seed: int
) -> tuple[np.ndarray, dict[str, float | str]]:
    """Sample the real beta-Laguerre ensemble in PSD tridiagonal form.

    For Gaussian matrices beta=1.  For HTMP, beta=kappa/m.  The printed
    Algorithm 2 of Hodgkinson et al. uses d_i*t_i off diagonal; that indexing
    is inconsistent with its own diagonal and is not PSD.  The bidiagonal
    product requires d_{i+1}*t_i, which is used here.
    """
    rng = np.random.default_rng(seed)
    beta = 1.0 if condition.family == "gaussian" else condition.parameter / condition.m
    d_df = beta * condition.n - beta * np.arange(condition.m)
    t_df = beta * (condition.m - 1 - np.arange(condition.m - 1))
    if np.min(d_df) <= 0 or np.min(t_df) <= 0:
        raise ValueError("invalid beta-Laguerre chi degrees")
    diagonal_chi = np.sqrt(rng.chisquare(d_df))
    off_diagonal_chi = np.sqrt(rng.chisquare(t_df))
    diagonal = diagonal_chi**2
    diagonal[:-1] += off_diagonal_chi**2
    off_diagonal = diagonal_chi[1:] * off_diagonal_chi
    eigenvalues = eigvalsh_tridiagonal(
        diagonal,
        off_diagonal,
        select="a",
        check_finite=True,
        lapack_driver="sterf",
    )
    tolerance = 1e-10 * max(1.0, float(eigenvalues[-1]))
    if float(eigenvalues[0]) < -tolerance:
        raise ArithmeticError("PSD beta-Laguerre construction has negative eigenvalue")
    eigenvalues = np.maximum(eigenvalues, 0.0)
    singular_values = np.sqrt(eigenvalues)
    frobenius = float(np.linalg.norm(singular_values))
    if frobenius == 0:
        raise ArithmeticError("zero beta-Laguerre sample")
    singular_values /= frobenius
    audit = {
        "beta": beta,
        "minimum_eigenvalue_before_clipping": float(eigenvalues[0]),
        "maximum_eigenvalue": float(eigenvalues[-1]),
        "normalization": "singular values divided by Frobenius norm",
    }
    return singular_values, audit


def residual_error(singular_values: np.ndarray) -> tuple[float, float]:
    residual = 1 - singular_values**2
    return float(np.linalg.norm(residual)), float(np.sqrt(np.mean(residual**2)))


def bounded_prism_alpha(
    singular_values: np.ndarray,
    weights: np.ndarray | None = None,
) -> tuple[float, dict[str, float | bool]]:
    """Globally minimize the exact quartic residual loss on ALPHA_BOUNDS."""
    if weights is None:
        weights = np.ones_like(singular_values)
    squared = singular_values**2
    residual = 1 - squared
    base = 1 + 0.5 * residual
    direction = residual**2
    c0 = 1 - squared * base**2
    c1 = -2 * squared * base * direction
    c2 = -squared * direction**2
    coefficients = np.array(
        [
            np.sum(weights * c0**2),
            np.sum(weights * 2 * c0 * c1),
            np.sum(weights * (c1**2 + 2 * c0 * c2)),
            np.sum(weights * 2 * c1 * c2),
            np.sum(weights * c2**2),
        ],
        dtype=np.float64,
    )
    derivative = np.arange(1, 5, dtype=np.float64) * coefficients[1:]
    roots = np.polynomial.polynomial.polyroots(derivative)
    candidates = [ALPHA_BOUNDS[0], ALPHA_BOUNDS[1]]
    candidates.extend(
        float(root.real)
        for root in roots
        if abs(root.imag) < 1e-9 and ALPHA_BOUNDS[0] <= root.real <= ALPHA_BOUNDS[1]
    )

    def objective(alpha: float) -> float:
        return float(np.polynomial.polynomial.polyval(alpha, coefficients))

    alpha = min(candidates, key=objective)
    grid = np.linspace(*ALPHA_BOUNDS, 1001)
    grid_best = float(np.min(np.polynomial.polynomial.polyval(grid, coefficients)))
    optimality_gap = max(0.0, objective(alpha) - grid_best)
    return alpha, {
        "objective": objective(alpha),
        "grid_upper_bound": grid_best,
        "optimality_gap": optimality_gap,
        "within_bounds": ALPHA_BOUNDS[0] <= alpha <= ALPHA_BOUNDS[1],
    }


def trajectory(
    initial: np.ndarray, method: str, horizon: int = HORIZON
) -> tuple[list[dict[str, float | int | str | None]], list[dict[str, float | bool]]]:
    singular_values = initial.astype(np.float64, copy=True)
    if method == "polar_express":
        singular_values /= 1.01 + 1e-7
    coefficients = polar_express_coefficients()
    rows: list[dict[str, float | int | str | None]] = []
    audits: list[dict[str, float | bool]] = []
    for iteration in range(horizon + 1):
        error_fro, error_rms = residual_error(singular_values)
        rows.append(
            {
                "method": method,
                "iteration": iteration,
                "error_fro": error_fro,
                "error_rms": error_rms,
                "alpha": None,
            }
        )
        if iteration == horizon:
            break
        if method == "prism":
            alpha, audit = bounded_prism_alpha(singular_values)
            residual = 1 - singular_values**2
            singular_values *= 1 + 0.5 * residual + alpha * residual**2
            rows[-1]["alpha"] = alpha
            audits.append(audit)
        elif method == "newton_schulz":
            residual = 1 - singular_values**2
            singular_values *= 1 + 0.5 * residual + (3 / 8) * residual**2
        elif method == "polar_express":
            a, b, c = coefficients[min(iteration, len(coefficients) - 1)]
            singular_values = (
                a * singular_values
                + b * singular_values**3
                + c * singular_values**5
            )
        else:
            raise ValueError(f"unknown method: {method}")
        if not np.all(np.isfinite(singular_values)):
            raise ArithmeticError(f"{method} produced a non-finite iterate")
    return rows, audits


def one_sample(task: tuple[Condition, int]) -> dict[str, object]:
    condition, seed = task
    started = time.perf_counter()
    singular_values, spectrum_audit = beta_laguerre_singular_values(condition, seed)
    rows: list[dict[str, object]] = []
    optimizer_audits: list[dict[str, float | bool]] = []
    for method in ("prism", "newton_schulz", "polar_express"):
        method_rows, method_audits = trajectory(singular_values, method)
        for row in method_rows:
            row.update(
                {
                    "family": condition.family,
                    "parameter": condition.parameter,
                    "n": condition.n,
                    "m": condition.m,
                    "seed": seed,
                }
            )
        rows.extend(method_rows)
        if method == "prism":
            optimizer_audits.extend(method_audits)
    return {
        "condition": condition.__dict__,
        "seed": seed,
        "spectrum_audit": spectrum_audit,
        "alpha_audit": {
            "all_within_bounds": all(
                bool(item["within_bounds"]) for item in optimizer_audits
            ),
            "maximum_grid_optimality_gap": max(
                float(item["optimality_gap"]) for item in optimizer_audits
            ),
        },
        "runtime_seconds": time.perf_counter() - started,
        "rows": rows,
    }


def first_hit(rows: list[dict[str, object]], threshold: float) -> int | None:
    hits = [
        int(row["iteration"])
        for row in rows
        if float(row["error_rms"]) <= threshold
    ]
    return min(hits) if hits else None


def summarize(samples: list[dict[str, object]]) -> dict[str, object]:
    flat_rows = [row for sample in samples for row in sample["rows"]]
    first_hits: list[dict[str, object]] = []
    for sample in samples:
        sample_rows = sample["rows"]
        condition = sample["condition"]
        for method in ("prism", "newton_schulz", "polar_express"):
            method_rows = [row for row in sample_rows if row["method"] == method]
            record: dict[str, object] = {
                **condition,
                "seed": sample["seed"],
                "method": method,
            }
            for threshold in THRESHOLDS:
                record[f"first_hit_rms_{threshold:g}"] = first_hit(
                    method_rows, threshold
                )
            first_hits.append(record)

    stability: dict[str, dict[str, float | int | None]] = {}
    for method in ("prism", "newton_schulz", "polar_express"):
        values = [
            item["first_hit_rms_0.01"]
            for item in first_hits
            if item["method"] == method and item["first_hit_rms_0.01"] is not None
        ]
        stability[method] = {
            "reached_count": len(values),
            "total_count": len(CONDITIONS) * len(SEEDS),
            "minimum": min(values) if values else None,
            "maximum": max(values) if values else None,
            "range": max(values) - min(values) if values else None,
            "mean": float(np.mean(values)) if values else None,
            "sample_std": float(np.std(values, ddof=1)) if len(values) > 1 else None,
        }
    paired = []
    for prism in (item for item in first_hits if item["method"] == "prism"):
        polar = next(
            item
            for item in first_hits
            if item["method"] == "polar_express"
            and item["family"] == prism["family"]
            and item["parameter"] == prism["parameter"]
            and item["seed"] == prism["seed"]
        )
        prism_hit = prism["first_hit_rms_0.01"]
        polar_hit = polar["first_hit_rms_0.01"]
        paired.append(
            {
                "family": prism["family"],
                "parameter": prism["parameter"],
                "seed": prism["seed"],
                "prism": prism_hit,
                "polar_express": polar_hit,
                "prism_no_slower": prism_hit is not None
                and (polar_hit is None or prism_hit <= polar_hit),
            }
        )
    claim6_aligned = (
        stability["prism"]["reached_count"] == len(CONDITIONS) * len(SEEDS)
        and all(item["prism_no_slower"] for item in paired)
        and (
            stability["polar_express"]["reached_count"]
            < stability["polar_express"]["total_count"]
            or stability["prism"]["range"] < stability["polar_express"]["range"]
        )
    )
    distinct_alpha_profiles = len(
        {
            tuple(
                round(float(row["alpha"]), 8)
                for row in sample["rows"]
                if row["method"] == "prism" and row["alpha"] is not None
            )
            for sample in samples
        }
    )
    return {
        "first_hits": first_hits,
        "stability": stability,
        "paired_prism_vs_polar_express": paired,
        "claim1_mechanism": {
            "polynomial": "g_2(R; alpha) = I + 1/2 R + alpha R^2",
            "fit_target": "eigenvalues of R = I - X^T X",
            "uses_explicit_spectral_bound": False,
            "distinct_alpha_profiles": distinct_alpha_profiles,
            "all_alpha_global_grid_checks_pass": all(
                sample["alpha_audit"]["all_within_bounds"]
                and sample["alpha_audit"]["maximum_grid_optimality_gap"] <= 1e-8
                for sample in samples
            ),
        },
        "claim6_scoped_alignment": claim6_aligned,
        "rows": flat_rows,
    }


def literal_sampler_negative_control() -> int:
    """The printed HTMP off-diagonal must fail the PSD invariant."""
    condition = Condition("htmp", 0.1, 200, 100)
    rng = np.random.default_rng(202601)
    beta = condition.parameter / condition.m
    d = np.sqrt(
        rng.chisquare(beta * condition.n - beta * np.arange(condition.m))
    )
    t = np.sqrt(
        rng.chisquare(beta * (condition.m - 1 - np.arange(condition.m - 1)))
    )
    diagonal = d**2
    diagonal[:-1] += t**2
    literal_off_diagonal = d[:-1] * t
    eigenvalues = eigvalsh_tridiagonal(
        diagonal, literal_off_diagonal, lapack_driver="sterf"
    )
    result = {
        "schema": "htmp-printed-index-negative-control-v1",
        "minimum_eigenvalue": float(eigenvalues[0]),
        "negative_eigenvalue_count": int(np.sum(eigenvalues < -1e-12)),
        "expected_invariant": "Laguerre beta ensemble is positive semidefinite",
    }
    print("HTMP_LITERAL_NEGATIVE_CONTROL=" + json.dumps(result, sort_keys=True))
    return 9 if result["negative_eigenvalue_count"] > 0 else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        return literal_sampler_negative_control()

    started = time.perf_counter()
    tasks = [(condition, seed) for condition in CONDITIONS for seed in SEEDS]
    affinity = (
        len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else 1
    )
    workers = min(6, affinity, len(tasks))
    with ProcessPoolExecutor(max_workers=workers) as executor:
        samples = list(executor.map(one_sample, tasks))
    summary = summarize(samples)
    payload = {
        "schema": "prism-full-dimension-spectral-v1",
        "paper_dimensions": True,
        "paper_float32_replaced_by": "float64 spectral-coordinate arithmetic",
        "dense_wall_clock_reproduced": False,
        "seeds": list(SEEDS),
        "horizon": HORIZON,
        "thresholds": list(THRESHOLDS),
        "alpha_bounds": list(ALPHA_BOUNDS),
        "polar_express_source_sha": POLAR_EXPRESS_SOURCE_SHA,
        "worker_processes": workers,
        "logical_cpu_affinity": affinity,
        "runtime_seconds": time.perf_counter() - started,
        **summary,
    }
    mechanism = payload["claim1_mechanism"]
    if not mechanism["all_alpha_global_grid_checks_pass"]:
        print("PRISM_ALPHA_OPTIMALITY_CHECK_FAILED")
        return 3
    if mechanism["distinct_alpha_profiles"] < 4:
        print("PRISM_SPECTRUM_ADAPTATION_CONTROL_FAILED")
        return 4
    print("SPECTRAL_RESULT=" + json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
