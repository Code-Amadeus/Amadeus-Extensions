# Submission and publication operations (curated-v1)

This guide is executable workflow guidance for the experimental catalog. The
public main branch may still have no catalog. An empty bootstrap or automated
preflight does not approve a package. Runtime contracts and curated-v1 admission
are separate: a valid locally installable package can be ineligible for this store.

## Author: submit once, revise the same PR

Before building, read policy.json and REVIEW_CHECKLIST.md. V1 accepts X.Y.Z,
py3-none-any, no effective dependencies except the compatible SDK, and reviewed
package/Python commands only. Fish Audio with third-party dependencies currently
belongs to local installation. Do not remove needed dependencies to pass the store.

Run the fixed Windows/CPython/checker environment from toolchain.json:

~~~powershell
python tools/preflight_submission.py --wheel <wheel> --host <fixed-host> --python <checker-python> --output preflight.json
~~~

The report distinguishes package-format and target-Host acceptance (the same
Host owner checks both), curated policy, and pending human/runtime review. On Host
failure it does not claim that the package format passed. It never imports package
code, invents an approval or requires authors to maintain derived catalog metadata.

Open one submission PR using the short catalog template:
- Link the versioned wheel and attach preflight.json; do not retype its metadata.
- Link source/build and basic usage/validation evidence.
- On first submission, link ownership and code/asset rights evidence. Reuse the
  established evidence on updates unless control or rights changed.
- On updates, summarize changes and any access/configuration/data migration steps.
  If there are no breaking changes, say so; no separate migration report is needed.

The author revises this same PR. Maintainers prepare catalog JSON and the second,
possibly batched publication PR. No account dashboard, second author form, separate
status report or mandatory fixed set of attachments is required. Existing README,
release notes, build logs and license files can provide the evidence directly.

The author does not populate a fictional reviewer or grant themselves approval.
A draft PR may contain materials before catalog/packages facts are complete;
required catalog CI can remain failing while those facts are incomplete. The
authorized independent reviewer adds the final existing review fields only after
review. Reports/attachments are evidence, not runtime manifest or catalog fields.

## Ownership and responsible people

For first ownership, establish control of the source repository/artifact publishing
location and proposed namespace from existing repository/release evidence. Ask for
a repository challenge only when that evidence leaves control ambiguous.
A display author name, matching PR account, fork or preflight alone is insufficient.
Record evidence in publisher.evidence and the PR. Inspect links independently.

For updates, use the previously reviewed publisher/maintainer record. A submitter
outside that set needs explicit authorization from a recorded maintainer, verified
through the established source/account channel. For transfers, obtain the current
holder's authorization and the recipient's acceptance; review changed control and
record the evidence. Silence, abandoned appearance or an unavailable URL is not
authorization to transfer. Disputes wait for an explicit decision.

Maintainers assign one contact/reviewer to carry the submission through publication.
Review and publication may be handled by the same eligible maintainer; backup is
an internal team arrangement, not another person the author must recruit. A reviewer
cannot be an author or publisher maintainer. If nobody eligible is available, say
what is waiting. No fabricated identities, timeout approval or self-review.

Use existing PR review states and cross-links; labels are optional convenience:
needs-preflight → needs-review → changes-requested → approved-awaiting-publication
→ published. Labels communicate status; protected-branch review is the authority.
The triage assignee updates the next responsible person and missing evidence.
No promised review SLA; security actions do not wait for ordinary release batches.

## Review and invalidation

Approval covers exact wheel SHA-256, curated policy, fixed checker/environment,
ownership/rights and runtime evidence at the reviewed PR head. Material changes to
bytes, URL/control, rights or qualification invalidate the affected evidence and
need relevant checks and renewed non-author review. A wording-only correction
must not force another full runtime qualification. Every
new version requires review. Configure dismiss-stale-approvals and approval after
the last push on the real protected branch before public release.

Approval to execute tests in an isolated environment is NOT approval to publish.
Never run submitted package code in a write-credential/publishing job. The wheel
inventory/diff and author report assist, but do not replace, the public checklist.
A changes-requested PR stays open; revisions and fresh preflight attach to the
same PR. The reviewer records which prior evidence/approval was superseded.

## Publication owner: input PR → publication PR → verified delivery

1. Merge reviewed inputs only after required checks and independent approval.
2. Prepare a separate publication PR from that committed input and reviewed
   generator. Link each included submission/withdrawal/security decision and list
   exact ID/version/digest, next sequence and current-main base. The author does
   not need to author this second PR.
3. Follow catalog/README.md for build_catalog.py, check_catalog.py and protected-base
   check_catalog_ci.py. Rebuild after any main movement; repeat approval as required.
4. Use verify_publication.py against a candidate endpoint and expected generated
   file before release, then the client's exact official index URL after merge.
   Use an empty fresh artifact cache (the tool always does this). Only mark
   published after the live bytes and newly distributed/relocated assets pass.

~~~powershell
python tools/verify_publication.py --index-url <official-index-url> --expected catalog/v1/index.json --previous <previous-index.json> --output delivery.json
~~~

The explicit expected file pins the sequence/content; a stale or different served
index fails even if otherwise valid. Newly available versions, restored distribution,
unblocked assets and changed URLs are freshly downloaded and digest/size checked.
Unchanged available versions may be skipped. Withdrawn/blocked assets are skipped:
an unavailable old wheel must not prevent a safety-only publication. Record skipped
scope honestly. Availability is a point-in-time check, not an uptime guarantee.
The publication owner links the receipt back to submissions; only then applies
published status and notifies authors through the normal authorized review process.

## Source failures, complaints and recovery

Use versioned asset URLs, never mutable latest aliases. Immutable release assets
are preferred; content hashes remain mandatory. A broken URL may change through a
reviewed input PR only if ID/version/digest remain the same; confirm new hosting
control and fresh download. Different bytes always require a new version.
No silent URL rewrite or replacement of the official index trust root.

Triage download failures via an ordinary catalog issue with ID/version/digest,
stage and sanitized error. Functional bugs go to the plugin's source issue tracker.
Copyright/rights reports go to catalog maintainers and cause copyright withdrawal.
Sensitive security reports follow the Host SECURITY.md policy, not public raw logs.

The triage owner routes a security report to a security reviewer and publication
owner. The independent reviewer records exact affected artifacts and evidence;
the publication owner issues a separate higher-sequence safety PR and verifies
the served index/client result. A false positive requires explicit higher-sequence
allowed decisions, not deleting the history or rolling back the index. Copyright
withdrawal remains independent of security unblocking.

## Installation handoff

After install, direct users to Configure credentials (TTS may need a paid external
account), Select compatible Agent (MCP/Skill), or Appearance selection (theme).
Saved backend changes require restart; distinguish saved and currently running
versions. For breaking configuration/data updates, provide manual steps before
installation, including whether the old running version can continue. No generic
migration engine, automatic rollback or secret-purpose guessing is promised.

A display cache has no install-authorizing TTL: the current Host refreshes the
official index for EVERY store installation. Offline/cached browsing and installed
management remain available, but a stale cache cannot authorize a new store install.
Known bans remain durable independently of that cache.

## Local qualification versus public gates

The local demonstration uses real Git commits, a rejected submission and revision,
fixed tools, HTTPS and real packages. Demo-author/reviewer and approved refs are
explicit simulations. A non-author using only this guide to submit/revise and an
independent user installing in a clean environment remain public qualification
evidence; local automation does not manufacture those identities or approvals.

GitHub controls reference: [protected-branch reviews](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-pull-request-reviews-before-merging).
