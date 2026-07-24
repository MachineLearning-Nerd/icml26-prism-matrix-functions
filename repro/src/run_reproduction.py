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
    suite_ok = (
        historical.returncode == 0
        and primary.returncode == 0
        and independent.returncode == 0
        and negative.returncode != 0
    )
    metadata = {
        "schema": "prism-run-metadata-v1",
        "backend_policy": "hf/cpu-upgrade for uncertain or >5 minute tasks",
        "estimated_cores_before_launch": 1,
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
        "cumulative_suite_passed": suite_ok,
    }
    print("RUN_METADATA=" + json.dumps(metadata, sort_keys=True), flush=True)
    return 0 if suite_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
