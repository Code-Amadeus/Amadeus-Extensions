"""A new manifest value opts into icons without widening the frozen v0 format."""
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import validate_manifest as vm  # noqa: E402

EXAMPLES = sorted((ROOT / 'examples').glob('*/amadeus-extension.json'))


@pytest.mark.parametrize('example', EXAMPLES, ids=lambda path: path.parent.name)
@pytest.mark.parametrize('schema', ['amadeus.extension/v0', 'amadeus.extension/v1'])
def test_existing_contributions_remain_valid_under_both_versions(example, schema):
    manifest = json.loads(example.read_text(encoding='utf-8'))
    manifest['schema'] = schema
    assert not vm.manifest_issues(manifest)
    assert not vm.package_issues(manifest, example.parent)


@pytest.mark.parametrize('schema', ['amadeus.extension/v0', 'amadeus.extension/v1'])
def test_only_v1_accepts_icon_and_both_versions_reject_unknown_fields(schema):
    manifest = json.loads(EXAMPLES[0].read_text(encoding='utf-8'))
    manifest['schema'] = schema
    manifest['icon'] = 'icon.png'
    assert bool(vm.manifest_issues(manifest)) == (schema == 'amadeus.extension/v0')
    del manifest['icon']
    for target in (manifest, manifest['author']):
        target['undeclared_field'] = 'not an extension point'
        assert {issue.code for issue in vm.manifest_issues(manifest)} == {'schema'}
        del target['undeclared_field']


@pytest.mark.parametrize('schema', ['amadeus.extension/v2', '../v0', '', None, [], {}])
def test_unknown_or_malformed_schema_is_rejected_without_loading_a_path(schema):
    manifest = json.loads(EXAMPLES[0].read_text(encoding='utf-8'))
    manifest['schema'] = copy.deepcopy(schema)
    issues = vm.manifest_issues(manifest)
    assert [(issue.code, issue.path) for issue in issues] == [('schema', '/schema')]
