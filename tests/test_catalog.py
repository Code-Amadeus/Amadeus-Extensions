"""Catalog semantics and actual Host-policy separation; no submitted code executes."""

import copy
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from catalog import (
    PIN,
    ROOT,
    build_entry,
    canonical,
    check_policy,
    https_url,
    incompatible_reasons,
    parse_json,
    retained_entry,
    validate_index,
    validate_transition,
    verify_host,
    wheel_diff,
)


def entry():
    return {
        "id": "org.example.test",
        "version": "1.0.0",
        "sha256": "a" * 64,
        "url": "https://example.test/example-1.0.0-py3-none-any.whl",
        "size": 100,
        "display": {"display_name": "Fixture"},
        "compatibility": {
            "host_api": ">=0.1,<0.2",
            "python": ">=3.12",
            "platforms": ["win32"],
            "sdk": "0.1.0",
            "dependencies": [],
            "delivery": "python-wheel",
            "runtime": "none",
            "contributions": [
                {"kind": "skill", "role": "", "contract": "amadeus.skill/v0"}
            ],
        },
        "publisher": {
            "id": "fixture-author",
            "maintainers": ["fixture-author"],
            "package_ids": ["org.example.test"],
            "evidence": "https://example.test/ownership",
        },
        "review": {
            "sha256": "a" * 64,
            "policy": "curated-v1",
            "reviewer": "independent-fixture-reviewer",
            "date": "2026-10-21",
            "evidence": "https://example.test/review",
        },
        "withdrawal": None,
    }


def index():
    return {
        "format": "amadeus.catalog/v1",
        "sequence": 1,
        "source_commit": "a" * 40,
        "source_time": "2026-10-21T00:00:00+00:00",
        "generator_commit": "b" * 40,
        "host_commit": PIN["host_commit"],
        "entries": [entry()],
        "security": [],
    }


def test_compatibility_is_per_package_while_safety_is_independent():
    source = index()
    capabilities = {
        "delivery": ["python-wheel"],
        "runtime": ["none", "python"],
        "contributions": source["entries"][0]["compatibility"]["contributions"],
    }
    for kind, contract in [("future", "future/v0"), ("skill", "amadeus.skill/v99")]:
        future = copy.deepcopy(entry())
        future["id"] += "." + kind
        future["publisher"]["package_ids"] = [future["id"]]
        future["compatibility"]["contributions"].append(
            {"kind": kind, "role": "", "contract": contract}
        )
        source["entries"].append(future)
    source["security"] = [
        {
            "id": "org.example.future",
            "version": "1.0.0",
            "sha256": "c" * 64,
            "status": "blocked",
            "reason": "security",
            "sequence": 1,
            "evidence": "https://example.test/ban",
        }
    ]
    validate_index(source)
    assert [bool(incompatible_reasons(e, capabilities)) for e in source["entries"]] == [
        False,
        True,
        True,
    ]
    assert source["security"][0]["status"] == "blocked"
    future = copy.deepcopy(entry())
    future["compatibility"]["delivery"] = "future-delivery"
    assert incompatible_reasons(future, capabilities)


@pytest.mark.parametrize(
    "mutation", ["format", "duplicate", "safety", "review", "owner", "self_review"]
)
def test_unsafe_structure_rejects_snapshot(mutation):
    data = index()
    if mutation == "format":
        data["format"] = "amadeus.catalog/v2"
    if mutation == "duplicate":
        data["entries"].append(copy.deepcopy(data["entries"][0]))
    if mutation == "safety":
        data["security"] = [{"status": "unknown"}]
    if mutation == "review":
        data["entries"][0]["review"]["sha256"] = "b" * 64
    if mutation == "owner":
        data["entries"][0]["publisher"]["package_ids"] = ["org.other.package"]
    if mutation == "self_review":
        data["entries"][0]["review"]["reviewer"] = "fixture-author"
    with pytest.raises(ValueError):
        validate_index(data)


