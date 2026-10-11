# Context source contract v0

> Part of the [Amadeus Extension Protocol v0.1](../extension-protocol-v0.1.md)
> draft. `amadeus.context.source/v0` is **provisional**: drafted for the memory
> recall pilot. Updated 2026-10-11: the current wire draft is not sufficient
> for scoped cross-session memory. The readiness gates in §7 must be resolved
> before an external memory pilot claims support. MiMo P1 does not implement
> this contract.

A context source offers reference material for a Main Chat turn: memories,
knowledge, or facts about the user's situation. The Host decides what reaches
the model. A context source never speaks, never instructs the model, and never
changes the persona, system prompt, or conversation history.

## 1. Manifest fields

| Field | Value |
| --- | --- |
| `category` | `memory`, `knowledge`, or `situation` |
| `max_tokens` | 1 to 2000: the most the source asks to contribute to one turn |
| `deadline_ms` | 20 to 500: the time the source asks for per turn |

The Host capability `conversation.current:read` is optional. Without it, queries
carry no `user_text`.

## 2. Admission boundary

The next Main Chat turn.

## 3. `context.query`

Host → Runner request.

| Param | Value |
| --- | --- |
| `turn_id` | Opaque turn reference |
| `session_ref` | Opaque Session reference |
| `language` | Language tag of the turn |
| `user_text` | The user's current turn, only with `conversation.current:read` |
| `budget_tokens` | The Host's allocation, at most `max_tokens` |
| `deadline_ms` | At most the declared `deadline_ms` |

Result: `{ "items": [ … ] }` with at most 16 items, most relevant first:

| Item field | Value |
| --- | --- |
| `text` | Plain text, at most 2000 characters |
| `ref` | The source's own stable reference for the item, at most 200 characters |
| `label` | Optional short label shown to the user, at most 80 characters |
| `observed_at` | Optional RFC 3339 time when the underlying fact was observed |
| `confidence` | Optional number from 0 to 1 |

## 4. Host behavior

- **Timing.** The Host queries all active sources concurrently once a turn is
  admitted and waits at most each source's deadline, which the Host may shorten.
  A late result is discarded for that turn and recorded as timed out. The turn
  never waits longer. Abandoning a turn also invalidates its outstanding
  results. Amadeus must bound still-running local thread queries: a timed-out
  `asyncio.to_thread` call does not terminate its worker.
- **Budget.** Each source gets at most `min(max_tokens, Host per-source cap)`
  tokens, and all sources share a total cap. The Host keeps a source's items in
  the source's order and drops whole items from the end when they do not fit. It
  never edits item text.
- **Order between sources.** The user's priority in Settings, by default the
  order of installation.
- **Placement.** Items go into a labeled reference section, separate from
  instructions, persona, and history. Each item shows its label and source, and
  the section says the material is reference, not instructions.
- **Provenance.** For each turn the Host records which items were used (origin,
  `ref`, `label`) and which were dropped and why. The user can see this and can
  disable a source.
- **Speculative turns.** If the Host starts a turn speculatively, it MAY query
  sources early and discard the results when the turn is abandoned.

Amadeus's current seam is `server/cooperative_provider_loop.py`'s
`role_reference`, wired by `server/app.py` to `role_character_reference` in
`core/character_rag.py`. The existing corpus is restricted to the default
character. Preserve that ownership while first exercising collection through
a built-in source; do not add a second Main Chat injection path in
`core/chat_runtime.py`, which now handles role text/audio presentation.
Session/role/Project/admission changes during retrieval invalidate the captured
query context; §7 describes the scope still missing from the external wire.

## 5. Memory governance

A source with `category: "memory"` MUST implement these methods, so the Host can
let the user inspect, forget and export memories even if the extension has no
interface of its own. **Correction and explicit retention are not defined by
these three methods** and remain readiness gates in §7; do not advertise them
as already supported:

| Method | Params | Result |
| --- | --- | --- |
| `memory.list` | `{ "cursor"?, "limit" }`, `limit` at most 100 | `{ "items": [{ "ref", "text", "created_at", "updated_at"? }], "next_cursor"? }` |
| `memory.forget` | `{ "refs": [...] }`, at most 100 refs | `{ "forgotten": [...], "missing": [...] }` |
| `memory.export` | `{}` | `{ "path" }`: a JSON file the source wrote in its data directory, which the Host offers to the user |

After `memory.forget` succeeds, the forgotten items never appear in
`context.query` again, and the source deletes them and the data it derived from
them. Successful forget also invalidates earlier in-flight results and cached
reference sections; a delayed query must not reintroduce a forgotten item.
Excluding a memory derived from a Session/Work source does not itself delete
that authoritative source. A later import or index rebuild must honor the
exclusion rather than silently recreate the memory. The user must separately
request deletion of raw conversation/Work records.

The Host cannot prove deletion inside arbitrary package code. The package's
contract/conformance tests must exercise forget, restart and index rebuild;
package review is not proof of physical erasure. Export paths must resolve
inside the package data directory without traversing links before the Host
offers the file. List, forget and export need the same Host-authorized scope
as queries; that scope's wire representation is still a §7 design gate.

## 6. Example

```text
→ {"jsonrpc":"2.0","id":7,"method":"context.query","params":{"turn_id":"t-5e1","session_ref":"s-9c0d","language":"zh","user_text":"周末帮我订上次那家咖啡店吧","budget_tokens":300,"deadline_ms":100}}
← {"jsonrpc":"2.0","id":7,"result":{"items":[
    {"text":"用户常去的咖啡店是车站南口的小店，偏好燕麦拿铁。","ref":"mem-412","label":"常去的咖啡店","observed_at":"2026-09-21T10:12:00+08:00","confidence":0.8}
  ]}}
```

## 7. Memory pilot readiness gates

The current `context.query` has a Session reference but no character/Project
scope. The observer contract delivers new events at most once and offers no
historical read/replay service. Neither grants arbitrary access to Host session
files or the Work Ledger database. The illustrative memory example combines
future contracts; it is not an approved automatic-retention policy.

The implementation sequence is:

1. **Built-in recall first:** read existing Session/Project/Work/Artifact records
   through their Host owners and return bounded, source-linked reference text.
   Start within the current Project, or current Session for an unbound Draft.
   User-shared preferences and character-specific relationships are different
   scopes. No second Work facts store or automatic persona updates are needed.
2. **Complete the external boundary:** use those real queries to specify
   authorized opaque scope references, bounded/paged historical source access,
   origin and source revision/invalidation, and cancellation/revocation.
   Update wire contracts, examples/schema where applicable and the Host together.
   A package cannot choose raw Host ids to widen its access.
3. **Governed explicit memory:** define user-directed retain/correct operations
   and consistent scope for query/list/correct/forget/export. Test restart,
   source corrections/removal, forgotten-item reimport, cross-role/Project
   isolation, Ledger conflicts and hostile reference text before enabling
   automatic formation experiments.

Host provenance must distinguish user statements, model-derived summaries,
Host templates and durable task facts. Current Session records may have
`turn_id`/`message_id` and Session `character_id`, but legacy messages do not
have complete source or timestamp metadata. Unknown values stay unknown; a
Session save timestamp is not an observation time. A turn can deliver multiple
messages, and interruption can revise its persisted representation. Emitting
one memory event per history append would misrepresent completion.

This section deliberately does not invent a second identity schema or a broad
history permission. The missing wire choices must be resolved with a real M0
caller before this provisional contract becomes stable.
