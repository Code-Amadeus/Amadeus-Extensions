# Artifact review checklist — curated-v1

Review the bytes whose SHA-256 is recorded, not only the source repository.
“Reviewed” means this artifact completed this checklist; it is not a security
warranty, an OS sandbox, a permission grant or approval of future versions.
Record reviewer, date, policy version, digest and evidence on every version.
An author/publisher maintainer cannot be their own reviewer.

- [ ] Fetch the exact wheel, verify digest, and retain its full file inventory.
  Confirm package ownership/transfer independently of manifest author text or PR account.
- [ ] Run the fixed Windows/CPython/Host checker. Record its commit and environment.
  Confirm ID, X.Y.Z version, wheel filename, METADATA and entry point agree.
  Never replace bytes at an existing ID/version, including build suffixes.
- [ ] Verify filename and WHEEL both specify py3-none-any, with purelib true.
  No native or executable binaries, .pth startup hooks or opaque/unreviewable code.
  Inspect signatures/content as well as suffixes; automated detection is incomplete.
- [ ] Effective dependencies are empty or the compatible Host SDK only. No direct
  dependency URLs, source builds, hidden installers or runtime package downloads.
- [ ] MCP starts only Python or reviewed package scripts. Python -m must name a
  packaged module; script targets stay under the package. No -c, pip, npx/uvx or
  configuration values selecting executables/modules. Test script executability
  on declared platforms; Windows should use Python plus a package module/.py.
- [ ] Inspect every execution entry, script and Skill instruction. Search and
  reason about network access, code downloads/eval, subprocesses and persistence.
  Remote API responses may be data, not fetched executable code. Static CI cannot
  establish this item; run approved contracts only in an isolated uncredentialed job.
- [ ] Check actual file/network behavior, secret handling and disclosures. No
  hidden Host imports or permissions; Main Chat receives no new execution authority.
  Retention and explicit deletion must match the documented lifecycle.
- [ ] Check code license and separate rights for every image, sound or other
  asset. Character artwork needs provenance/permission; a code license alone is
  insufficient. Current themes use installed fonts, not newly bundled fonts.
- [ ] Review install, use, update, cancellation/close, disable, uninstall/reinstall
  evidence for this contribution. Label static, process, native Agent, GUI and
  paid/real-service coverage separately. Do not promise automatic startup rollback.
- [ ] Compare with the previous reviewed wheel using check_catalog.py. Read the
  complete changed files when the diff is truncated, and review unchanged code
  as needed. Initial versions require full review; every later version still
  completes the whole checklist. Independently built source comparison is supporting
  evidence, not a substitute for examining the actual distribution.
- [ ] Record remaining limitations and the independent approval in the review PR.
  A CI pass alone must never create a reviewed record.

For later removal, use copyright withdrawal for asset/license complaints,
maintainer withdrawal for ordinary retirement, and security decisions for unsafe
artifacts. Do not relabel copyright removal as a security ban or delete user data.

Before first public release: protect main, require reviewed merges, verify
maintainer two-factor authentication and least-privilege workflows, and ensure
submission execution jobs have no publishing credentials. S3 owns that evidence.


For author preflight, ownership/transfer, review invalidation, PR responsibilities,
revision and verified distribution, follow the [submission workflow](SUBMISSION.md).