def test_publications_are_monotone_immutable_and_preserve_explicit_safety():
    first = index()
    first["security"] = [
        {
            "id": "org.example.test",
            "version": "1.0.0",
            "sha256": "a" * 64,
            "status": "blocked",
            "reason": "security",
            "sequence": 1,
            "evidence": "https://example.test/ban",
        }
    ]
    validate_transition(first, copy.deepcopy(first))
    for mutation in [
        "sequence",
        "bytes",
        "missing",
        "ban_missing",
        "ban_changed_old_sequence",
    ]:
        next_index = copy.deepcopy(first)
        next_index["sequence"] = 2
        if mutation == "sequence":
            next_index["sequence"] = 0
        if mutation == "bytes":
            next_index["entries"][0]["sha256"] = "b" * 64
        if mutation == "missing":
            next_index["entries"] = []
        if mutation == "ban_missing":
            next_index["security"] = []
        if mutation == "ban_changed_old_sequence":
            next_index["security"][0].update(
                status="allowed", reason="security-resolved"
            )
        with pytest.raises(ValueError):
            validate_transition(first, next_index)
    for reason in ["maintainer", "copyright"]:
        next_index = copy.deepcopy(first)
        next_index["sequence"] = 2
        next_index["entries"][0]["withdrawal"] = {
            "reason": reason,
            "evidence": "https://example.test/withdraw",
        }
        validate_transition(first, next_index)
        assert next_index["security"] == first["security"]
    next_index["security"][0].update(
        status="allowed", reason="security-resolved", sequence=2
    )
    validate_transition(first, next_index)


@pytest.mark.parametrize(
    "url",
    [
        "http://example.test/a",
        "https://user:secret@example.test/a",
        "https://example.test/a\n",
        "file:///tmp/a",
    ],
)
def test_urls_cannot_carry_credentials_or_downgrade(url):
    with pytest.raises(ValueError):
        https_url(url)


def test_diff_contains_full_initial_inventory_and_changed_binary_hashes(tmp_path):
    old, new = tmp_path / "old.whl", tmp_path / "new.whl"
    for path, items in [
        (old, {"a.py": b"old\n", "old.txt": b"x", "image.png": b"\xffa"}),
        (new, {"a.py": b"new\n", "new.txt": b"x", "image.png": b"\xffb"}),
    ]:
        with zipfile.ZipFile(path, "w") as z:
            for name, body in items.items():
                z.writestr(name, body)
    changes = {e["path"]: e for e in wheel_diff(old, new)}
    assert (
        changes["old.txt"]["status"] == "removed"
        and changes["new.txt"]["status"] == "added"
    )
    assert (
        "-old" in changes["a.py"]["text_diff"]
        and "+new" in changes["a.py"]["text_diff"]
    )
    assert changes["image.png"]["before"] != changes["image.png"]["after"]
    assert "text_diff" not in changes["image.png"]
    assert len(wheel_diff(None, new)) == 3


@pytest.fixture
def host_environment():
    value = os.environ.get("AMADEUS_CATALOG_HOST")
    if not value:
        pytest.skip("explicit pinned Host checkout required for real artifact checks")
    host = Path(value)
    python = Path(os.environ.get("AMADEUS_CATALOG_PYTHON", sys.executable))
    profile = verify_host(host, python)
    return host, python, profile


def artifact_source(wheel, artifacts):
    digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
    target = artifacts / digest / wheel.name
    target.parent.mkdir(parents=True)
    target.write_bytes(wheel.read_bytes())
    source = entry()
    source["publisher"]["package_ids"] = [
        "com.example.handoff-skill",
        "com.example.csv-audit-skill",
        "com.example.notes-mcp",
        "com.example.desktop-theme",
        "com.example.mimo-tts",
        "com.example.fish-audio",
    ]
    source["review"]["sha256"] = digest
    return {
        "wheel": {"url": "https://example.test/" + wheel.name, "sha256": digest},
        **{k: source[k] for k in ["publisher", "review", "withdrawal"]},
    }


