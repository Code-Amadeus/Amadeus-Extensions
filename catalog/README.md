# Curated catalog v1 (experimental, no public store yet)

This directory defines distribution facts, not new extension execution rights.
The sole official index URL will be
`https://raw.githubusercontent.com/Code-Amadeus/Amadeus-Extensions/main/catalog/index.json`
on protected main. There is no signature in v1: repository access,
branch protection, independent review, maintainer 2FA and least-privilege Actions
are the trust root. These publication controls must be verified before S3.
No real package is reviewed or published by the empty sequence-0 bootstrap.

## Inputs and review

Put one JSON file per artifact below `packages/`. Hand-maintained keys are exactly:

```json
{
  "wheel": {"url": "https://example.invalid/package-1.0.0-py3-none-any.whl", "sha256": "<64 lowercase hex>"},
  "publisher": {"id": "publisher", "maintainers": ["author"], "package_ids": ["org.example.package"], "evidence": "https://..."},
  "review": {"sha256": "<same artifact digest>", "policy": "curated-v1", "reviewer": "independent-reviewer", "date": "2026-10-21", "evidence": "https://..."},
  "withdrawal": null
}
```

A reviewer must verify the ownership evidence and independently inspect the
actual wheel using [the public checklist](REVIEW_CHECKLIST.md). Reviewer/maintainer identities are GitHub logins, compared without case. These JSON strings
are review records, not authentication; protected-branch PR approval establishes
their authority. Maintainer examples follow the same independent-review rule.
Every new version is reviewed, including when the source repository appears unchanged.
Never enter a review record merely because automated checks passed.

The generator derives identity, size, author/license/homepage/description, Host
and Python constraints, platform list, dependencies and contribution summaries
from that artifact. It never modifies or adds catalog fields to the manifest.
`policy.json` is the single v1 admission policy used by the catalog tooling.
Fish Audio remains valid for local installation but its third-party dependencies
exclude it from this first catalog. A future dependency closure must pin every
transitive wheel URL/hash and install offline with `--no-index --find-links`
plus `--require-hashes --only-binary=:all:`; this is not implemented in v1.

Artifacts are stored locally as `<sha256>/<original-wheel-filename>`. The optional
`--fetch` path allows HTTPS, system TLS verification, bounded redirects, time and
size, no URL credentials/cookies. It only downloads bytes. Host S1 downloads must
use Electron net; this maintenance tool is not a replacement Host downloader.
Artifact mirrors may supply the same digest-pinned bytes; index mirrors require
future signatures. Never replace the official index trust root with a mirror.

## Fixed checker and publication

`toolchain.json` fixes Host commit, Windows, CPython 3.12.10 and the hash of the
Host's generated minimal dependency list. Obtain that exact Host checkout; the
tools reject a different or modified checker. Install its minimal environment
with `pip --require-hashes`. The Host pin is currently a local experimental commit
and must be pushed/reviewed before GitHub Actions can retrieve it. No SDK or Host
protocol pin is changed by this catalog work.

1. Commit proposed artifact/review/ownership facts. CI uses protected-base tools
   to inspect their bytes without importing or installing package code. Human
   review must finish before the input PR merges into main.
2. A separate publication PR selects an already merged input commit. Select an
   already reviewed generator commit. The generator tree must be clean.
3. Run the fixed generator from that commit, with the current main index as
   `--previous` and the next integer sequence. Source time comes from the input
   commit, never the wall clock. Repeat builds yield identical bytes.

```powershell
python tools/build_catalog.py --source-repo . --source-commit <merged-input-sha> --approved-ref origin/main --sequence <previous-plus-one> --previous <current-main-index.json> --host <pinned-host> --python <minimal-python> --artifacts <artifact-cache> --output catalog/index.json --fetch
python tools/check_catalog.py --index catalog/index.json --previous <current-main-index.json>
python tools/check_catalog.py --wheel <current-wheel> --previous-wheel <previous-reviewed-wheel> --output <review-diff.json>
```

`check_catalog.py` emits additions/removals/changes, text diffs and binary hashes;
initial review emits the whole file inventory. Truncated text diffs are marked:
review the full artifact for those files. Manifest, METADATA/dependencies and
startup scripts appear in the same content diff. Do not treat a diff as approval.

4. Immediately before merging, CI rechecks against current protected main.
   Concurrent publication PRs must rebase and obtain review again. No workflow
   pushes to main or executes submitted plugin code with publication privileges.
   The bootstrap is a separately reviewed code change admitting only an empty
   index; subsequent catalog PRs execute protected-base tooling. Generator changes
   are reviewed before a later PR selects them for publication.

An unchanged index may be rebuilt exactly. A changed index must increment by one,
including content rollback. An existing ID/version cannot disappear or acquire
new bytes; retain it and mark withdrawal. Unchanged reviewed facts may be reused
from the previous protected-main index at the same Host/policy pin. This preserves
security publication when an old download is unavailable; the download/display
cache is never used as authority. New bytes/reviews/ownership or a changed checker
pin still require artifact inspection.

## Withdrawal, safety and future clients

`withdrawal` is null or `{ "reason": "maintainer" | "copyright", "evidence": "https://..." }`.
It stops catalog installation/recommendation, not execution of existing local copies.
`security.json` retains one explicit latest decision per ID/version/SHA-256:
`status` is `blocked` or `allowed`, `reason` is `security` or `security-resolved`,
with evidence and the publication sequence that changed the decision. A known
fact cannot disappear; explicit unban requires a higher publication sequence.
Safety applies to both local and catalog installations. The Host experiment now implements durable settings,
backup recovery and activation enforcement; see its `docs/extension_catalog.md`.
These local changes still require Host integration and release qualification.

Stable index structure is validated without running the full manifest validator.
Unknown contribution kind, role, contract, runtime or delivery makes that entire
package incompatible; compatible neighbors remain visible. Mixed packages are not
partially installed. Security structure is parsed independently of those entries.
Unknown format major, invalid safety structure or identity conflicts reject the
new snapshot, retaining prior safety/high-water facts in S1. Shared examples are
in `fixtures/compatibility.json`; the Python compatibility function specifies the
capability part only. Host API/Python/platform/dependency checks and main-process
installation rechecks are implemented by the Host experiment, separately from this publisher.

Display strings are untrusted plain text. The experimental S2 client renders no remote images and
validates HTTPS homepage links in main before opening an external browser.
Host S3 preparation records fixed old-reader cross-checks; this repository alone
does not certify a released Electron client.

S2 detail views consume generated `display.access`: declared OS access and TTS/MCP deployment, command/arguments or endpoint templates. Configuration defaults, bearer tokens and environment values are excluded. Older entries without this optional display fact remain readable and must show that access details are unavailable until wheel inspection. This does not change catalog format or runtime contracts.


## First catalog review preparation

[Candidate review materials](review-candidates/README.md) inventory exact reference
wheel bytes and static checks. They are not catalog entries or approvals. Keep the
bootstrap empty until independent review, public artifacts, protected publication
and final release qualification are complete. The Host experimental S3 checklist
is `docs/verification/extensions/store-v1.md`; no release is implied by this material.


For author preflight, ownership/transfer, review invalidation, PR responsibilities,
revision and verified distribution, follow the [submission workflow](SUBMISSION.md).
