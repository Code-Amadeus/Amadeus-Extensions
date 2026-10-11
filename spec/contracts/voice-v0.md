# Voice backend contracts v0

> Part of the Extension Protocol v0.1 draft. TTS and ASR are **provisional**.
> Updated 2026-10-11. Amadeus implements the restart profile in core §1.3.1;
> it has not shipped a stable SDK or full conformance claim.

A `voice_backend` contribution turns text into speech or speech into text for
the Host. The Host keeps everything around it: when to speak or listen,
playback, subtitles, mouth movement, interruption, and fallback.

## 1. Common rules

| Field | Value |
| --- | --- |
| `role` | `tts` or `asr` (`wake` is reserved) |
| `contract` | `amadeus.voice.tts/v0` for `tts`, `amadeus.voice.asr/v0` for `asr` |
| `deployment` | `local` (runs on this computer) or `remote` (sends text or audio to a network service) |
| `languages` | 1 to 32 language tags, for example `zh`, `ja`, `en` |

- **Selection.** The user selects a backend for each role by qualified id. The
  Host shows a `remote` backend as sending text or audio off this computer.
- **No silent remote use.** The Host MUST NOT select a `remote` backend
  automatically, including as a fallback when another backend fails.
- **Fallback.** When the selected backend cannot serve (its package is not
  `active`, its health is `error`, or a call failed), the Host uses the
  fallback the user configured: a local backend, or text only. It shows the
  reason. Being built-in does not make a remote backend an eligible automatic
  fallback. The first MiMo pilot implements text only; it does not assume
  another model is loaded or silently load one.
- **Languages.** The Host sends only requests in a declared language. Requests
  in any other language go to the fallback.
- **Inherent inputs.** The text a TTS backend speaks and the audio an ASR
  backend transcribes are authorized by the user's selection of that backend.
  They need no Host capability.

## 2. TTS: `amadeus.voice.tts/v0` (provisional)

### 2.1 Manifest fields

| Field | Value |
| --- | --- |
| `streaming` | `true` if audio can arrive before the whole utterance is synthesized |

An **utterance** is the text of one synthesis request, usually one sentence or
a group of short sentences.

### 2.2 Admission boundary

For Amadeus P1, selection/configuration/enablement/removal apply after backend
restart. The native scheduler keeps one stable proxy for that process lifetime;
Runner crash recovery is internal. No pipeline generation handover is required.
On process shutdown, admitted work finishes within the bound or is cancelled.
Cancelled/obsolete audio is discarded; emitted audio and failed paid synthesis
are never replayed. Text remains available when voice fails.

Other future profiles may define utterance-boundary hot application, but must
then bind every request's runtime/configuration/cache/cleanup to one generation.
That optional future behavior must not be presented as Amadeus product behavior.

### 2.3 `tts.synthesize`

Host → Runner request.

| Param | Value |
| --- | --- |
| `contribution_id` | Local TTS contribution id; required when a Runner has multiple TTS contributions |
| `utterance_id` | Host correlation id, at most 128 characters |
| `text` | Plain text without markup, 1 to 2000 characters |
| `language` | Requested speech language; match declared tags by case-insensitive primary subtag (`ja` matches `ja-JP`, `en` matches `en-US`) |
| `speed` | Advisory pace hint, 0.5 to 2.0, default 1.0. The Amadeus restart profile always sends 1.0; packages may expose an explicit speed setting. GPT-SoVITS first-sentence pacing is not forwarded. |
| `deadline_ms` | Optional relative deadline |

While it works, the Runner sends `tts.chunk` notifications:

| Param | Value |
| --- | --- |
| `request_id` | Id of the `tts.synthesize` request |
| `seq` | 0 for the first chunk, then increasing by 1 |
| `sample_rate` | 8000 to 48000 Hz, the same for every chunk of a request |
| `pcm_s16le` | Base64 of mono signed 16-bit little-endian PCM, at most 1 MiB decoded |

Result: `{ "chunks": <count>, "duration_ms": <total audio duration> }`.

Rules:

- Streaming and non-streaming backends use the same method. A non-streaming
  backend sends all its audio before responding.
- A successful request delivers at least one non-empty chunk. A backend that
  cannot produce audio responds with `contribution_error`. The Host never drops
  an utterance silently.
