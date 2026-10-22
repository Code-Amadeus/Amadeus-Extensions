# Contributing

This repository owns the protocol, schema, reference validator and standalone
stdlib TTS SDK. Contributions to those paths are offered under Apache-2.0;
authored examples under `examples/` are MIT-0 as stated by their LICENSE.
Do not submit material without the necessary rights; preserve third-party
licenses. Code licensing does not grant rights to voices, models or artwork.

Host permissions, installation transactions, environment policy and activation
remain in Amadeus. Changes to contracts require a design Issue and review.
Current contracts remain provisional; no release or merge is implied by CI.

Use CPython 3.12.10 and install `requirements-dev.txt` with
`python -m pip install --require-hashes -r requirements-dev.txt`, then run
`python -m pytest` and
`python tools/build_sdk.py --output-dir dist`. Runtime SDK code uses only the
standard library and never imports Host modules. Change canonical source here,
then update the Host's source revision, wheel and checksums together.

The direct development requirements live in `requirements-dev.in`; the generated
`requirements-dev.txt` pins all transitive versions and archive hashes for
Windows/Linux. Regenerate with uv 0.12.8:

```sh
uv pip compile --universal --python-version 3.12.10 --generate-hashes --no-emit-index-url --output-file requirements-dev.txt requirements-dev.in
```

The build tool canonicalizes SDK text/ZIP metadata and recalculates RECORD per
[the wheel format](https://packaging.python.org/en/latest/specifications/binary-distribution-format/).
CI compares artifacts built independently on Windows and Linux. Do not replace
that cross-platform comparison with two builds on the same machine. The Host's
pinned wheel must match this canonical artifact; runtime support remains >=3.11.


For author preflight, ownership/transfer, review invalidation, PR responsibilities,
revision and verified distribution, follow the [submission workflow](catalog/SUBMISSION.md).
