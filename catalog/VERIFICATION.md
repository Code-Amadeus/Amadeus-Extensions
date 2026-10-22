# S0 local verification — 2026-10-21

Experimental branch: `codex/extension-community-preview`. Nothing was pushed or
published. The empty `index.json` is a sequence-0 bootstrap, not a reviewed package
listing. Its `source_commit` and `generator_commit` identify the actual committed
generator/input; no wall-clock generation field is used.

The fixed Host checker is `1840c8e4f646992ddaebea3139c8895f29743a8f`, CPython 3.12.10,
Windows. Its authoring dependencies were installed by hash into an independent
environment. The protocol repository's own requirements-dev.txt was also installed
by hash into a separate clean environment (including pytest 9.0.3 and packaging
26.3). No submitted package was imported or installed by catalog tooling.

- Full protocol/SDK/catalog suite: **121 passed, 1 skipped** in that clean environment.
  The skip is Windows symbolic-link creation privilege. After the final case-insensitive
  reviewer check, catalog tests were rerun: **28 passed**.
- Actual Host reference wheels: Handoff, CSV Audit, Notes MCP, desktop theme and
  MiMo generate catalog entries under synthetic review facts. Fish Audio passes
  the same Host checker but is excluded only by the v1 third-party dependency policy.
  Synthetic ownership/review URLs are fixtures only and never enter `packages/`.
- Negative real-wheel variants: altered tags, native suffix/magic, build suffix,
  disclosed npx command, pip module, -c, direct URL and third-party dependency.
  Each remains a separate catalog rejection; generic Host acceptance is unchanged.
- Identity, ownership, independent review (including login case), per-digest review,
  duplicate JSON keys, malformed review date, URL credentials and protocol downgrade
  have rejection cases. Immutable ID/version bytes, sequence conflict/rollback,
  explicit unban and persistent safety facts have transition cases.
- Future kind/role/contract, unknown delivery/runtime and mixed packages have shared
  compatibility fixtures. Legal security records remain parseable beside unknown
  contribution values; bad safety/format/identity rejects the entire new snapshot.
  This is a reference-consumer contract, not a shipped Electron catalog client.
- A committed synthetic input repository was generated twice with the actual fixed
  Host checker: byte-identical output and the input commit timestamp. Corrupting the
  cached artifact was rejected. The empty bootstrap also passed a second --check run.
- Protected-base CI entry point passed locally against unchanged empty index/source.
  GitHub Actions itself was not run: the Host pin must first be made available
  remotely. Workflow has Windows/Python pins, read-only permissions, protected-base
  artifact inspection, independent generator/input ancestry checks, and review diff
  upload. Public branch protection/2FA/reviewer governance remain S3 acceptance.

Run the tests with explicit fixed-checker paths (the implementation branch may
advance while this checker remains pinned):

```powershell
$env:AMADEUS_CATALOG_HOST = '<checkout at 1840c8e>'
$env:AMADEUS_CATALOG_PYTHON = '<its minimal authoring Python>'
python -m pytest -q -rs
```

The generator uses a private wheel snapshot, with size/digest inspection before
policy checks. Unchanged derived facts can be reused only from the prior protected
main index at the same Host/policy pin. This allows withdrawal/security publication
when old assets are unavailable; arbitrary download or display caches confer no trust.

Not implemented here: Host network fetch or mirrors, durable safety settings,
activation bans, store UI, user-triggered update flows, real public review approvals,
repository governance changes, or external-author qualification. No stable SDK or
new runtime contribution is introduced.


## S2 display follow-up (2026-10-21, local experiment)

Commit `58d3892d55c6a7ec6f8626153f503291bb10ab9a` adds optional generated
`display.access` for the Host detail view. It excludes configuration defaults,
environment values and bearer tokens; publication and runtime contracts are unchanged.
Local `tests/test_catalog.py`: 18 passed, 11 skipped because no explicit historical
1840c8e Host checkout was supplied for those cases. Ruff passed. Those skipped fixed
Host checks are not claimed as requalified here.

Host experiment `24d410e47b920d69445a3ced5163df676180321f` pins this generator separately
from its SDK/manifest source and runs the real renderer/IPC/net/installer journey.
Its `docs/verification/extensions/community-preview-batch4-2026-10-21.md` records the
27-check UI qualification with actual reference wheels. Catalog ownership/review data
in that journey is fixture authority, not real approvals. No index publication or main
merge occurred; the bootstrap remains empty. This section supplements the S0 baseline
above, rather than claiming its historical fixed-checker CI has rerun.


## S3 local review preparation (2026-10-21)

`e09f431` adds unreviewed reference dossiers and current client status links.
The eight candidate wheels pass the fixed `1840c8e` exported static checker and
curated-v1 policy; full inventories/candidate-version diffs are recorded under
`review-candidates/`. No catalog approval, ownership claim, artifact URL or safety
publication was added. The bootstrap remains empty.

Host code `ee45e337428de4ccd21d9f0252497a5c49a32270` packages the checker closure and
qualifies actual source and packaged shells with 15 existing shell checks plus
14 plugin checks: theme, mirror update, offline state, Tone Runner and Notes MCP.
Confirmations and index authority are fixtures. Fixed unmodified S1/S2 readers
accept compatible neighbors and understood safety beside future entries. The Host's
`docs/verification/extensions/community-preview-batch5-2026-10-21.md` records hashes,
exact dirty/commit boundaries and limitations. Catalog tests here remain 18 passed,
11 explicitly skipped fixed-checkout cases; exported checker evidence is separate.

Read-only GitHub configuration checks found no main protection/applicable rules,
read-only default workflow tokens with no PR approval permission, and no enforced
organization 2FA. Individual maintainer 2FA is unverified. No settings were changed;
these remain release gates, alongside independent review and public reachable pins.


## Draft integration qualification (2026-10-23)

Before pushing the catalog draft, the full protocol suite at 8fb39ba ran on
Windows / Python 3.12.10 with the explicit historical Host checker and its minimal
hashed environment: **132 passed, 1 skipped** (Windows symlink privilege).
The Host experiment incorporated main 5382b329 and reuses its dependency fixes.
A fresh publisher-only run of the six-phase local Git/HTTPS demonstration passed
input/publication CI, exact rebuild and candidate/live delivery verification in
all phases; malformed submission and publication negatives remained enforced.
Review identities and approvals were synthetic; the public index is still empty.

Host draft must be pushed first so the fixed checker 1840c8e becomes remotely
reachable. Remote Actions results are separate from the local qualification.
No protected-branch change, real publisher approval, public artifact or index
release is authorized by this draft.

Parallel icon protocol PR #4 has no file overlap here, but its optional icon
field is rejected by the current fixed Host checker. After the icon contract
and Host implementation are integrated, qualify a real icon-bearing wheel and
update the fixed checker and dependent pins explicitly; do not infer catalog
acceptance from schema acceptance alone. Host UI PR #255 also overlaps store
settings/IPC files and needs combined UI and admission verification on integration.
