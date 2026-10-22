"""Generate an index from a reviewed Git input commit and digest-addressed wheels."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from catalog import (
    PIN,
    ROOT,
    build_entry,
    canonical,
    fetch_artifact,
    parse_json,
    read_json,
    retained_entry,
    validate_index,
    validate_transition,
    verify_host,
)


def git(repo, *args):
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, encoding="utf-8"
    ).strip()


def generate(
    source_repo,
    source_commit,
    approved_ref,
    sequence,
    artifacts,
    host,
    python,
    fetch=False,
    previous=None,
):
    commit = git(source_repo, "rev-parse", source_commit + "^{commit}")
    subprocess.run(
        [
            "git",
            "-C",
            str(source_repo),
            "merge-base",
            "--is-ancestor",
            commit,
            approved_ref,
        ],
        check=True,
        capture_output=True,
    )
    generator = git(ROOT, "rev-parse", "HEAD")
    if git(
        ROOT,
        "status",
        "--porcelain",
        "--",
        "tools",
        "catalog/policy.json",
        "catalog/schema.json",
        "catalog/toolchain.json",
    ):
        raise ValueError(
            "commit the trusted generator inputs before generating an index"
        )
    profile = verify_host(host, python)
    paths = git(
        source_repo,
        "ls-tree",
        "-r",
        "--name-only",
        commit,
        "catalog/packages",
        "catalog/security.json",
    ).splitlines()
    entries, safety = [], []
    for path in paths:
        if not path.endswith(".json"):
            continue
        # Git tree content, never a submitter-selected executable or working-tree file.
        raw = git(source_repo, "show", f"{commit}:{path}")
        if len(raw.encode()) > 4 * 1024 * 1024:
            raise ValueError("catalog input exceeds size limit")
        source = parse_json(raw.encode("utf-8"))
        if path == "catalog/security.json":
            safety = source
        else:
            retained = retained_entry(source, previous)
            if retained is not None:
                entries.append(retained)
            else:
                if fetch:
                    fetch_artifact(source, artifacts)
                entries.append(build_entry(source, artifacts, host, python, profile))
    result = {
        "format": "amadeus.catalog/v1",
        "sequence": sequence,
        "source_commit": commit,
        "source_time": git(source_repo, "show", "-s", "--format=%cI", commit),
        "generator_commit": generator,
        "host_commit": PIN["host_commit"],
        "entries": sorted(entries, key=lambda e: (e["id"], e["version"])),
        "security": sorted(safety, key=lambda e: (e["id"], e["version"], e["sha256"])),
    }
    return validate_index(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", type=Path, default=ROOT)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument(
        "--approved-ref",
        default="origin/main",
        help="CI pins this to the current protected main commit",
    )
    parser.add_argument("--sequence", type=int, required=True)
    parser.add_argument(
        "--previous",
        type=Path,
        help="Required except for an empty sequence-0 bootstrap",
    )
    parser.add_argument("--host", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch missing wheel bytes over bounded HTTPS; never execute them",
    )
    parser.add_argument(
        "--check", action="store_true", help="Compare output instead of writing it"
    )
    args = parser.parse_args()
    try:
        previous = validate_index(read_json(args.previous)) if args.previous else None
        index = generate(
            args.source_repo,
            args.source_commit,
            args.approved_ref,
            args.sequence,
            args.artifacts.resolve(),
            args.host.resolve(),
            args.python.resolve(),
            args.fetch,
            previous,
        )
        if args.previous:
            validate_transition(previous, index)
        elif index["sequence"] != 0 or index["entries"] or index["security"]:
            raise ValueError(
                "only an empty sequence-0 bootstrap may omit the previous index"
            )
        data = canonical(index)
        if args.check:
            if args.output.read_bytes() != data:
                raise ValueError("generated index differs from committed bytes")
        else:
            args.output.write_bytes(data)
        print(
            json.dumps(
                {
                    "ok": True,
                    "sequence": index["sequence"],
                    "entries": len(index["entries"]),
                }
            )
        )
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError):
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "catalog generation failed; check pins, reviewed input, artifacts and sequence",
                }
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
