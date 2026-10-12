"""Canonical SDK builds independently and carries its license at runtime."""
from email.parser import BytesParser
import ast
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import zipfile

from tools.build_sdk import build_sdk

ROOT = Path(__file__).resolve().parents[1]


def test_reproducible_licensed_wheel_installs_offline(tmp_path):
    first = build_sdk(ROOT / "sdk/python", tmp_path / "first")
    second = build_sdk(ROOT / "sdk/python", tmp_path / "second")
    assert hashlib.sha256(first.read_bytes()).digest() == hashlib.sha256(second.read_bytes()).digest()
    with zipfile.ZipFile(first) as wheel:
        metadata_path, = [p for p in wheel.namelist() if p.endswith(".dist-info/METADATA")]
        metadata = BytesParser().parsebytes(wheel.read(metadata_path))
        assert metadata["License-Expression"] == "Apache-2.0"
        assert metadata["License-File"] == "LICENSE"
        assert not metadata.get_all("Requires-Dist")
        license_path = metadata_path.rsplit("/", 1)[0] + "/licenses/LICENSE"
        assert wheel.read(license_path) == (ROOT / "sdk/python/LICENSE").read_bytes()
    environment = tmp_path / "consumer"
    subprocess.run([sys.executable, "-I", "-m", "venv", str(environment)], check=True, capture_output=True)
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run([str(python), "-I", "-m", "pip", "install", "--no-index", "--no-deps", str(first)], check=True, capture_output=True)
    subprocess.run([str(python), "-I", "-c", "from amadeus_extension import Extension, RequestContext, CancelledError; import amadeus_extension.runner; c=RequestContext(); calls=[]; c.on_cancel(lambda: calls.append(True)); c._cancel(); c._cancel(); assert calls == [True]"], cwd=tmp_path, check=True, capture_output=True)


def test_sdk_has_no_host_or_third_party_imports():
    for source in (ROOT / "sdk/python/src").rglob("*.py"):
        for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
            names = [x.name for x in node.names] if isinstance(node, ast.Import) else [node.module or ""] if isinstance(node, ast.ImportFrom) else []
            assert all(name.split(".")[0] in sys.stdlib_module_names | {"amadeus_extension", "__future__"} for name in names)


def test_sdk_archive_is_platform_independent_and_record_matches_bytes(tmp_path):
    import base64
    import csv
    import io
    import stat
    wheel_path = build_sdk(ROOT / "sdk/python", tmp_path)
    with zipfile.ZipFile(wheel_path) as wheel:
        record_path, = [name for name in wheel.namelist() if name.endswith(".dist-info/RECORD")]
        rows = list(csv.reader(io.StringIO(wheel.read(record_path).decode("utf-8"))))
        assert {row[0] for row in rows} == set(wheel.namelist())
        for info in wheel.infolist():
            assert info.create_system == 3
            assert info.external_attr == (stat.S_IFREG | 0o644) << 16
            assert info.date_time == (2023, 11, 14, 22, 13, 20)
            assert info.compress_type == zipfile.ZIP_STORED
            assert not info.extra and not info.comment and info.internal_attr == 0
            assert b"\r\n" not in wheel.read(info)
        for name, digest, size in rows:
            if name == record_path:
                assert digest == size == ""
            else:
                payload = wheel.read(name)
                expected = base64.urlsafe_b64encode(hashlib.sha256(payload).digest()).rstrip(b"=").decode("ascii")
                assert digest == "sha256=" + expected and int(size) == len(payload)
        metadata_path, = [name for name in wheel.namelist() if name.endswith(".dist-info/METADATA")]
        assert b"blob/codex/" not in wheel.read(metadata_path)


def test_windows_and_unix_backend_variants_produce_identical_wheels(tmp_path):
    from tools.build_sdk import _canonicalize_wheel
    names = {
        "amadeus_extension/__init__.py": b"VALUE = 1\n",
        "sdk-0.1.dist-info/METADATA": b"Metadata-Version: 2.4\nName: sdk\nVersion: 0.1\n\nDescription\n",
        "sdk-0.1.dist-info/WHEEL": b"Wheel-Version: 1.0\nRoot-Is-Purelib: true\n",
        "sdk-0.1.dist-info/licenses/LICENSE": b"License text\n",
        "sdk-0.1.dist-info/RECORD": b"stale record from build backend\n",
    }
    outputs = []
    for platform in ["windows", "unix"]:
        raw = tmp_path / (platform + ".whl")
        with zipfile.ZipFile(raw, "w") as wheel:
            entries = list(names.items())
            if platform == "windows":
                entries.reverse()
            for name, data in entries:
                info = zipfile.ZipInfo(name, (2024 if platform == "windows" else 2025, 1, 2, 3, 4, 6))
                info.create_system = 0 if platform == "windows" else 3
                info.external_attr = (0o100666 if platform == "windows" else 0o100644) << 16
                info.internal_attr = 1
                info.comment = b"backend platform comment"
                info.compress_type = zipfile.ZIP_DEFLATED
                wheel.writestr(info, data.replace(b"\n", b"\r\n") if platform == "windows" else data)
        canonical = tmp_path / (platform + "-canonical.whl")
        _canonicalize_wheel(raw, canonical)
        outputs.append(canonical.read_bytes())
    assert outputs[0] == outputs[1]


def test_failed_normalization_keeps_existing_wheel_and_cleans_staging(tmp_path, monkeypatch):
    import pytest
    import tools.build_sdk as build
    first = build_sdk(ROOT / "sdk/python", tmp_path)
    original = first.read_bytes()
    def fail(_source, target):
        target.write_bytes(b"incomplete archive")
        raise OSError("synthetic interrupted normalization")
    monkeypatch.setattr(build, "_canonicalize_wheel", fail)
    with pytest.raises(OSError, match="interrupted normalization"):
        build_sdk(ROOT / "sdk/python", tmp_path)
    assert first.read_bytes() == original
    assert not list(tmp_path.glob(".sdk-*.tmp"))
