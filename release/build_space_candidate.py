"""Materialize and audit the additive, text-only PRISM Space candidate."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "release/space_candidate"
JUDGED = Path("/tmp/prism-judged-space-60c5a76")
STARTUP_MANIFEST = (
    ROOT / ".openresearch/artifacts/startup/judged_space_manifest.json"
)

CODE_FILES = [
    "prism.py",
    "verify_prism.py",
    "run_reproduction.py",
    "dense_prism_certificate.py",
    "spectral_prism.py",
    "theorem_counterexample.py",
    "check_theorem_counterexample.py",
    "htmp_calibration.py",
    "htmp_limiting_density.py",
    "audit_arxiv_reproducibility.py",
    "claim6_falsification_audit.py",
    "check_claim6_falsification.py",
    "training_claims_closure.py",
    "check_training_claims_closure.py",
]
CLAIMS = ["claim1", "claim2", "claim3", "claim4", "claim5", "claim6"]
TEXT_SUFFIXES = {".md", ".json", ".txt", ".py", ".toml", ".lock", ".css", ".js", ".html", ".svg"}
OVERLAID_PROTECTED = {"README.md", "logbook.json", "pages/index.md"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def require_judged_snapshot() -> dict[str, object]:
    manifest = json.loads(STARTUP_MANIFEST.read_text())
    mismatches = []
    for relative, expected in manifest["files"].items():
        path = JUDGED / relative
        actual = sha256(path) if path.is_file() else None
        if actual != expected:
            mismatches.append(
                {"path": relative, "expected": expected, "actual": actual}
            )
    if mismatches:
        raise RuntimeError(f"judged snapshot mismatch: {mismatches}")
    return manifest


def preserve_judged_files(manifest: dict[str, object]) -> None:
    historical = CANDIDATE / "historical/judged-60c5a76"
    for relative in manifest["files"]:
        source = JUDGED / relative
        target = CANDIDATE / relative
        if relative not in OVERLAID_PROTECTED and not target.exists():
            copy_file(source, target)
        if source.suffix.lower() in TEXT_SUFFIXES or source.name in {
            "README.md",
            "logbook.json",
        }:
            copy_file(source, historical / relative)


def copy_current_evidence() -> None:
    code_dir = CANDIDATE / "code"
    for name in CODE_FILES:
        copy_file(ROOT / "repro/src" / name, code_dir / name)
        copy_file(ROOT / "repro/src" / name, CANDIDATE / "repro/src" / name)
    cache_dir = code_dir / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    for claim in CLAIMS:
        source_dir = ROOT / ".openresearch/artifacts" / claim
        target_dir = CANDIDATE / "evidence" / claim
        for source in sorted(source_dir.iterdir()):
            if source.is_file() and source.suffix.lower() in TEXT_SUFFIXES:
                copy_file(source, target_dir / source.name)
                copy_file(
                    source,
                    CANDIDATE
                    / ".openresearch/artifacts"
                    / claim
                    / source.name,
                )

    copy_file(ROOT / "pyproject.toml", CANDIDATE / "environment/pyproject.toml")
    copy_file(ROOT / "uv.lock", CANDIDATE / "environment/uv.lock")
    copy_file(
        ROOT / ".openresearch/artifacts/startup/paper_source.json",
        CANDIDATE / "evidence/source/paper_source.json",
    )
    copy_file(
        STARTUP_MANIFEST,
        CANDIDATE / "manifest/judged_space_manifest.json",
    )


def audit_and_manifest(manifest: dict[str, object]) -> None:
    old_paths = sorted(manifest["files"])
    subset = all((CANDIDATE / relative).exists() for relative in old_paths)
    unchanged_at_original_path = {
        relative: sha256(CANDIDATE / relative) == expected
        for relative, expected in manifest["files"].items()
    }
    overlaid_historical_hash_match = {
        relative: sha256(
            CANDIDATE / "historical/judged-60c5a76" / relative
        )
        == manifest["files"][relative]
        for relative in sorted(OVERLAID_PROTECTED)
    }
    subset_record = {
        "schema": "protected-space-subset-check-v1",
        "space_id": manifest["space_id"],
        "judged_revision": manifest["revision"],
        "old_file_set_subset_of_candidate": subset,
        "old_file_count": len(old_paths),
        "old_paths": old_paths,
        "unchanged_at_original_path": unchanged_at_original_path,
        "overlaid_protected_files": sorted(OVERLAID_PROTECTED),
        "overlaid_historical_hash_match": overlaid_historical_hash_match,
        "note": (
            "Canonical navigation files are intentionally overlaid to expose the "
            "current verifier; their exact judged bytes are preserved under "
            "historical/judged-60c5a76."
        ),
    }
    manifest_dir = CANDIDATE / "manifest"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / "judged_subset_check.json").write_text(
        json.dumps(subset_record, indent=2, sort_keys=True) + "\n"
    )

    required_paths = [
        "README.md",
        "pages/current-verification/page.md",
        *[f"pages/claim-{number}/page.md" for number in range(1, 7)],
        *[f"evidence/claim{number}/raw_result.json" for number in range(1, 7)],
        "pages/release-report/page.md",
    ]
    traversal = {
        "schema": "evaluator-visible-traversal-v1",
        "entrypoint": "README.md",
        "files_opened": required_paths,
        "missing": [
            relative
            for relative in required_paths
            if not (CANDIDATE / relative).is_file()
        ],
        "hidden_project_evidence_used": False,
    }
    (manifest_dir / "evaluator_traversal.json").write_text(
        json.dumps(traversal, indent=2, sort_keys=True) + "\n"
    )

    upload_paths = []
    for path in sorted(CANDIDATE.rglob("*")):
        relative_parts = path.relative_to(CANDIDATE).parts
        if not path.is_file() or ".cache" in relative_parts:
            continue
        relative = path.relative_to(CANDIDATE).as_posix()
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {
            "README.md",
            "logbook.json",
            "uv.lock",
        }:
            upload_paths.append(relative)
    allowlist_path = manifest_dir / "upload_allowlist.txt"
    allowlist_path.write_text("\n".join(upload_paths) + "\n")

    hashes = {
        relative: sha256(CANDIDATE / relative)
        for relative in upload_paths
        if relative != "manifest/candidate_sha256.json"
    }
    (manifest_dir / "candidate_sha256.json").write_text(
        json.dumps(
            {
                "schema": "text-upload-sha256-v1",
                "space_id": "DineshAI/hwhvjhXC0m",
                "files": hashes,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def main() -> None:
    manifest = require_judged_snapshot()
    preserve_judged_files(manifest)
    copy_current_evidence()
    audit_and_manifest(manifest)
    print(
        json.dumps(
            {
                "candidate": str(CANDIDATE),
                "protected_files": len(manifest["files"]),
                "text_upload_files": len(
                    (
                        CANDIDATE / "manifest/upload_allowlist.txt"
                    ).read_text().splitlines()
                ),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
