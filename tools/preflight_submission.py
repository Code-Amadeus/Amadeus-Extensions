"""Author preflight: reuse pinned Host admission and curated policy without approval."""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from catalog import PIN, canonical, check_policy, verify_host, wheel_diff


def preflight(wheel, host, python):
    report = {
        "ok": False, "review_status": "not_reviewed", "host_commit": PIN["host_commit"],
        "checks": {"package_format": "not_established", "target_host": "not_established",
                   "catalog_policy": "not_run", "human_and_runtime_review": "pending"},
    }
    try:
        profile = verify_host(host, python)
        with tempfile.TemporaryDirectory(prefix="submission-preflight-") as temporary:
            snapshot = Path(temporary) / wheel.name
            shutil.copyfile(wheel, snapshot)
            digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
            result = subprocess.run(
                [str(python), "-I", str(host / "tools/extension_package.py"),
                 "check-wheel", str(snapshot)],
                capture_output=True, text=True, encoding="utf-8", timeout=60,
            )
            inspection = json.loads(result.stdout)
            if result.returncode or not inspection.get("ok"):
                report["checks"]["target_host"] = "failed"
                # Fixed Host's JSON is sanitized; never include process stderr/config.
                report["host_diagnostic"] = {key: inspection[key] for key in
                    ("error", "errors", "checked", "not_checked", "unavailable") if key in inspection}
                report["next_step"] = "Resolve the fixed Host check-wheel diagnostic, then repeat preflight."
                return report
            if inspection["digest"] != digest:
                raise ValueError("wheel changed during inspection")
            report.update(identity={"id": inspection["manifest"]["id"],
                "version": inspection["manifest"]["version"], "sha256": digest},
                environment={"python": profile["python"], "platform": profile["platform"]},
                checked=inspection["checked"], not_checked=inspection["not_checked"])
            # One owner checks both boundaries; a failure is not guessed to be format-valid.
            report["checks"].update(package_format="passed", target_host="passed")
            try:
                check_policy(snapshot, inspection)
            except ValueError as exc:
                report["checks"]["catalog_policy"] = "failed"
                report["policy_diagnostic"] = str(exc)
                report["next_step"] = "Fix this curated-policy violation; Host/local admission may still be valid."
                return report
            report["checks"]["catalog_policy"] = "passed"
            report["inventory"] = wheel_diff(None, snapshot)
            report["ok"] = True
            report["next_step"] = "Attach this report to the submission PR; ownership, rights, runtime and independent review remain required."
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        report["error"] = str(exc)
        report["next_step"] = "Check the wheel path and pinned Windows/Python/checker environment."
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--host", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = preflight(args.wheel.resolve(), args.host.resolve(), args.python.resolve())
    args.output.write_bytes(canonical(report))
    print(json.dumps({"ok": report["ok"], "checks": report["checks"], "review_status": "not_reviewed"}))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
