import copy
import io
from pathlib import Path

import pytest
import test_catalog
import verify_publication as delivery
from preflight_submission import preflight
from test_catalog import index

from catalog import canonical

host_environment = test_catalog.host_environment


@pytest.mark.parametrize("fragment,admitted", [("notes_mcp", True), ("fish_audio", False)])
def test_real_author_preflight_separates_host_policy_and_review(host_environment, fragment, admitted):
    host, python, _ = host_environment
    wheel = next((host / "build/extension-authoring-review-wheels").glob("*"+fragment+"*.whl"))
    report = preflight(wheel, host, python)
    assert report["ok"] == admitted
    assert report["checks"]["target_host"] == report["checks"]["package_format"] == "passed"
    assert report["checks"]["catalog_policy"] == ("passed" if admitted else "failed")
    assert report["checks"]["human_and_runtime_review"] == "pending"
    assert report["review_status"] == "not_reviewed"


@pytest.fixture
def served(monkeypatch):
    state = {"bytes": b"", "fetches": [], "fail_assets": False}
    class Opener:
        def open(self, *_args, **_kwargs):
            return io.BytesIO(state["bytes"])
    monkeypatch.setattr(delivery, "build_opener", lambda *_: Opener())
    def fetch(source, directory):
        state["fetches"].append(source["wheel"])
        if state["fail_assets"]:
            raise ValueError("artifact digest mismatch")
        path = Path(directory) / "wheel"
        path.write_bytes(b"x"*100)
        return path
    monkeypatch.setattr(delivery, "fetch_artifact", fetch)
    return state


def run_check(tmp_path, served, before, after):
    expected, previous = tmp_path/"index.json", tmp_path/"previous.json"
    expected.write_bytes(canonical(after))
    previous.write_bytes(canonical(before))
    served["bytes"] = canonical(after)
    return delivery.verify("https://catalog.test/index.json", expected, previous)


@pytest.mark.parametrize("change", ["new", "restored", "unblocked", "relocated"])
def test_fresh_check_required_when_distribution_becomes_available(tmp_path, served, change):
    after = index()
    before = copy.deepcopy(after)
    if change == "new":
        before["entries"] = []
    if change == "restored":
        before["entries"][0]["withdrawal"] = {"reason":"copyright","evidence":"https://review.test/"}
    if change == "relocated":
        before["entries"][0]["url"] = "https://old.test/old-1.0.0-py3-none-any.whl"
    if change == "unblocked":
        e = after["entries"][0]
        before["security"] = [{**{k:e[k] for k in ("id","version","sha256")},
                              "status":"blocked","sequence":1,"reason":"security","evidence":"https://review.test/"}]
    report = run_check(tmp_path, served, before, after)
    assert report["ok"] and len(served["fetches"]) == 1


def test_unavailable_old_assets_do_not_block_safety_publication(tmp_path, served):
    after = index()
    after["entries"][0]["withdrawal"] = {"reason":"copyright","evidence":"https://review.test/"}
    served["fail_assets"] = True
    report = run_check(tmp_path, served, {"entries":[], **{k:v for k,v in after.items() if k!="entries"}}, after)
    assert report["ok"] and not served["fetches"]


def test_missing_or_changed_new_asset_is_not_live(tmp_path, served):
    after = index(); before = copy.deepcopy(after); before["entries"] = []
    served["fail_assets"] = True
    with pytest.raises(ValueError, match="digest mismatch"):
        run_check(tmp_path, served, before, after)


def test_valid_but_stale_served_index_is_rejected(tmp_path, served):
    expected = tmp_path/"index.json"
    expected.write_bytes(canonical(index()))
    stale = index(); stale["sequence"] = 0; stale["entries"] = []
    served["bytes"] = canonical(stale)
    with pytest.raises(ValueError, match="served index differs"):
        delivery.verify("https://catalog.test/index.json", expected)
    assert not served["fetches"]
