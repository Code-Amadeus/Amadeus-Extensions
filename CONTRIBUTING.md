# Contributing

This repository owns the protocol, schema, reference validator and standalone
stdlib TTS SDK. Contributions to those paths are offered under Apache-2.0;
authored examples under `examples/` are MIT-0 as stated by their LICENSE.
Do not submit material without the necessary rights; preserve third-party
licenses. Code licensing does not grant rights to voices, models or artwork.

Host permissions, installation transactions, environment policy and activation
remain in Amadeus. Changes to contracts require a design Issue and review.
Current contracts remain provisional; no release or merge is implied by CI.

Install `requirements-dev.txt`, then run `python -m pytest` and
`python tools/build_sdk.py --output-dir dist`. Runtime SDK code uses only the
standard library and never imports Host modules. Change canonical source here,
then update the Host's source revision, wheel and checksums together.
