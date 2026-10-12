"""Tests for the v0.1 manifest schema, semantic rules, and example packages."""

from __future__ import annotations

import copy
import json
import os
import shutil
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import validate_manifest as vm  # noqa: E402


EXAMPLES = sorted(path.parent for path in (ROOT / "examples").glob(f"*/{vm.MANIFEST_NAME}"))


def example(name: str) -> dict:
    return json.loads((ROOT / "examples" / name / vm.MANIFEST_NAME).read_text(encoding="utf-8"))


def codes(manifest: dict) -> set[str]:
    return {issue.code for issue in vm.manifest_issues(manifest)}


def _set(path: list, value: object):
    def mutate(manifest: dict) -> None:
        target = manifest
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = copy.deepcopy(value)

    return mutate


def _delete(path: list):
    def mutate(manifest: dict) -> None:
        target = manifest
        for key in path[:-1]:
            target = target[key]
        del target[path[-1]]

    return mutate


HTTP_SERVER = {
    "id": "weather",
    "contract": "amadeus.mcp-server/v0",
    "transport": "http",
    "url": "https://mcp.example.com/weather",
}


def test_schema_is_a_valid_draft_2020_12_schema():
    vm._validator()


@pytest.mark.parametrize("package", EXAMPLES, ids=lambda path: path.name)
def test_example_packages_are_valid(package):
    assert vm.validate_path(package) == []


def test_examples_cover_every_contribution_kind():
    kinds = set()
    for package in EXAMPLES:
        kinds.update(example(package.name)["contributes"])
    assert kinds == set(json.loads(vm.SCHEMA_PATH.read_text(encoding='utf-8'))['$defs']['contributes']['properties'])


SCHEMA_REJECTIONS = {
    "unknown top-level field": ("mimo-tts", _set(["extra"], True)),
    "reserved amadeus id prefix": ("mimo-tts", _set(["id"], "amadeus.mimo-tts")),
    "single-segment id": ("mimo-tts", _set(["id"], "mimo-tts")),
    "version is not semver": ("mimo-tts", _set(["version"], "1.0")),
    "host api range uses caret": ("mimo-tts", _set(["engines", "amadeus_host_api"], "^0.1")),
    "unknown platform": ("mimo-tts", _set(["engines", "platforms"], ["android"])),
    "python runtime without requires_python": ("mimo-tts", _delete(["runtime", "requires_python"])),
    "none runtime with entry": ("paper-review-skills", _set(["runtime", "entry"], "pkg:extension")),
    "unknown contribution kind": ("mimo-tts", _set(["contributes", "surface"], [{"id": "panel"}])),
    "empty contributes": ("mimo-tts", _set(["contributes"], {})),
    "tts with asr contract": (
        "mimo-tts", _set(["contributes", "voice_backend", 0, "contract"], "amadeus.voice.asr/v0")
    ),
    "tts without languages": ("mimo-tts", _delete(["contributes", "voice_backend", 0, "languages"])),
    "secret with default": ("mimo-tts", _set(["config", "api_key", "default"], "placeholder")),
    "secret on enum field": ("mimo-tts", _set(["config", "voice", "secret"], True)),
    "enum without options": ("mimo-tts", _delete(["config", "voice", "options"])),
    "options on string field": ("mimo-tts", _set(["config", "model", "options"], ["a"])),
    "min on string field": ("mimo-tts", _set(["config", "model", "min"], 1)),
    "integer field with fractional default": ("memory-recall", _set(["config", "max_items", "default"], 2.5)),
    "config field without title": ("mimo-tts", _delete(["config", "model", "title"])),
    "unknown host capability": ("memory-recall", _set(["permissions", "host", 0, "capability"], "files:read")),
    "host capability without reason": ("memory-recall", _delete(["permissions", "host", 0, "reason"])),
    "skill path escapes package": ("paper-review-skills", _set(["contributes", "skill", 0, "path"], "../outside")),
    "skill path is absolute": ("paper-review-skills", _set(["contributes", "skill", 0, "path"], "/etc/skills")),
    "http bearer token is a literal": (
        "notes-mcp", _set(["contributes", "mcp_server", 0], {**HTTP_SERVER, "bearer_token": "plain-token"})
    ),
    "context deadline above limit": ("memory-recall", _set(["contributes", "context_source", 0, "deadline_ms"], 5000)),
    "unknown observer topic": ("task-notifier", _set(["contributes", "observer", 0, "topics"], ["chat.token"])),
    "network pattern with scheme": ("mimo-tts", _set(["permissions", "os", "network"], ["https://api.example.com"])),
}


