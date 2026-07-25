"""Evaluator-blind, fail-closed audit of the materialized Space candidate."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "release/space_candidate"
CLAIM_PAGES = [f"pages/claim-{number}/page.md" for number in range(1, 7)]
EXPECTED_VERDICTS = {
    1: "VERIFIED",
    2: "FALSIFIED",
    3: "FALSIFIED",
    4: "BLOCKED",
    5: "BLOCKED",
    6: "BLOCKED",
}
LINK_RE = re.compile(r"\[[^\]]+\]\((/[^)#]+)\)")
SECRET_PATTERNS = [
    re.compile(r"hf_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    opened: list[str] = []
    failures: list[str] = []

    def open_text(relative: str) -> str:
        path = CANDIDATE / relative
        if not path.is_file():
            failures.append(f"missing file: {relative}")
            return ""
        opened.append(relative)
        return path.read_text(errors="replace")

    readme = open_text("README.md")
    if "#/current-verification" not in readme:
        failures.append("README does not expose current verification")
    logbook = json.loads(open_text("logbook.json"))
    children = logbook["root"]["children"]
    if not children or children[0]["slug"] != "current-verification":
        failures.append("current verification is not first in navigation")
    historical_titles = [
        child["title"]
        for child in children
        if child["slug"] in {
            "overview",
            "claims",
            "evidence",
            "verification-run",
            "conclusion",
        }
    ]
    if any(
        not title.startswith("Historical rejected baseline")
        for title in historical_titles
    ):
        failures.append("historical navigation is not explicitly labeled")

    current = open_text("pages/current-verification/page.md")
    fixed_command = (
        "uv run --frozen --python 3.11 python repro/src/run_reproduction.py"
    )
    if fixed_command not in current:
        failures.append("fixed command absent from current page")
    for number, verdict in EXPECTED_VERDICTS.items():
        if f"| {number} |" not in current or verdict not in current:
            failures.append(f"claim {number} missing from visibility matrix")

    for number, relative in enumerate(CLAIM_PAGES, start=1):
        page = open_text(relative)
        verdict = EXPECTED_VERDICTS[number]
        required_phrases = [
            verdict,
            "Exact contract",
            "Source",
            "Confidence",
            "Raw",
            "checker",
            "control",
        ]
        for phrase in required_phrases:
            if phrase.lower() not in page.lower():
                failures.append(
                    f"{relative} missing evaluator-visible phrase: {phrase}"
                )
        for link in LINK_RE.findall(page):
            target = link.lstrip("/")
            open_text(target)

        raw_relative = f"evidence/claim{number}/raw_result.json"
        try:
            raw = json.loads(open_text(raw_relative))
        except json.JSONDecodeError as error:
            failures.append(f"invalid JSON {raw_relative}: {error}")
            continue
        if raw.get("verdict") != verdict:
            failures.append(
                f"{raw_relative} verdict {raw.get('verdict')} != {verdict}"
            )

    release_report = open_text("pages/release-report/page.md")
    for phrase in [
        "Previous live judged score: `5/12`",
        "Conservative projected score range",
        "Best-supported possible new score",
        "forecast, not a judge result",
    ]:
        if phrase.lower() not in release_report.lower():
            failures.append(f"release report missing: {phrase}")

    subset = json.loads(open_text("manifest/judged_subset_check.json"))
    if not subset.get("old_file_set_subset_of_candidate"):
        failures.append("judged old-file subset check failed")
    if not all(subset.get("overlaid_historical_hash_match", {}).values()):
        failures.append("overlaid judged bytes not preserved historically")

    allowlist = [
        line
        for line in open_text("manifest/upload_allowlist.txt").splitlines()
        if line
    ]
    binary_suffixes = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".pdf",
        ".zip",
        ".tar",
        ".gz",
        ".npy",
        ".npz",
        ".pt",
        ".pth",
    }
    binary_uploads = [
        relative
        for relative in allowlist
        if Path(relative).suffix.lower() in binary_suffixes
    ]
    if binary_uploads:
        failures.append(f"non-text paths in upload allowlist: {binary_uploads}")

    hash_manifest = json.loads(open_text("manifest/candidate_sha256.json"))
    for relative, expected in hash_manifest["files"].items():
        path = CANDIDATE / relative
        if not path.is_file() or sha256(path) != expected:
            failures.append(f"hash mismatch: {relative}")

    secret_hits = []
    for relative in allowlist:
        path = CANDIDATE / relative
        if not path.is_file():
            failures.append(f"allowlisted path missing: {relative}")
            continue
        text = path.read_text(errors="replace")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                secret_hits.append(
                    {"path": relative, "pattern": pattern.pattern}
                )
    if secret_hits:
        failures.append(f"potential secrets: {secret_hits}")

    review = {
        "schema": "evaluator-blind-red-team-v1",
        "entrypoint": "README.md",
        "files_opened": list(dict.fromkeys(opened)),
        "files_opened_count": len(set(opened)),
        "conclusions_not_verified": failures,
        "current_verifier_obvious": not failures,
        "visibility_matrix_complete": not failures,
        "secret_hits": secret_hits,
        "upload_allowlist_text_only": not binary_uploads,
        "review_passed": not failures,
    }
    record = CANDIDATE / "manifest/red_team_review.json"
    record.write_text(json.dumps(review, indent=2, sort_keys=True) + "\n")
    print(json.dumps(review, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
