"""Build the trusted SDK offline with the project's installed build backend.

Only bundled first-party sources are built. Third-party extensions still use
wheel-only installation; neither this command nor the installer fetches an SDK.
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def _canonicalize_wheel(source: Path, target: Path) -> None:
    """Remove backend OS differences; rebuild RECORD from the delivered bytes.

    This is the small stdlib SDK's build output, not an extension installer.
    Stored ZIP entries avoid a dependency on the host's zlib implementation.
    """
    with zipfile.ZipFile(source) as archive:
        records = [name for name in archive.namelist() if name.endswith('.dist-info/RECORD')]
        if len(records) != 1:
            raise ValueError('SDK wheel must have exactly one RECORD')
        record = records[0]
        contents = {}
        for member in archive.infolist():
            if member.is_dir() or member.filename == record:
                continue
            payload = archive.read(member)
            if (member.filename.endswith(('.py', '.txt'))
                    or Path(member.filename).name in {'METADATA', 'WHEEL', 'LICENSE'}):
                payload = payload.replace(b'\r\n', b'\n')
            contents[member.filename] = payload
    rows = io.StringIO(newline='')
    writer = csv.writer(rows, lineterminator='\n')
    for name in sorted(contents):
        payload = contents[name]
        digest = base64.urlsafe_b64encode(hashlib.sha256(payload).digest()).rstrip(b'=').decode('ascii')
        writer.writerow((name, 'sha256=' + digest, len(payload)))
    writer.writerow((record, '', ''))
    contents[record] = rows.getvalue().encode('utf-8')
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name in [*sorted(name for name in contents if name != record), record]:
            info = zipfile.ZipInfo(name, date_time=(2023, 11, 14, 22, 13, 20))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, contents[name])


def build_sdk(source: Path, output: Path) -> Path:
    output.mkdir(parents=True, exist_ok=True)
    # Build away from sources; setuptools must not leave build/egg-info in a
    # source archive or consume a stale local build of the package.
    with tempfile.TemporaryDirectory(prefix='amadeus-sdk-') as temporary:
        work = Path(temporary)
        package = work / 'source'
        package.mkdir()
        for filename in ('pyproject.toml', 'README.md', 'LICENSE'):
            shutil.copy2(source / filename, package / filename)
        shutil.copytree(source / 'src', package / 'src',
            ignore=shutil.ignore_patterns('__pycache__', '*.egg-info'))
        wheels = work / 'wheels'
        result = subprocess.run([sys.executable, '-I', '-c',
            'import sys; from setuptools.build_meta import build_wheel; build_wheel(sys.argv[1])',
            str(wheels)], cwd=package, capture_output=True, text=True, encoding='utf-8',
            env={**os.environ, 'SOURCE_DATE_EPOCH': '1700000000'})
        if result.returncode:
            raise RuntimeError('SDK build failed. Install requirements-dev.txt in the build environment '
                '(setuptools and wheel must be installed).\n' + result.stderr)
        built = list(wheels.glob('*.whl'))
        if len(built) != 1:
            raise RuntimeError('SDK build did not produce exactly one wheel')
        target = output / built[0].name
        # The installer may be reading the previous build. Replace only a
        # complete wheel, without removing the existing one on build failure.
        with tempfile.NamedTemporaryFile(dir=output, prefix='.sdk-', suffix='.tmp', delete=False) as staging:
            staging_path = Path(staging.name)
        try:
            _canonicalize_wheel(built[0], staging_path)
            os.replace(staging_path, target)
        finally:
            staging_path.unlink(missing_ok=True)
        return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'dist')
    arguments = parser.parse_args()
    print(build_sdk(ROOT / 'sdk/python', arguments.output_dir.resolve()))
