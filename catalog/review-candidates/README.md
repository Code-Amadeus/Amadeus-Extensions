# Reference wheel candidates — not reviewed

`reference-wheels.json` records eight local candidate artifacts: Tone TTS, Notes
MCP, Handoff Skill and desktop theme at 0.1.0/0.2.0. It contains their byte digests,
full file inventories/content diffs, static checker results, and exact checker
source hashes. No item is approved or published, and these are not external-author
evidence. The 0.1.0 → 0.2.0 comparisons use earlier **candidates**, not approved wheels.

The checker files are unmodified Git blobs from Host
`1840c8e4f646992ddaebea3139c8895f29743a8f`, run with Windows CPython 3.12.10 and
the existing minimal dependency environment. Its lock SHA-256 is recorded.
The policy/diff implementation is the unchanged Host-vendored copy of protocol
`58d3892d55c6a7ec6f8626153f503291bb10ab9a`. All eight pass static Host wheel checks
and curated-v1 automated policy. This is an exported checker inspection, not a
claim that remote CI or `verify_host` ran against a full clean Git checkout.

The actual wheel bytes are retained in the Host experiment under
`build/extension-author-journey/4005cfb5b41a/wheels`. This is a local evidence path,
not a public download URL. A new build may produce different bytes: reviewers must
receive and check these exact artifacts, or regenerate this packet for the new bytes.
The candidate IDs are illustrative `com.example.*` identities; confirm/allocate
publisher ownership before publication. An identity change requires a new wheel
and fresh review, not a catalog alias over the current bytes.

For each version, a non-author reviewer must:

1. Obtain the exact wheel, verify the recorded digest, and inspect all unpacked
   files using [curated-v1](../REVIEW_CHECKLIST.md). An inventory/diff is only evidence.
2. Confirm package ownership, code license and separate material rights. These
   examples declare MIT-0, but that declaration is not the reviewer's rights finding.
3. Review every executable entry/script/Skill instruction and actual access;
   validate runtime behavior against Host D2/S1/S2/S3 evidence. Tone generates
   synthetic PCM and must not be described as useful speech synthesis.
4. Record their own approval and evidence, fix findings and re-check changed bytes.
5. Only then create reviewed package input facts and immutable artifact URLs;
   follow the separate publication PR and increasing-sequence procedure.

The candidate file intentionally has no reviewer/date approval or download URL.
A maintainer must not translate `host_static_check: passed` into a reviewed record.
No candidate was added to `packages/`, `security.json`, or `index.json`.

To reproduce the underlying checks with the exact bytes and pinned tools:

```powershell
<pinned-minimal-python> -I <fixed-host>/tools/extension_package.py check-wheel <wheel>
python tools/check_catalog.py --wheel <wheel> --output <initial-inventory.json>
python tools/check_catalog.py --wheel <0.2.0-wheel> --previous-wheel <0.1.0-candidate-wheel> --output <candidate-diff.json>
```

The Host's shipping-shell fixture records synthetic authority and automated
native confirmations explicitly; it does not establish public reviewer identity.
