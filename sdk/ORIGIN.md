# SDK origin and license scope

The initial `sdk/python/` source was authored for the Amadeus extension experiment
and moved from Code-Amadeus/Amadeus commit
`388e9733676e06e37e82629d5c7c89b8bbf84f58`, `sdk/extension-python/`.
The maintainer authorized Apache-2.0 licensing for this standalone source on
2026-10-13. This is a scoped grant for the protocol/SDK, not a relicensing of the
AGPL Host. The moved implementation imports only Python standard-library code;
no third-party implementation is copied into the SDK. Build dependencies retain
their own licenses and are not bundled in its runtime wheel.

Repository examples are MIT-0. Host examples currently remain at their existing
paths with an explicit MIT-0 grant; moving examples or adding a developer CLI is
outside this delivery change. A commit-author inventory alone is not evidence
of rights over any future external contribution.