@pytest.mark.parametrize("name", sorted(SCHEMA_REJECTIONS))
def test_schema_rejections(name):
    package, mutate = SCHEMA_REJECTIONS[name]
    manifest = example(package)
    mutate(manifest)
    assert codes(manifest) == {"schema"}


def _append_duplicate(path: list):
    def mutate(manifest: dict) -> None:
        target = manifest
        for key in path:
            target = target[key]
        target.append(copy.deepcopy(target[0]))

    return mutate


def _secret_in_args(manifest: dict) -> None:
    manifest["config"]["token"] = {"type": "string", "title": "Token", "secret": True}
    manifest["contributes"]["mcp_server"][0]["args"].append("--token=${config.token}")


def _bearer_not_secret(manifest: dict) -> None:
    manifest["config"]["token"] = {"type": "string", "title": "Token"}
    manifest["contributes"]["mcp_server"][0] = {**HTTP_SERVER, "bearer_token": "${config.token}"}


def _python_template_without_runtime(manifest: dict) -> None:
    manifest["contributes"]["mcp_server"] = [
        {
            "id": "tool",
            "contract": "amadeus.mcp-server/v0",
            "transport": "stdio",
            "command": "${python}",
            "args": ["-m", "tool"],
        }
    ]


SEMANTIC_REJECTIONS = {
    "duplicate contribution id": (
        "mimo-tts", _append_duplicate(["contributes", "voice_backend"]), "S1.duplicate_contribution_id"
    ),
    "runner kind without entry": ("mimo-tts", _delete(["runtime", "entry"]), "S2.runner_required"),
    "runner kind with none runtime": ("mimo-tts", _set(["runtime"], {"kind": "none"}), "S2.runner_required"),
    "undefined config reference": (
        "notes-mcp",
        _set(["contributes", "mcp_server", 0, "env", "NOTES_LIMIT"], "${config.missing}"),
        "S3.undefined_config",
    ),
    "unknown template variable": (
        "notes-mcp", _set(["contributes", "mcp_server", 0, "env", "HOME_DIR"], "${home}"), "S3.unknown_variable"
    ),
    "unterminated template": (
        "notes-mcp", _set(["contributes", "mcp_server", 0, "env", "NOTES_DIR"], "${data"), "S3.unterminated_variable"
    ),
    "secret in args": ("notes-mcp", _secret_in_args, "S3.secret_position"),
    "bearer token from non-secret field": ("notes-mcp", _bearer_not_secret, "S3.bearer_not_secret"),
    "python template without python runtime": (
        "paper-review-skills", _python_template_without_runtime, "S4.python_without_runtime"
    ),
    "observer topic without capability": (
        "task-notifier", _delete(["permissions", "host", 0]), "S5.capability_not_requested"
    ),
    "enum default not in options": ("mimo-tts", _set(["config", "voice", "default"], "Nobody"), "S6.default_not_in_options"),
    "duplicate enum option": ("mimo-tts", _append_duplicate(["config", "voice", "options"]), "S6.duplicate_option"),
    "integer default out of range": (
        "memory-recall", _set(["config", "max_items", "default"], 99), "S6.default_out_of_range"
    ),
    "inverted numeric range": ("memory-recall", _set(["config", "max_items", "min"], 20), "S6.invalid_range"),
    "default longer than max_length": ("mimo-tts", _set(["config", "model", "max_length"], 4), "S6.default_too_long"),
    "duplicate host capability": (
        "task-notifier", _append_duplicate(["permissions", "host"]), "S7.duplicate_capability"
    ),
    "command outside package": (
        "notes-mcp", _set(["contributes", "mcp_server", 0, "command"], "C:/tools/server.exe"), "S8.command_location"
    ),
    "package command escapes": (
        "notes-mcp", _set(["contributes", "mcp_server", 0, "command"], "${package}/../server"), "S8.command_location"
    ),
    "undisclosed bare command": (
        "notes-mcp", _set(["contributes", "mcp_server", 0, "command"], "node"), "S8.undisclosed_process"
    ),
    "entry without runner kinds": (
        "notes-mcp", _set(["runtime", "entry"], "example_notes_mcp:extension"), "S9.unused_entry"
    ),
}


