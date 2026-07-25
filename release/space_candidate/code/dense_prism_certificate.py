"""Independent dense certificate for PRISM's spectrum-adaptive fit."""

from __future__ import annotations

import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass

import numpy as np
from scipy.optimize import minimize_scalar


ALPHA_BOUNDS = (3 / 8, 29 / 20)
SEEDS = (202601, 202602)
ITERATIONS = 5
INFORMATIVE_OBJECTIVE_FLOOR = 1e-12


@dataclass(frozen=True)
class DenseCondition:
    family: str
    parameter: float
    n: int
    m: int


CONDITIONS = (
    DenseCondition("gaussian", 1.0, 128, 128),
    DenseCondition("gaussian", 4.0, 256, 64),
    DenseCondition("gaussian", 50.0, 800, 16),
    DenseCondition("power_law_spectrum", 0.5, 128, 64),
    DenseCondition("power_law_spectrum", 1.0, 128, 64),
    DenseCondition("power_law_spectrum", 2.0, 128, 64),
)


def make_matrix(condition: DenseCondition, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    if condition.family == "gaussian":
        matrix = rng.standard_normal((condition.n, condition.m))
    else:
        left, _ = np.linalg.qr(rng.standard_normal((condition.n, condition.m)))
        right, _ = np.linalg.qr(rng.standard_normal((condition.m, condition.m)))
        singular_values = np.arange(1, condition.m + 1, dtype=np.float64)
        singular_values **= -condition.parameter
        matrix = (left * singular_values) @ right.T
    matrix /= np.linalg.norm(matrix)
    return matrix


def residual(matrix: np.ndarray) -> np.ndarray:
    return np.eye(matrix.shape[1]) - matrix.T @ matrix


def next_iterate_from_residual(
    matrix: np.ndarray, residual_matrix: np.ndarray, alpha: float
) -> np.ndarray:
    polynomial = (
        np.eye(matrix.shape[1])
        + 0.5 * residual_matrix
        + alpha * residual_matrix @ residual_matrix
    )
    return matrix @ polynomial


def direct_dense_choice(matrix: np.ndarray) -> tuple[float, float]:
    """Primary route: bounded search using only dense matrix operations."""
    residual_matrix = residual(matrix)

    def loss(alpha: float) -> float:
        candidate = next_iterate_from_residual(matrix, residual_matrix, alpha)
        return float(np.linalg.norm(residual(candidate)) ** 2)

    result = minimize_scalar(
        loss,
        bounds=ALPHA_BOUNDS,
        method="bounded",
        options={"xatol": 1e-11, "maxiter": 80},
    )
    candidates = (
        (float(result.x), loss(float(result.x))),
        (ALPHA_BOUNDS[0], loss(ALPHA_BOUNDS[0])),
        (ALPHA_BOUNDS[1], loss(ALPHA_BOUNDS[1])),
    )
    return min(candidates, key=lambda item: item[1])


def independent_spectral_choice(matrix: np.ndarray) -> tuple[float, float]:
    """Checker: solve the quartic from residual-matrix eigenvalues."""
    eigenvalues = np.linalg.eigvalsh(residual(matrix))
    squared_singular_values = 1 - eigenvalues
    base = 1 + 0.5 * eigenvalues
    direction = eigenvalues**2
    c0 = 1 - squared_singular_values * base**2
    c1 = -2 * squared_singular_values * base * direction
    c2 = -squared_singular_values * direction**2
    coefficients = np.array(
        [
            np.sum(c0**2),
            np.sum(2 * c0 * c1),
            np.sum(c1**2 + 2 * c0 * c2),
            np.sum(2 * c1 * c2),
            np.sum(c2**2),
        ]
    )
    roots = np.polynomial.polynomial.polyroots(
        np.arange(1, 5, dtype=np.float64) * coefficients[1:]
    )
    candidates = [ALPHA_BOUNDS[0], ALPHA_BOUNDS[1]]
    candidates.extend(
        float(root.real)
        for root in roots
        if abs(root.imag) < 1e-9 and ALPHA_BOUNDS[0] <= root.real <= ALPHA_BOUNDS[1]
    )

    def objective(alpha: float) -> float:
        return float(np.polynomial.polynomial.polyval(alpha, coefficients))

    alpha = min(candidates, key=objective)
    return alpha, objective(alpha)


def one_sample(task: tuple[DenseCondition, int]) -> dict[str, object]:
    condition, seed = task
    started = time.perf_counter()
    matrix = make_matrix(condition, seed)
    rows: list[dict[str, float | int | bool]] = []
    for iteration in range(ITERATIONS):
        residual_matrix = residual(matrix)
        pre_error = float(np.linalg.norm(residual_matrix))
        dense_alpha, dense_objective = direct_dense_choice(matrix)
        checker_alpha, checker_objective = independent_spectral_choice(matrix)
        informative = checker_objective > INFORMATIVE_OBJECTIVE_FLOOR
        dense_next = next_iterate_from_residual(matrix, residual_matrix, dense_alpha)
        checker_next = next_iterate_from_residual(
            matrix, residual_matrix, checker_alpha
        )
        dense_next_error = float(np.linalg.norm(residual(dense_next)))
        checker_next_error = float(np.linalg.norm(residual(checker_next)))
        objective_tolerance = 1e-12 + 1e-6 * checker_objective
        rows.append(
            {
                "iteration": iteration,
                "pre_error_fro": pre_error,
                "dense_alpha": dense_alpha,
                "checker_alpha": checker_alpha,
                "alpha_identifiable": informative,
                "alpha_difference": abs(dense_alpha - checker_alpha),
                "dense_objective": dense_objective,
                "checker_objective": checker_objective,
                "dense_objective_within_tolerance": (
                    dense_objective <= checker_objective + objective_tolerance
                ),
                "dense_next_error_fro": dense_next_error,
                "checker_next_error_fro": checker_next_error,
                "next_error_difference": abs(dense_next_error - checker_next_error),
            }
        )
        matrix = dense_next
    return {
        "condition": asdict(condition),
        "seed": seed,
        "rows": rows,
        "runtime_seconds": time.perf_counter() - started,
    }


def negative_control() -> int:
    profiles = {(3 / 8,) * ITERATIONS for _ in CONDITIONS}
    result = {
        "schema": "prism-fixed-alpha-negative-control-v2",
        "mutation": "replace the fitted coefficient by constant 3/8",
        "distinct_profiles": len(profiles),
        "required_distinct_profiles": 4,
    }
    print("DENSE_NEGATIVE_CONTROL=" + json.dumps(result, sort_keys=True))
    return 7 if result["distinct_profiles"] < result["required_distinct_profiles"] else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        return negative_control()
    started = time.perf_counter()
    tasks = [(condition, seed) for condition in CONDITIONS for seed in SEEDS]
    affinity = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else 1
    workers = min(6, affinity, len(tasks))
    with ProcessPoolExecutor(max_workers=workers) as executor:
        samples = list(executor.map(one_sample, tasks))
    rows = [row for sample in samples for row in sample["rows"]]
    identifiable_rows = [row for row in rows if row["alpha_identifiable"]]
    exact_profiles = {
        tuple(round(float(row["dense_alpha"]), 7) for row in sample["rows"])
        for sample in samples
    }
    payload = {
        "schema": "prism-dense-mechanism-certificate-v2",
        "conditions": [asdict(condition) for condition in CONDITIONS],
        "seeds": list(SEEDS),
        "iterations": ITERATIONS,
        "alpha_bounds": list(ALPHA_BOUNDS),
        "fit_target": "eigenvalues of R=I-X^T X",
        "uses_explicit_spectral_bound": False,
        "worker_processes": workers,
        "logical_cpu_affinity": affinity,
        "identifiable_row_count": len(identifiable_rows),
        "maximum_identifiable_alpha_difference": max(
            float(row["alpha_difference"]) for row in identifiable_rows
        ),
        "maximum_next_error_difference": max(
            float(row["next_error_difference"]) for row in rows
        ),
        "all_dense_objectives_match_checker": all(
            row["dense_objective_within_tolerance"] for row in rows
        ),
        "distinct_alpha_profiles": len(exact_profiles),
        "all_samples_improved": all(
            float(sample["rows"][-1]["dense_next_error_fro"])
            < float(sample["rows"][0]["pre_error_fro"])
            for sample in samples
        ),
        "samples": samples,
        "runtime_seconds": time.perf_counter() - started,
    }
    print(
        "DENSE_CERTIFICATE="
        + json.dumps(payload, sort_keys=True, separators=(",", ":"))
    )
    if payload["identifiable_row_count"] < 12:
        return 2
    if payload["maximum_identifiable_alpha_difference"] > 1e-5:
        return 3
    if payload["maximum_next_error_difference"] > 1e-7:
        return 4
    if not payload["all_dense_objectives_match_checker"]:
        return 5
    if payload["distinct_alpha_profiles"] < 4:
        return 6
    if not payload["all_samples_improved"]:
        return 8
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
