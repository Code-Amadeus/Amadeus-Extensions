"""Check index transitions or emit actual wheel content review evidence (no execution)."""

import argparse
import json
import zipfile
from pathlib import Path

from catalog import (
    canonical,
    read_json,
    validate_index,
    validate_transition,
    wheel_diff,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path)
    parser.add_argument("--previous", type=Path)
    parser.add_argument(
        "--wheel", type=Path, help="Digest-verified current artifact to review"
    )
    parser.add_argument(
        "--previous-wheel",
        type=Path,
        help="Previous reviewed artifact; omit for initial full inventory",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if bool(args.index) == bool(args.wheel):
            raise ValueError("choose an index or a wheel")
        if args.index:
            result = validate_index(read_json(args.index))
            if args.previous:
                validate_transition(read_json(args.previous), result)
            payload = {
                "ok": True,
                "sequence": result["sequence"],
                "entries": len(result["entries"]),
            }
        else:
            payload = {
                "ok": True,
                "changes": wheel_diff(args.previous_wheel, args.wheel),
                "review_status": "not_reviewed",
                "note": "Diff is evidence only; every version needs independent full review.",
            }
        if args.output:
            args.output.write_bytes(canonical(payload))
        else:
            print(json.dumps(payload, ensure_ascii=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile):
        print(json.dumps({"ok": False, "error": "invalid catalog or review artifact"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
