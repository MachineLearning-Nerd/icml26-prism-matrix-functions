"""Fail-closed audit of the PRISM arXiv source archive for Claim 6."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import tarfile
import urllib.request


SOURCE_URL = "https://export.arxiv.org/e-print/2601.22137"
USER_AGENT = "OpenResearch-PRISM-Reproduction/1.0"
EXECUTABLE_SUFFIXES = (".py", ".ipynb", ".sh", ".jl", ".m", ".r")
RAW_DATA_SUFFIXES = (".csv", ".tsv", ".npy", ".npz", ".pt", ".pth", ".parquet")
REQUIRED_PLOTS = (
    "plots/HTMP_iteration_n=8000_m=4000_kappa=0.1.png",
    "plots/HTMP_iteration_n=8000_m=4000_kappa=0.5.png",
    "plots/HTMP_iteration_n=8000_m=4000_kappa=100.0.png",
    "plots/alphas_htmp.png",
)


def retrieve() -> bytes:
    request = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def audit() -> dict[str, object]:
    source = retrieve()
    with tarfile.open(fileobj=io.BytesIO(source), mode="r:*") as archive:
        members = [member for member in archive.getmembers() if member.isfile()]
        names = [member.name.removeprefix("./") for member in members]
        executable = [
            name for name in names if name.lower().endswith(EXECUTABLE_SUFFIXES)
        ]
        raw_data = [name for name in names if name.lower().endswith(RAW_DATA_SUFFIXES)]
        tex_chunks = []
        plot_hashes: dict[str, str] = {}
        for member in members:
            normalized = member.name.removeprefix("./")
            extracted = archive.extractfile(member)
            if extracted is None:
                continue
            content = extracted.read()
            if normalized.endswith(".tex"):
                tex_chunks.append(content.decode("utf-8", errors="replace"))
            if normalized in REQUIRED_PLOTS:
                plot_hashes[normalized] = hashlib.sha256(content).hexdigest()
        tex = "\n".join(tex_chunks)
    seed_lines = [
        line.strip()
        for line in tex.splitlines()
        if "seed" in line.lower() and not line.lstrip().startswith("%")
    ]
    operational_generator_lines = [
        line.strip()
        for line in tex.splitlines()
        if (
            "generate" in line.lower()
            and ("htmp" in line.lower() or "marchenko" in line.lower())
        )
    ]
    missing = []
    if not executable:
        missing.append("generator or experiment executable")
    if not raw_data:
        missing.append("machine-readable raw curve data")
    if not seed_lines:
        missing.append("random seed")
    if "float32" not in tex:
        missing.append("numerical precision")
    if len(plot_hashes) != len(REQUIRED_PLOTS):
        missing.append("all required Figure D.2 plot files")
    return {
        "schema": "prism-arxiv-reproducibility-audit-v1",
        "source_url": SOURCE_URL,
        "explicit_user_agent": USER_AGENT,
        "archive_sha256": hashlib.sha256(source).hexdigest(),
        "file_count": len(names),
        "executable_files": executable,
        "raw_data_files": raw_data,
        "seed_lines": seed_lines,
        "operational_generator_lines": operational_generator_lines,
        "plot_sha256": plot_hashes,
        "precision_float32_present": "float32" in tex,
        "missing_operational_items": missing,
        "claim6_operationally_reproducible_from_archive": not missing,
    }


def negative_control() -> int:
    """Images and prose must not be misclassified as code, data, or a seed."""
    fake_files = ["plots/alphas_htmp.png", "06_experiments.tex"]
    incorrectly_complete = any(
        name.lower().endswith(EXECUTABLE_SUFFIXES + RAW_DATA_SUFFIXES)
        for name in fake_files
    )
    result = {
        "schema": "archive-classification-negative-control-v1",
        "mutation": "treat a plot and prose as operational generator evidence",
        "fake_files": fake_files,
        "incorrectly_complete": incorrectly_complete,
    }
    print("ARCHIVE_AUDIT_NEGATIVE_CONTROL=" + json.dumps(result, sort_keys=True))
    return 9 if not incorrectly_complete else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        return negative_control()
    payload = audit()
    print("ARXIV_REPRODUCIBILITY_AUDIT=" + json.dumps(payload, sort_keys=True))
    if not payload["claim6_operationally_reproducible_from_archive"]:
        print("CLAIM6_ARCHIVE_ROUTE_BLOCKED")
        return 8
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