def test_actual_reference_wheels_and_third_party_policy_boundary(
    host_environment, tmp_path
):
    host, python, profile = host_environment
    wheels = list((host / "build/extension-authoring-review-wheels").glob("*.whl"))
    assert len(wheels) == 6
    for wheel in wheels:
        source = artifact_source(wheel, tmp_path)
        if "fish_audio" in wheel.name:
            with pytest.raises(ValueError, match="catalog policy: third-party"):
                build_entry(source, tmp_path, host, python, profile)
        else:
            built = build_entry(source, tmp_path, host, python, profile)
            assert (
                not built["compatibility"]["platforms"]
                or "win32" in built["compatibility"]["platforms"]
            )
            assert built["display"]["author"]
            assert canonical(built) == canonical(
                build_entry(source, tmp_path, host, python, profile)
            )
        # Even Fish remains Host-admissible: catalog policy never changes local rules.
        checked = subprocess.run(
            [
                str(python),
                "-I",
                str(host / "tools/extension_package.py"),
                "check-wheel",
                str(wheel),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert checked.returncode == 0


@pytest.mark.parametrize(
    "defect",
    [
        "tag",
        "native_suffix",
        "native_magic",
        "version",
        "command",
        "module",
        "code",
        "sdk_url",
        "dependency",
    ],
)
def test_catalog_exclusions_on_actual_host_inspected_bytes(
    host_environment, tmp_path, defect
):
    host, python, _ = host_environment
    original = next(
        (host / "build/extension-authoring-review-wheels").glob("*notes_mcp*.whl")
    )
    with zipfile.ZipFile(original) as z:
        content = {n: z.read(n) for n in z.namelist()}
    manifest_path = next(n for n in content if n.endswith("amadeus-extension.json"))
    manifest = json.loads(content[manifest_path])
    metadata_path = next(n for n in content if n.endswith(".dist-info/METADATA"))
    header_path = next(n for n in content if n.endswith(".dist-info/WHEEL"))
    if defect == "tag":
        content[header_path] = (
            b"Wheel-Version: 1.0\nRoot-Is-Purelib: false\nTag: cp312-cp312-win_amd64\n"
        )
    if defect == "native_suffix":
        content["payload.dll"] = b"not even a real DLL"
    if defect == "native_magic":
        content["payload.dat"] = b"MZbinary"
    if defect == "version":
        manifest["version"] = "0.1.0+build"
        content[metadata_path] = content[metadata_path].replace(
            b"Version: 0.1.0", b"Version: 0.1.0+build"
        )
    server = manifest["contributes"]["mcp_server"][0]
    if defect == "command":
        server.update(command="npx", args=["-y", "unreviewed"])
        manifest["permissions"] = {"os": {"process": ["npx"]}}
    if defect == "module":
        server["args"] = ["-m", "pip", "install", "unreviewed"]
    if defect == "code":
        server["args"] = ["-c", "print(1)"]
    if defect in {"sdk_url", "dependency"}:
        # Add a header before the blank metadata/body separator.
        requirement = (
            b"other @ https://example.test/unreviewed.whl"
            if defect == "sdk_url"
            else b"other==1.0"
        )
        content[metadata_path] = (
            b"Requires-Dist: " + requirement + b"\n" + content[metadata_path]
        )
    content[manifest_path] = json.dumps(manifest).encode()
    wheel = tmp_path / original.name
    with zipfile.ZipFile(wheel, "w") as z:
        for name, body in content.items():
            z.writestr(name, body)
    checked = subprocess.run(
        [
            str(python),
            "-I",
            str(host / "tools/extension_package.py"),
            "check-wheel",
            str(wheel),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert checked.returncode == 0, (
        checked.stdout
    )  # legitimate local behavior is preserved
    with pytest.raises(ValueError, match="catalog policy:"):
        check_policy(wheel, json.loads(checked.stdout))


def test_shared_future_client_fixtures():
    fixture = json.loads(
        (ROOT / "catalog/fixtures/compatibility.json").read_text(encoding="utf-8")
    )
    for case in fixture["cases"]:
        assert (
            not incompatible_reasons(
                {"compatibility": case["compatibility"]}, fixture["capabilities"]
            )
        ) == case["compatible"], case["name"]


def test_safety_publication_reuses_reviewed_main_facts_without_redownloading():
    previous = index()
    old = previous["entries"][0]
    source = {
        "wheel": {"url": old["url"], "sha256": old["sha256"]},
        "publisher": old["publisher"],
        "review": old["review"],
        "withdrawal": {
            "reason": "copyright",
            "evidence": "https://example.test/takedown",
        },
    }
    retained = retained_entry(source, previous)
    assert retained["withdrawal"]["reason"] == "copyright"
    assert retained["compatibility"] == old["compatibility"]
    source["wheel"]["sha256"] = "b" * 64
    assert retained_entry(source, previous) is None


def test_duplicate_keys_and_invalid_review_dates_are_rejected():
    with pytest.raises(ValueError):
        parse_json(b'{"sequence":1,"sequence":2}')
    data = index()
    data["entries"][0]["review"]["date"] = "2026-99-99"
    with pytest.raises(ValueError):
        validate_index(data)


def test_committed_generator_is_reproducible_and_checks_actual_digest(
    host_environment, tmp_path
):
    from build_catalog import generate

    host, python, _ = host_environment
    source_repo = tmp_path / "inputs"
    source_repo.mkdir()
    subprocess.run(["git", "init", str(source_repo)], check=True, capture_output=True)
    source = artifact_source(
        next(
            (host / "build/extension-authoring-review-wheels").glob("*notes_mcp*.whl")
        ),
        tmp_path / "artifacts",
    )
    packages = source_repo / "catalog/packages"
    packages.mkdir(parents=True)
    (packages / "notes.json").write_text(json.dumps(source), encoding="utf-8")
    (source_repo / "catalog/security.json").write_text("[]", encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(source_repo), "add", "."], check=True, capture_output=True
    )
    environment = {
        **os.environ,
        "GIT_AUTHOR_DATE": "2026-10-21T12:00:00+13:00",
        "GIT_COMMITTER_DATE": "2026-10-21T12:00:00+13:00",
    }
    subprocess.run(
        [
            "git",
            "-C",
            str(source_repo),
            "-c",
            "user.name=Catalog fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-m",
            "Synthetic input only",
        ],
        check=True,
        capture_output=True,
        env=environment,
    )
    previous = index()
    previous.update(sequence=0, entries=[])
    first = generate(
        source_repo,
        "HEAD",
        "HEAD",
        1,
        tmp_path / "artifacts",
        host,
        python,
        previous=previous,
    )
    second = generate(
        source_repo,
        "HEAD",
        "HEAD",
        1,
        tmp_path / "artifacts",
        host,
        python,
        previous=previous,
    )
    assert canonical(first) == canonical(second)
    assert first["source_time"] == "2026-10-21T12:00:00+13:00"
    validate_transition(previous, first)
    wheel = next((tmp_path / "artifacts").glob("*/*.whl"))
    wheel.write_bytes(b"wrong artifact")
    with pytest.raises(ValueError, match="digest mismatch"):
        generate(
            source_repo,
            "HEAD",
            "HEAD",
            1,
            tmp_path / "artifacts",
            host,
            python,
            previous=previous,
        )


def test_github_reviewer_identity_is_case_insensitive():
    data = index()
    data["entries"][0]["review"]["reviewer"] = "FIXTURE-AUTHOR"
    with pytest.raises(ValueError, match="independent reviewer"):
        validate_index(data)


def test_display_is_derived_without_config_defaults_or_environment_values():
    from catalog import artifact_display

    manifest = {
        "display_name": "Fixture",
        "description": "<script>plain text</script>",
        "config": {"credential": {"default": "synthetic-private-value"}},
        "permissions": {"os": {"network": ["example.test"]}},
        "contributes": {
            "mcp_server": [
                {
                    "id": "notes",
                    "transport": "stdio",
                    "command": "${python}",
                    "args": ["-m", "notes"],
                    "env": {"TOKEN": "synthetic-private-value"},
                }
            ]
        },
    }
    result = artifact_display(manifest)
    assert result["access"]["services"][0]["command"] == "${python}"
    assert result["access"]["os"] == manifest["permissions"]["os"]
    assert "synthetic-private-value" not in json.dumps(result)
    assert result["description"] == manifest["description"]
