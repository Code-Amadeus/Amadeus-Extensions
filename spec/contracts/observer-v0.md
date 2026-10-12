# Observer contract v0

> Part of the [Amadeus Extension Protocol v0.1](../extension-protocol-v0.1.md)
> draft. `amadeus.events.observer/v0` is **provisional**: drafted for the memory
> recall and task companion pilots. Updated 2026-10-11: outside MiMo P1;
> these topics alone do not implement historical recall or authorize automatic
> long-term retention.

An observer receives projected Host events. It cannot change how the Host
handles an event: there is no return value, no veto, and no ordering guarantee
relative to the Host's own processing.

## 1. Manifest fields

| Field | Value |
| --- | --- |
| `topics` | Non-empty list of the topics below, without duplicates |

Each topic requires a Host capability, which the manifest lists in
`permissions.host` (rule S5).

## 2. Admission boundary

Immediate. Deliveries start after `ready` and stop when the package leaves
`active` or the capability is revoked.

## 3. Topics

### 3.1 `work.item.updated`

Requires `events.work:read`. Sent when the projected state or title of a Work
item changes.

| Field | Value |
| --- | --- |
| `work_item_ref` | Opaque reference |
| `title` | The Work item title as shown to the user, at most 200 characters |
| `state` | `queued`, `running`, `needs_attention`, `completed`, `failed`, or `cancelled` |
| `project_title` | Optional project title |
| `updated_at` | RFC 3339 time |

`needs_attention` covers permission requests and questions that wait for the
user. The event is a projection. It never carries Provider-native payloads, file
contents, diffs, or credentials.

### 3.2 `conversation.turn.completed`

Requires `conversation.history:read`. Sent after the Host records a completed
Main Chat turn in the Session.

| Field | Value |
| --- | --- |
| `session_ref` | Opaque reference |
| `turn_id` | Opaque reference |
| `user_text` | The user's turn as recorded in the Session |
| `assistant_text` | The reply as recorded in the Session |
| `interrupted` | `true` if the user interrupted the reply |
| `language` | Language tag |
| `completed_at` | RFC 3339 time |

## 4. Delivery

- The Host sends the notification `events.deliver { "topic", "seq", "event",
  "dropped"? }`. `seq` increases by 1 per topic within an Activation.
- Delivery is at most once. v0 does not replay events after a restart.
- Each Activation has a bounded queue (default 256 events). When it is full, the
  Host drops the oldest events and reports how many in `dropped` on the next
  delivery.
- Revoking a topic's capability stops its deliveries immediately.

### 4.1 Current Amadeus integration limits

The current delivery owner in `server/cooperative_delivery.py` first obtains
display acceptance and then records history through
`core/session_manager.py:append_session_message`. One turn can publish several
`message_id` values, and interruption can update the stored reply. Consequently
the old proposal to emit a completed-turn event on each history append is not
a valid integration rule. Define the actual completion/correction boundary in
the owner before implementing this topic, and do not retry model generation
because history recording failed after display succeeded.

These at-most-once events have no backfill/replay and lack the scoped historical
source access needed by memory. Character/Project scope, authoritative origin,
correction/invalidation and scoped delivery must be resolved with the
[memory readiness gates](context-source-v0.md#7-memory-pilot-readiness-gates).
An opaque Session reference alone is not an authorization scope. MiMo P1 does
not expose these topics or implement the presentation service.

## 5. Combining with presentation requests

An observer that wants the character to mention something calls
`host.presentation.notify` (core [§6.5](../extension-protocol-v0.1.md#65-host-services)),
which requires `presentation:notify`. The Host decides whether and how to say
it.

```text
→ {"jsonrpc":"2.0","method":"events.deliver","params":{"topic":"work.item.updated","seq":12,"event":{"work_item_ref":"w-3fa2","title":"整理论文引用","state":"needs_attention","updated_at":"2026-10-05T14:03:11+08:00"}}}
← {"jsonrpc":"2.0","id":3,"method":"host.presentation.notify","params":{"fact":"任务“整理论文引用”在等待你批准一个操作。","urgency":"normal","source_ref":"w-3fa2"}}
→ {"jsonrpc":"2.0","id":3,"result":{"disposition":"queued"}}
```