@pytest.mark.parametrize("name", sorted(SEMANTIC_REJECTIONS))
def test_semantic_rejections(name):
    package, mutate, expected = SEMANTIC_REJECTIONS[name]
    manifest = example(package)
    mutate(manifest)
    assert vm.schema_issues(manifest) == []
    assert expected in codes(manifest)


def test_secret_may_reach_env_and_bearer_token():
    manifest = example("notes-mcp")
    manifest["config"]["token"] = {"type": "string", "title": "Token", "secret": True, "required": True}
    manifest["contributes"]["mcp_server"][0]["env"]["NOTES_TOKEN"] = "${config.token}"
    manifest["contributes"]["mcp_server"].append({**HTTP_SERVER, "bearer_token": "${config.token}"})
    assert vm.manifest_issues(manifest) == []


def test_disclosed_bare_command_is_accepted():
    manifest = example("notes-mcp")
    manifest["contributes"]["mcp_server"][0]["command"] = "node"
    manifest["permissions"] = {"os": {"process": ["node"]}}
    assert vm.manifest_issues(manifest) == []


def _copy_example(tmp_path: Path, name: str) -> Path:
    target = tmp_path / name
    shutil.copytree(ROOT / "examples" / name, target)
    return target


def test_missing_skill_file_is_rejected(tmp_path):
    package = _copy_example(tmp_path, "paper-review-skills")
    (package / "skills" / "paper-review" / "SKILL.md").unlink()
    assert [issue.code for issue in vm.validate_path(package)] == ["P2.missing_skill"]


def test_manifest_file_alone_skips_package_checks(tmp_path):
    package = _copy_example(tmp_path, "paper-review-skills")
    (package / "skills" / "paper-review" / "SKILL.md").unlink()
    assert vm.validate_path(package / vm.MANIFEST_NAME) == []


def test_link_inside_skill_is_rejected(tmp_path):
    package = _copy_example(tmp_path, "paper-review-skills")
    outside = tmp_path / "outside.txt"
    outside.write_text("outside the package", encoding="utf-8")
    try:
        os.symlink(outside, package / "skills" / "paper-review" / "linked.txt")
    except OSError:
        pytest.skip("this account cannot create symbolic links")
    assert [issue.code for issue in vm.validate_path(package)] == ["P2.link_in_package"]


def test_missing_package_command_is_rejected(tmp_path):
    package = _copy_example(tmp_path, "notes-mcp")
    manifest = example("notes-mcp")
    manifest["contributes"]["mcp_server"][0]["command"] = "${package}/bin/server"
    (package / vm.MANIFEST_NAME).write_text(json.dumps(manifest), encoding="utf-8")
    assert [issue.code for issue in vm.validate_path(package)] == ["P3.missing_file"]


def test_byte_order_mark_is_rejected(tmp_path):
    manifest_path = tmp_path / vm.MANIFEST_NAME
    manifest_path.write_bytes(b"\xef\xbb\xbf" + json.dumps(example("mimo-tts")).encode("utf-8"))
    assert [issue.code for issue in vm.validate_path(manifest_path)] == ["P1.invalid_json"]


