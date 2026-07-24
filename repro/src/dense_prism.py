"""Independent dense reconstruction of fifth-order polar PRISM."""

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
SEEDS = (202601, 202602, 202603)
ITERATIONS = 8
SKETCH_DIMENSION = 64


@dataclass(frozen=True)
class DenseCondition:
    family: str
    parameter: float
    n: int
    m: int


CONDITIONS = (
    DenseCondition("gaussian", 1.0, 256, 256),
    DenseCondition("gaussian", 4.0, 512, 128),
    DenseCondition("gaussian", 50.0, 3_200, 64),
    DenseCondition("htmp", 0.1, 256, 128),
    DenseCondition("htmp", 0.5, 256, 128),
    DenseCondition("htmp", 100.0, 256, 128),
)


def make_matrix(condition: DenseCondition, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    if condition.family == "gaussian":
        matrix = rng.standard_normal((condition.n, condition.m))
    else:
        beta = condition.parameter / condition.m
        d = np.sqrt(
            rng.chisquare(
                beta * condition.n - beta * np.arange(condition.m)
            )
        )
        t = np.sqrt(
            rng.chisquare(
                beta * (condition.m - 1 - np.arange(condition.m - 1))
            )
        )
        bidiagonal = np.diag(d) + np.diag(t, k=-1)
        matrix = np.zeros((condition.n, condition.m))
        matrix[: condition.m] = bidiagonal
    matrix /= np.linalg.norm(matrix)
    return matrix


def next_iterate(matrix: np.ndarray, alpha: float) -> np.ndarray:
    residual = np.eye(matrix.shape[1]) - matrix.T @ matrix
    polynomial = (
        np.eye(matrix.shape[1])
        + 0.5 * residual
        + alpha * (residual @ residual)
    )
    return matrix @ polynomial


def dense_alpha(matrix: np.ndarray, sketch: np.ndarray | None) -> float:
    """Primary implementation: direct dense loss and bounded scalar search."""
    if sketch is None:
        sketch = np.eye(matrix.shape[1])

    def loss(alpha: float) -> float:
        candidate = next_iterate(matrix, alpha)
        residual = np.eye(matrix.shape[1]) - candidate.T @ candidate
        return float(np.linalg.norm(sketch @ residual) ** 2)

    result = minimize_scalar(
        loss,
        bounds=ALPHA_BOUNDS,
        method="bounded",
        options={"xatol": 1e-13, "maxiter": 500},
    )
    candidates = [
        (float(result.x), loss(float(result.x))),
        (ALPHA_BOUNDS[0], loss(ALPHA_BOUNDS[0])),
        (ALPHA_BOUNDS[1], loss(ALPHA_BOUNDS[1])),
    ]
    return min(candidates, key=lambda item: item[1])[0]


def scalar_alpha(singular_values: np.ndarray) -> float:
    """Independent checker: build quartic coefficients in spectral coordinates."""
    squared = singular_values**2
    residual = 1 - squared
    constant = 1 - squared * (1 + 0.5 * residual) ** 2
    linear = -2 * squared * (1 + 0.5 * residual) * residual**2
    quadratic = -squared * residual**4
    coefficients = np.array(
        [
            np.sum(constant**2),
            np.sum(2 * constant * linear),
            np.sum(linear**2 + 2 * constant * quadratic),
            np.sum(2 * linear * quadratic),
            np.sum(quadratic**2),
        ]
    )
    roots = np.polynomial.polynomial.polyroots(
        np.arange(1, 5) * coefficients[1:]
    )
    candidates = [ALPHA_BOUNDS[0], ALPHA_BOUNDS[1]]
    candidates.extend(
        float(root.real)
        for root in roots
        if abs(root.imag) < 1e-9 and ALPHA_BOUNDS[0] <= root.real <= ALPHA_BOUNDS[1]
    )
    return min(
        candidates,
        key=lambda alpha: np.polynomial.polynomial.polyval(alpha, coefficients),
    )


def residual_fro(matrix: np.ndarray) -> float:
    return float(
        np.linalg.norm(np.eye(matrix.shape[1]) - matrix.T @ matrix)
    )


def one_condition(task: tuple[DenseCondition, int]) -> dict[str, object]:
    condition, seed = task
    started = time.perf_counter()
    matrix = make_matrix(condition, seed)
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    exact_rows: list[dict[str, float | int]] = []
    sketch_rows: list[dict[str, float | int]] = []
    maximum_alpha_difference = 0.0
    maximum_error_difference = 0.0
    sketch_rng = np.random.default_rng(seed + 1_000_000)
    sketch_matrix = matrix.copy()
    for iteration in range(ITERATIONS):
        dense_choice = dense_alpha(matrix, None)
        spectral_choice = scalar_alpha(singular_values)
        dense_error = residual_fro(matrix)
        spectral_error = float(np.linalg.norm(1 - singular_values**2))
        maximum_alpha_difference = max(
            maximum_alpha_difference, abs(dense_choice - spectral_choice)
        )
        maximum_error_difference = max(
            maximum_error_difference, abs(dense_error - spectral_error)
        )
        exact_rows.append(
            {
                "iteration": iteration,
                "dense_alpha": dense_choice,
                "independent_spectral_alpha": spectral_choice,
                "dense_error_fro": dense_error,
                "independent_spectral_error_fro": spectral_error,
            }
        )
        sketch = sketch_rng.normal(
            loc=0.0,
            scale=1 / np.sqrt(SKETCH_DIMENSION),
            size=(SKETCH_DIMENSION, condition.m),
        )
        sketch_choice = dense_alpha(sketch_matrix, sketch)
        exact_choice_for_sketch_state = dense_alpha(sketch_matrix, None)
        sketch_rows.append(
            {
                "iteration": iteration,
                "sketched_alpha": sketch_choice,
                "exact_alpha_same_state": exact_choice_for_sketch_state,
                "pre_update_error_fro": residual_fro(sketch_matrix),
            }
        )
        matrix = next_iterate(matrix, dense_choice)
        singular_values *= (
            1
            + 0.5 * (1 - singular_values**2)
            + spectral_choice * (1 - singular_values**2) ** 2
        )
        sketch_matrix = next_iterate(sketch_matrix, sketch_choice)
    maximum_error_difference = max(
        maximum_error_difference,
        abs(
            residual_fro(matrix)
            - float(np.linalg.norm(1 - singular_values**2))
        ),
    )
    return {
        "condition": asdict(condition),
        "seed": seed,
        "exact_rows": exact_rows,
        "sketch_rows": sketch_rows,
        "final_exact_error_fro": residual_fro(matrix),
        "final_sketch_error_fro": residual_fro(sketch_matrix),
        "maximum_dense_vs_spectral_alpha_difference": maximum_alpha_difference,
        "maximum_dense_vs_spectral_error_difference": maximum_error_difference,
        "runtime_seconds": time.perf_counter() - started,
    }


def negative_control() -> int:
    """A fixed coefficient must not pass a spectrum-adaptation checker."""
    profiles = {(3 / 8,) * ITERATIONS for _ in CONDITIONS}
    result = {
        "schema": "prism-fixed-alpha-negative-control-v1",
        "coefficient": 3 / 8,
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
    affinity = (
        len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else 1
    )
    workers = min(6, affinity, len(tasks))
    with ProcessPoolExecutor(max_workers=workers) as executor:
        samples = list(executor.map(one_condition, tasks))
    maximum_alpha_difference = max(
        float(sample["maximum_dense_vs_spectral_alpha_difference"])
        for sample in samples
    )
    maximum_error_difference = max(
        float(sample["maximum_dense_vs_spectral_error_difference"])
        for sample in samples
    )
    exact_profiles = {
        tuple(round(float(row["dense_alpha"]), 8) for row in sample["exact_rows"])
        for sample in samples
    }
    sketch_profiles = {
        tuple(
            round(float(row["sketched_alpha"]), 8)
            for row in sample["sketch_rows"]
        )
        for sample in samples
    }
    payload = {
        "schema": "prism-dense-independent-v1",
        "seeds": list(SEEDS),
        "iterations": ITERATIONS,
        "sketch_dimension": SKETCH_DIMENSION,
        "sketch_distribution": "iid N(0,1/p)",
        "estimated_useful_cores": 6,
        "actual_worker_processes": workers,
        "logical_cpu_affinity": affinity,
        "maximum_dense_vs_spectral_alpha_difference": maximum_alpha_difference,
        "maximum_dense_vs_spectral_error_difference": maximum_error_difference,
        "distinct_exact_alpha_profiles": len(exact_profiles),
        "distinct_sketch_alpha_profiles": len(sketch_profiles),
        "all_sketch_runs_improved": all(
            float(sample["final_sketch_error_fro"])
            < float(sample["sketch_rows"][0]["pre_update_error_fro"])
            for sample in samples
        ),
        "runtime_seconds": time.perf_counter() - started,
        "samples": samples,
    }
    print("DENSE_RESULT=" + json.dumps(payload, sort_keys=True, separators=(",", ":")))
    if maximum_alpha_difference > 1e-7:
        return 3
    if maximum_error_difference > 1e-7:
        return 4
    if len(exact_profiles) < 4 or len(sketch_profiles) < 4:
        return 5
    if not payload["all_sketch_runs_improved"]:
        return 6
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
