"""Fixed experiment entrypoint.

The baseline intentionally invokes the historical verifier unchanged. Child
experiments may extend this module, but the OpenResearch run command remains
fixed for the entire tree.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    started = time.perf_counter()
    command = [sys.executable, str(ROOT / "repro/src/verify_prism.py")]
    completed = subprocess.run(command, cwd=ROOT, check=False)
    metadata = {
        "schema": "prism-run-metadata-v1",
        "backend_policy": "hf/cpu-upgrade for uncertain or >5 minute tasks",
        "estimated_cores_before_launch": 2,
        "selected_flavor": "cpu-upgrade",
        "actual_logical_cpu_allocation": os.cpu_count(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "runtime_seconds": time.perf_counter() - started,
        "historical_verifier_exit_code": completed.returncode,
    }
    print("RUN_METADATA=" + json.dumps(metadata, sort_keys=True), flush=True)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
