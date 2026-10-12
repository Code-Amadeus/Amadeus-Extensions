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
