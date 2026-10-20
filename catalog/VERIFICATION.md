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