- A gap in `seq` or a change of `sample_rate` makes the Host treat the utterance
  as failed.
- On `$/cancel` the Runner signals cancellation promptly, stops emitting audio
  and responds with `cancelled` after cleanup. Blocking network setup may finish
  later and MUST use bounded timeouts. The Host immediately stops delivering
  cancelled audio and discards late chunks. Unacknowledged cancellations count
  against the two-request admission bound until a terminal response or process
  exit. There is no two-second crash rule: cancellation latency alone MUST NOT
  consume the Runner crash-restart budget or terminate unrelated synthesis.
- The Host MAY send up to two concurrent requests to one backend so it can
  synthesize ahead. A backend MAY process them one after the other but answers
  each.
- A backend never plays audio itself.

### 2.4 Health

| Health | Example |
| --- | --- |
| `ready` | Configured and reachable |
| `degraded` | The service is rate-limiting; requests still succeed, more slowly |
| `error` | The service rejected the API key. `detail` tells the user what to fix. |

### 2.5 Example

```text
→ {"jsonrpc":"2.0","id":42,"method":"tts.synthesize","params":{"utterance_id":"u-981","contribution_id":"mimo","text":"The task is complete.","language":"en","speed":1.0,"deadline_ms":8000}}
← {"jsonrpc":"2.0","method":"tts.chunk","params":{"request_id":42,"seq":0,"sample_rate":24000,"pcm_s16le":"AAABAP7/…"}}
← {"jsonrpc":"2.0","method":"tts.chunk","params":{"request_id":42,"seq":1,"sample_rate":24000,"pcm_s16le":"…"}}
← {"jsonrpc":"2.0","id":42,"result":{"chunks":2,"duration_ms":1840}}
```

### 2.6 Relation to the in-process contract

Amadeus's built-in `BaseTTSBackend.synthesize_stream(TTSSynthesisRequest)`
maps directly for `text`, `language`, and `speed`. The fields `voice`,
`reference_audio`, `reference_text`, `reference_language`,
`chunk_size_seconds`, and `options` are not part of v0. A package takes
backend-specific choices, such as the voice, from its own config. Reference
audio and style or emotion hints are an open question for a later version.
The proxy converts the wire PCM16LE audio to the existing adapter's audio
representation and leaves playback, subtitles, mouth movement and turn gates
with the Host. The first pilot must verify language and speed behavior; a
wire field is not proof of remote support. MiMo declares English only for
Amadeus and does not support Japanese; it ignores the advisory speed hint.
Fish declares Japanese/English and maps the hint to its own prosody parameter.

The existing MiMo backend imports `config.settings` and private helpers from
`tts.backends.openai_compatible`. The external package must replace those
dependencies with its own config and tested public SDK/package helpers.
Preserve the existing SSE, malformed/incomplete audio, response cleanup and
no-second-POST tests during extraction.

## 3. ASR: `amadeus.voice.asr/v0` (provisional)

### 3.1 Manifest fields

| Field | Value |
| --- | --- |
| `speculative` | `true` if the backend accepts speculative requests on partial audio, which the Host uses to detect the end of an utterance early |

### 3.2 Admission boundary

The next speech segment.

### 3.3 `asr.transcribe`

Host → Runner request.

| Param | Value |
| --- | --- |
| `segment_id` | Host correlation id, at most 128 characters |
| `mode` | `final`, or `speculative` if the backend declared it |
| `sample_rate` | `16000` |
| `pcm_s16le` | Base64 of mono signed 16-bit little-endian PCM, at most 120 seconds |
| `hotwords` | Optional comma-separated domain terms, at most 1000 characters |
| `deadline_ms` | Optional relative deadline |

Result: `{ "text": <string or null> }`. `null` means no speech was recognized.
A failure is an error, not `null`.

Rules:

- The Host sends microphone audio only to the backend the user selected for
  this role.
- A speculative result is a hint. Only a final result becomes the user's turn.
- When the Host sends `final` for a segment, it cancels any pending
  `speculative` request for the same segment.

### 3.4 Relation to the in-process contract

Amadeus's built-in `BaseASRBackend.transcribe(audio, sample_rate, context)`
maps to `pcm_s16le` (converted from float32), `sample_rate`, and `hotwords`
(from `context`). `load(device)` is replaced by the Runner lifecycle; device
choice belongs in the package's config.
