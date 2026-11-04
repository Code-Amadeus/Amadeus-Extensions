# Author resubmission — Windows GUI Runtime Connector 0.0.5

Follow-up to [submission #7](https://github.com/Code-Amadeus/Amadeus-Extensions/pull/7)
and [author revision request #4](https://github.com/Desolate-Jix/agent-gui-runtime/issues/4).
The prior 0.0.4 candidate evidence is retained. This directory supplies author
materials, **not catalog approval or a live catalog entry**. Please make all
further revisions in the new submission PR.

- **Versioned wheel and preflight:** [0.0.5 wheel](https://github.com/Desolate-Jix/agent-gui-runtime/releases/download/amadeus-extension-v0.0.5/amadeus_agent_gui_runtime-0.0.5-py3-none-any.whl),
  **24,635 bytes**, SHA-256
  `9727889c378354ee6b24648c94b2276b8ed30d986b49d1dd4b0f5c3c188774dd`.
  The attached `preflight.json` is the actual fixed Windows/CPython 3.12.10/
  Host `1840c8e` report. Format, Host and curated policy passed; independent
  human/runtime review remains pending and `review_status` is `not_reviewed`.
- **Source/build and usage:** [Exact source ZIP](https://github.com/Desolate-Jix/agent-gui-runtime/releases/download/amadeus-extension-v0.0.5/extension-source-0.0.5.zip),
  **48,737 bytes**, SHA-256
  `93e78d5a008df6d4c5fbb35a237fc9517269d5ebbc6c461beabdc667095cd53f`;
  [English setup](https://github.com/Desolate-Jix/agent-gui-runtime/blob/amadeus-extension-v0.0.5/integrations/amadeus/agent-review-instant/README.md),
  [中文指南](https://github.com/Desolate-Jix/agent-gui-runtime/blob/amadeus-extension-v0.0.5/integrations/amadeus/agent-review-instant/README.zh-CN.md),
  [build verification](https://github.com/Desolate-Jix/agent-gui-runtime/releases/download/amadeus-extension-v0.0.5/BUILD_VERIFICATION.json),
  [author validation and limits](https://github.com/Desolate-Jix/agent-gui-runtime/blob/amadeus-extension-v0.0.5/docs/verification/AMADEUS_CONNECTOR_005_20261026.md).
  Two offline wheel builds were byte-identical. Inventory and the full
  candidate-to-candidate 0.0.4 diff are attached; the older candidate was not an
  approved catalog package.
- **Ownership and rights:** namespace `io.github.desolate-jix.gui-runtime`;
  [source repository](https://github.com/Desolate-Jix/agent-gui-runtime),
  [release history](https://github.com/Desolate-Jix/agent-gui-runtime/releases),
  [connector ISC license](https://github.com/Desolate-Jix/agent-gui-runtime/blob/amadeus-extension-v0.0.5/integrations/amadeus/agent-review-instant/LICENSE).
  These are independently verifiable control/rights references, not author-issued
  approval. The wheel includes no Runtime executable, artwork, model weights,
  provider credentials or user data; external component licenses remain separate.
- **Changes/migration:** 0.0.5 updates installation disclosures, manifest
  homepage/repository, package metadata and synchronized README/Skill instructions.
  Existing `runtime_url`, secret `connection_token`, permissions and native HTTP
  connection semantics are unchanged; no 0.0.3/0.0.4 configuration migration.
  Runtime code, thresholds and model defaults are unchanged. Old 0.0.4 bytes and
  URLs are not replaced.

## Installation commitment and compatibility

This is a **connector**. Users separately install, configure, start, update and
stop Windows GUI Runtime. Recommend released **Runtime 0.1.8**; the minimum
HTTP/pre-action-review route was introduced in **0.1.6**, and the active service
must expose the required authentication, original-command and review/continue
capabilities. Version numbers and successful initialization alone do not certify
the entire integration. Runtime 0.1.5 has no HTTP entry point. Later versions need
manual capability qualification; no automatic version detector is claimed.

Install the [Runtime separately](https://github.com/Desolate-Jix/agent-gui-runtime/releases/tag/instant-v0.1.8),
then import this wheel into a compatible Amadeus with native HTTP MCP/Skill
support and Python 3.12. Configure a trusted loopback `runtime_url` and a
separately generated `connection_token`, bind both contributions to Pi, enable,
apply the Host restart and create a new Work. Provider API keys stay in Runtime;
they are different from the local connection token. External model calls may
incur charges. The API route requires no local GPU/model weights. Uninstalling
or disabling the connector does not stop/uninstall Runtime or delete its data.

## Evidence boundaries and reviewer handoff

Fixed and current Host `b6616a1` static manifest/Skill and secret-projection
checks passed two cases each. Source Runtime 0.1.8 HTTP checks passed version/tool
discovery, seven security negatives, ownership controls and two actual child-host
start/stop/release/reconnect rounds with no GUI/model commands. A stopped first
session's maintenance registration was not immediately retired; exact test-owned
cleanup proof was later accepted. Maintenance admission/update was not tested,
and an update blockage was not reproduced. The attached `AUTHOR_VALIDATION.json`
retains this observation and the narrower pass scope.

The prior installed 0.0.4/0.1.6 controlled Pi/Main-review evidence remains
historical. The exact new Host/Pi/0.0.5/Runtime combination still needs independent
installation, the documented minimal navigation task, failure/credentials,
cancellation/disconnection, session release/reconnect, disable/uninstall review.
The supplied setup guides include concrete troubleshooting and no-replay recovery.
This is not a new accuracy, performance or token benchmark.

The independent maintainer adds real `catalog/packages` ownership/review facts
after review in the submission PR, then prepares and verifies a separate
publication PR. This author submission does not edit `catalog/packages`, the
official index, security decisions, policy or workflows. Candidate-only CI may
report `publication: false`; that is not package approval. Please keep the
submission open until the exact version's review is complete.

中文：按 #4 新投 0.0.5，补齐连接器安装承诺和包内说明，旧 #7 的 0.0.4 证据保留。
用户需独立安装、配置和启动 Runtime；推荐 0.1.8，最低 HTTP／前置审核能力起于 0.1.6，
实际版本和必要能力须人工核对。本机连接 token 与模型 API Key 不同，模型调用可能收费。
配置键／权限／执行逻辑不变，停用或卸载连接器不会停止、卸载 Runtime 或删除其数据。
固定预检和有限作者联调不是独立批准；新组合 GUI、异常和生命周期验收由维护者完成。
收录事实、非作者批准和另一次索引发布均待完成，不自填 reviewer 或正式索引。
