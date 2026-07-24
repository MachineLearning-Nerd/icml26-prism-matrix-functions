"""Fixed experiment entrypoint with cumulative historical regression."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run_and_echo(command: list[str]) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command, cwd=ROOT, check=False, capture_output=True, text=True
    )
    print("$ " + " ".join(command), flush=True)
    print(completed.stdout, end="", flush=True)
    print(completed.stderr, end="", flush=True)
    print(f"EXIT_CODE={completed.returncode}", flush=True)
    return completed


def main() -> int:
    started = time.perf_counter()
    historical = run_and_echo(
        [sys.executable, str(ROOT / "repro/src/verify_prism.py")]
    )
    primary = run_and_echo(
        [sys.executable, str(ROOT / "repro/src/theorem_counterexample.py")]
    )
    independent = run_and_echo(
        [sys.executable, str(ROOT / "repro/src/check_theorem_counterexample.py")]
    )
    negative = run_and_echo(
        [
            sys.executable,
            str(ROOT / "repro/src/check_theorem_counterexample.py"),
            str(ROOT / ".openresearch/artifacts/claim2/negative_control.json"),
        ]
    )
    spectral = run_and_echo(
        [sys.executable, str(ROOT / "repro/src/spectral_prism.py")]
    )
    spectral_negative = run_and_echo(
        [
            sys.executable,
            str(ROOT / "repro/src/spectral_prism.py"),
            "--negative-control",
        ]
    )
    dense = run_and_echo(
        [sys.executable, str(ROOT / "repro/src/dense_prism_certificate.py")]
    )
    dense_negative = run_and_echo(
        [
            sys.executable,
            str(ROOT / "repro/src/dense_prism_certificate.py"),
            "--negative-control",
        ]
    )
    archive_audit = run_and_echo(
        [sys.executable, str(ROOT / "repro/src/audit_arxiv_reproducibility.py")]
    )
    archive_audit_negative = run_and_echo(
        [
            sys.executable,
            str(ROOT / "repro/src/audit_arxiv_reproducibility.py"),
            "--negative-control",
        ]
    )
    suite_ok = (
        historical.returncode == 0
        and primary.returncode == 0
        and independent.returncode == 0
        and negative.returncode != 0
        and spectral.returncode == 0
        and spectral_negative.returncode != 0
        and dense.returncode == 0
        and dense_negative.returncode != 0
        and archive_audit.returncode == 0
        and archive_audit_negative.returncode != 0
    )
    metadata = {
        "schema": "prism-run-metadata-v1",
        "backend_policy": "HF cpu-upgrade for a six-worker uncertain-runtime CPU experiment",
        "estimated_cores_before_launch": 6,
        "selected_backend": "hf",
        "selected_flavor": "cpu-upgrade",
        "actual_logical_cpu_allocation": os.cpu_count(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "runtime_seconds": time.perf_counter() - started,
        "historical_verifier_exit_code": historical.returncode,
        "primary_verifier_exit_code": primary.returncode,
        "independent_checker_exit_code": independent.returncode,
        "negative_control_exit_code": negative.returncode,
        "negative_control_failed_as_intended": negative.returncode != 0,
        "spectral_verifier_exit_code": spectral.returncode,
        "spectral_negative_control_exit_code": spectral_negative.returncode,
        "spectral_negative_control_failed_as_intended": spectral_negative.returncode
        != 0,
        "dense_verifier_exit_code": dense.returncode,
        "dense_negative_control_exit_code": dense_negative.returncode,
        "dense_negative_control_failed_as_intended": dense_negative.returncode != 0,
        "archive_audit_exit_code": archive_audit.returncode,
        "archive_audit_negative_control_exit_code": archive_audit_negative.returncode,
        "archive_audit_negative_control_failed_as_intended": (
            archive_audit_negative.returncode != 0
        ),
        "cumulative_suite_passed": suite_ok,
    }
    print("RUN_METADATA=" + json.dumps(metadata, sort_keys=True), flush=True)
    return 0 if suite_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
