"""Reconstruct Figure D.2 from the cited limiting HTMP density.

This route implements Eq. (E.5) of Hodgkinson, Wang, and Mahoney (2025)
directly.  It avoids the underflow-prone finite chi-square construction by
integrating the limiting density in log-eigenvalue coordinates and using its
deterministic midpoint quantiles.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor

import mpmath as mp
import numpy as np

from spectral_prism import bounded_prism_alpha, residual_error


GAMMA = 0.5
KAPPAS = (0.1, 0.5, 100.0)
N_EIGENVALUES = 4_000
HORIZON = 32
LOG_GRID_MIN = -750.0
LOG_GRID_MAX = 20.0
LOG_GRID_SIZE = 6_001
PAPER_FIRST_HIT_BRACKETS = {
    0.1: {"fro_1e-2": (17, 19), "fro_1e-4": (18, 20)},
    0.5: {"fro_1e-2": (17, 19), "fro_1e-4": (18, 20)},
    100.0: {"fro_1e-2": (7, 9), "fro_1e-4": (7, 10)},
}


def htmp_log_density(log_x: float, kappa: float, gamma: float = GAMMA) -> float:
    """Return rho(exp(log_x))*exp(log_x), the density in log coordinates."""
    mp.mp.dps = 35
    x = mp.exp(log_x)
    a = mp.mpf(kappa) / 2
    scale = mp.mpf(kappa) / (2 * gamma)
    b = -scale + 1 + a
    t = scale * x
    normalization = scale / (mp.gamma(a + 1) * mp.gamma(scale))
    rho = (
        normalization
        * mp.power(t, scale - 1 - a)
        * mp.exp(-t)
        / abs(mp.hyperu(a, b, -t)) ** 2
    )
    return float(rho * x)


def limiting_quantiles(kappa: float) -> tuple[np.ndarray, dict[str, float]]:
    log_grid = np.linspace(LOG_GRID_MIN, LOG_GRID_MAX, LOG_GRID_SIZE)
    density_log = np.array(
        [htmp_log_density(float(log_x), kappa) for log_x in log_grid],
        dtype=np.float64,
    )
    if not np.all(np.isfinite(density_log)) or np.any(density_log < 0):
        raise ArithmeticError("Eq. E.5 produced an invalid density")
    increments = 0.5 * (density_log[1:] + density_log[:-1]) * np.diff(log_grid)
    cdf = np.concatenate(([0.0], np.cumsum(increments)))
    captured_mass = float(cdf[-1])
    if not 0.98 <= captured_mass <= 1.02:
        raise ArithmeticError(f"Eq. E.5 captured mass {captured_mass} is not near one")
    cdf /= cdf[-1]
    probabilities = (np.arange(N_EIGENVALUES) + 0.5) / N_EIGENVALUES
    quantile_logs = np.interp(probabilities, cdf, log_grid)
    eigenvalues = np.exp(quantile_logs)
    audit = {
        "captured_probability_mass_before_normalization": captured_mass,
        "minimum_midpoint_quantile": float(eigenvalues[0]),
        "median_midpoint_quantile": float(eigenvalues[N_EIGENVALUES // 2]),
        "maximum_midpoint_quantile": float(eigenvalues[-1]),
        "trapezoid_grid_points": LOG_GRID_SIZE,
        "log_grid_min": LOG_GRID_MIN,
        "log_grid_max": LOG_GRID_MAX,
    }
    return eigenvalues, audit


def first_hit(values: list[float], threshold: float) -> int | None:
    return next((index for index, value in enumerate(values) if value <= threshold), None)


def one_kappa(kappa: float) -> dict[str, object]:
    started = time.perf_counter()
    eigenvalues, density_audit = limiting_quantiles(kappa)
    singular_values = np.sqrt(eigenvalues)
    singular_values /= np.linalg.norm(singular_values)
    errors: list[float] = []
    alphas: list[float] = []
    for iteration in range(HORIZON + 1):
        error_fro, _ = residual_error(singular_values)
        errors.append(error_fro)
        if iteration == HORIZON:
            break
        alpha, _ = bounded_prism_alpha(singular_values)
        alphas.append(alpha)
        residual = 1 - singular_values**2
        singular_values *= 1 + 0.5 * residual + alpha * residual**2
    hits = {
        "fro_1e-2": first_hit(errors, 1e-2),
        "fro_1e-4": first_hit(errors, 1e-4),
    }
    checks = {
        key: hits[key] is not None and low <= hits[key] <= high
        for key, (low, high) in PAPER_FIRST_HIT_BRACKETS[kappa].items()
    }
    return {
        "kappa": kappa,
        "gamma": GAMMA,
        "density_audit": density_audit,
        "first_hits": hits,
        "paper_first_hit_brackets": PAPER_FIRST_HIT_BRACKETS[kappa],
        "hit_checks": checks,
        "matches_all_anchors": all(checks.values()),
        "error_fro_profile": errors,
        "alpha_profile": alphas,
        "runtime_seconds": time.perf_counter() - started,
    }


def negative_control() -> int:
    """Omitting the dx=x dlog(x) Jacobian must not yield a normalized density."""
    log_grid = np.linspace(-80, 20, 401)
    wrong_integral = float(
        np.trapezoid(
            [
                htmp_log_density(float(log_x), 0.5) / math.exp(float(log_x))
                for log_x in log_grid
            ],
            log_grid,
        )
    )
    print(
        "HTMP_DENSITY_NEGATIVE_CONTROL="
        + json.dumps(
            {
                "mutation": "omitted log-coordinate Jacobian",
                "wrong_integral": wrong_integral,
                "expected": "not within 2% of one",
            },
            sort_keys=True,
        )
    )
    return 9 if not 0.98 <= wrong_integral <= 1.02 else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        return negative_control()
    started = time.perf_counter()
    affinity = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else 1
    workers = min(3, affinity)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        rows = list(executor.map(one_kappa, KAPPAS))
    payload = {
        "schema": "prism-htmp-limiting-density-v1",
        "equation": "Hodgkinson et al. (2025), Eq. E.5",
        "paper_dimensions": [8_000, N_EIGENVALUES],
        "gamma": GAMMA,
        "kappas": list(KAPPAS),
        "horizon": HORIZON,
        "worker_processes": workers,
        "logical_cpu_affinity": affinity,
        "rows": rows,
        "matches_every_published_anchor": all(
            row["matches_all_anchors"] for row in rows
        ),
        "runtime_seconds": time.perf_counter() - started,
    }
    print(
        "HTMP_LIMITING_DENSITY="
        + json.dumps(payload, sort_keys=True, separators=(",", ":"))
    )
    if not payload["matches_every_published_anchor"]:
        print("HTMP_LIMITING_DENSITY_DID_NOT_MATCH_ALL_PUBLISHED_ANCHORS")
        return 8
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