def test_command_line_exit_status(tmp_path, capsys):
    assert vm.main([str(package) for package in EXAMPLES]) == 0
    broken = tmp_path / vm.MANIFEST_NAME
    broken.write_text(json.dumps({"schema": "amadeus.extension/v0"}), encoding="utf-8")
    assert vm.main([str(broken)]) == 1
    assert "invalid" in capsys.readouterr().out


@pytest.mark.parametrize('name,value,code', [
    ('--danger', '#111111', 'T1.reserved_token'),
    ('--bg', 'url(https://example.invalid)', 'T2.css_input'),
    ('--font', 'Arial; color:red', 'T2.css_input'),
])
def test_theme_cannot_override_status_or_inject_css(name, value, code):
    manifest = example('desktop-theme')
    manifest['contributes']['theme'][0]['tokens'][name] = value
    assert code in codes(manifest)


def test_theme_background_requires_a_contained_package_file(tmp_path):
    manifest = example('desktop-theme')
    manifest['contributes']['theme'][0]['background'] = {'image': 'bg.png', 'fit': 'cover', 'dim': .4}
    assert not codes(manifest)
    assert {issue.code for issue in vm.package_issues(manifest, tmp_path)} == {'P3.missing_file'}
    (tmp_path / 'bg.png').write_bytes(b'Host separately validates image encoding and decoded dimensions')
    assert 'P4.theme_image' in {issue.code for issue in vm.package_issues(manifest, tmp_path)}
    (tmp_path / 'bg.png').write_bytes(b'\x89PNG\r\n\x1a\n' + b'header-only fixture; full decoding remains Host-owned')
    assert not vm.package_issues(manifest, tmp_path)
    manifest['contributes']['theme'][0]['background']['image'] = '../bg.png'
    assert 'schema' in codes(manifest)


@pytest.mark.parametrize('name,value', [
    ('--unknown', '#123456'), ('--bg', 'image-set("x.png" 1x)'),
    ('--bg', 'expression(alert(1))'), ('--bg', 'red'), ('--bg', 'rgb(256 0 0)'),
    ('--bg', 'hsl(10 101% 20%)'), ('--bg', '#12345'), ('--bg', 'rgba(1,2,3,1.1)'),
    ('--font', 'Arial, serif'), ('--font', '</style>'),
])
def test_theme_rejects_unknown_tokens_and_non_literal_values(name, value):
    manifest = example('desktop-theme')
    manifest['contributes']['theme'][0]['tokens'][name] = value
    assert codes(manifest)


@pytest.mark.parametrize('color', ['#123', '#1234', '#123456', '#12345678',
    'rgb(10 20 30 / 50%)', 'rgba(10, 20, 30, .5)', 'hsl(-30deg 80% 20%)'])
def test_theme_color_literals_match_host_grammar(color):
    manifest=example('desktop-theme')
    manifest['contributes']['theme'][0]['tokens']['--bg']=color
    assert not codes(manifest)


@pytest.mark.parametrize('font', ['"Segoe UI"', "'Noto Sans'", '微软雅黑'])
def test_single_quoted_or_unicode_font_family_syntax(font):
    manifest = example('desktop-theme')
    manifest['contributes']['theme'][0]['tokens']['--font'] = font
    assert not codes(manifest)

@pytest.mark.parametrize('group', ['accepted', 'rejected'])
def test_shared_css_literal_cases(group):
    cases = json.loads((ROOT / 'tests/fixtures/theme-color-literals.json').read_text(encoding='utf-8-sig'))
    for color in cases[group]:
        assert vm._theme_color_literal(color) is (group == 'accepted'), color


def test_theme_v0_rejects_webp_declaration_and_bytes(tmp_path):
    manifest = example('desktop-theme')
    manifest['contributes']['theme'][0]['background'] = {'image': 'bg.webp', 'fit': 'cover', 'dim': .4}
    (tmp_path / 'bg.webp').write_bytes(b'RIFF' + b'\0' * 4 + b'WEBP' + b'fixture')
    assert codes(manifest)
    assert 'P4.theme_image' in {issue.code for issue in vm.package_issues(manifest, tmp_path)}
