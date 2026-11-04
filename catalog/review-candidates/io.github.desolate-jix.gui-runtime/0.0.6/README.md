# Author revision — Windows GUI Runtime Connector 0.0.6

Revision within [PR #11](https://github.com/Code-Amadeus/Amadeus-Extensions/pull/11),
addressing the [maintenance-settlement blocker](https://github.com/Code-Amadeus/Amadeus-Extensions/pull/11#issuecomment-6415025554).
The 0.0.5 and earlier candidate evidence and published bytes are retained.
These are author materials, **not final catalog approval or a live catalog entry**.

## Exact immutable delivery

- [Connector release](https://github.com/Desolate-Jix/agent-gui-runtime/releases/tag/amadeus-extension-v0.0.6):
  `amadeus_agent_gui_runtime-0.0.6-py3-none-any.whl`, **25,761 bytes**,
  SHA-256 `e55b88de422d2a8bfcb0edd39331a4980d5753c25a2ec084b7b2abac2ee8c586`.
- [Source ZIP](https://github.com/Desolate-Jix/agent-gui-runtime/releases/download/amadeus-extension-v0.0.6/extension-source-0.0.6.zip):
  **49,929 bytes**, SHA-256 `61b9f0f6456ba6d08f0d8d69463a0969335228c7d646ea397bc1467ae258c048`.
- Source commit `b0ddd8096bacd0d8710cc60736bce5b861032156`; source repository and
  [ISC license](https://github.com/Desolate-Jix/agent-gui-runtime/blob/amadeus-extension-v0.0.6/integrations/amadeus/agent-review-instant/LICENSE)
  establish author/rights references for independent verification.
- Recommend repaired [Runtime 0.1.9](https://github.com/Desolate-Jix/agent-gui-runtime/releases/tag/instant-v0.1.9).
  Installer SHA-256 `bde46f7a8c47b42388c8ac39916c5152cb0931528d171170c0d9b91e2bf5e972`;
  update target digest `6163b60b33eecbc4067a1951c0ae2f690385719e13d85c255159c11bbc161d8a`.
- All 11 Runtime and eight connector assets were anonymously downloaded and
  matched frozen size/SHA-256 after publication. The installer remains unsigned.

## Changes and installation commitment

The resource-only HTTP MCP + Skill wheel updates its packaged Runtime
recommendation to 0.1.9 and moves mutable store-review wording out of the Skill.
Configuration keys, permissions, HTTP contributions and the recovery boundary
are unchanged. Skills are behavior-impacting operating instructions and remain
reviewed as such. Both disconnected recovery tools stay operator-only;
same-session Main screenshot review and explicit continuation remain supported.

Users separately install/configure/start/stop/update Runtime. Use Windows x64,
a compatible Amadeus with native HTTP MCP and Skill support, and Host Python
3.12; Runtime supports the documented prepared API Python 3.12 or existing 3.11
environment. No local GPU/model weights are required for the API route. Provider
API credentials stay in Runtime and may incur service charges; the connector's
secret `connection_token` is a separate local authentication secret. Configure
a trusted loopback `runtime_url`, bind both contributions to Pi and follow Host
enable/restart/new-Work requirements. Disabling/uninstalling this connector
does not stop/uninstall the external Runtime or delete its data.

[English setup](https://github.com/Desolate-Jix/agent-gui-runtime/blob/amadeus-extension-v0.0.6/integrations/amadeus/agent-review-instant/README.md)
· [中文指南](https://github.com/Desolate-Jix/agent-gui-runtime/blob/amadeus-extension-v0.0.6/integrations/amadeus/agent-review-instant/README.zh-CN.md)
· [0.1.8 recovery procedure](https://github.com/Desolate-Jix/agent-gui-runtime/blob/instant-v0.1.9/docs/RUNTIME_018_SETTLEMENT_RECOVERY.md)

## Evidence and limits

- Two offline wheel builds match byte-for-byte. Source, METADATA, all packaged
  resources and RECORD match. Attached diff compares exact 0.0.5 candidate bytes,
  not a previously approved package.
- Fixed catalog `3c739e1a5c177d585db3ed63868725dae5cadc32`, Host
  `1840c8e4f646992ddaebea3139c8895f29743a8f`, Windows/CPython 3.12.10 preflight
  passed format, Host and policy; `review_status=not_reviewed` and human/runtime
  independent review remain pending.
- Runtime original plan/runner/receipt settlement: **187 affected checks** passed.
  **94 updater/installer checks** and **five exact-release migration cases** passed.
  Counts overlap and are not added as unique coverage. Original failures and
  repaired test-harness failures remain retained; see `AUTHOR_VALIDATION.json`.
- Original 0.1.8 completion/cancellation evidence stays unchanged. In a separate
  exact 0.1.8 installation, old `settle/apply` and direct installer refusal were
  reproduced; the verified new release's external maintenance CLI settled the
  original proofs, then the **original old updater** applied exact 0.1.9 bytes
  and passed its fixed health check. Active lock/process, unknown input and
  altered receipt cases still refused. No registration was manually deleted.
- Final **installed 0.0.6 + Runtime 0.1.9**: shipping Host `b6616a1`, Pi 1.2.0,
  native ExtensionInstaller and real Work route completed Documents → Reports →
  Up → Receipts, one original four-step plan. No refusal proxy or Main semantic
  intervention occurred this round. Pi read the final bound image; author
  inspection confirmed Receipts and its marker. Owned window/host cleanup,
  fresh HTTP initialize/status/DELETE 200 and official `settle` passed, clearing
  **one** proven registration. All 700 payload and two marker hashes stayed equal.
  Controller termination of HTTP/Electron parents returned Windows exit 1 after
  verified host/window cleanup; this is not called graceful daemon shutdown.
- `recover`, `observe`, `resume_pre_dispatch` task-plan settlement remains
  conservatively unqualified. No new performance/general-accuracy claim; no new
  certification of current-agent mode in Amadeus, physical power loss, every
  migration, operator-prepared-window retention or disable-with-live-Runtime.

Independent maintainers retain the earlier checks for their stated scope and
own remaining Host UI/credential-error and final installed acceptance. After
that they add real `catalog/packages` review facts **in this PR**, obtain
non-author approval on the final head, merge, then use a separate publication PR.
This revision edits only `review-candidates`, not approvals/index/policy/workflows.
Candidate-only green `publication:false` CI is not admission approval.

## 简体中文

本轮在原 #11 返修，不覆盖旧版本。Runtime 0.1.9 修复原计划、runner 与输入回执的
维护结算；连接器 0.0.6 更新包内推荐版本，配置／权限与恢复边界不变。两恢复工具
仍交操作员，同会话 Main 看图审核后继续原任务的能力保留。

双离线构建及固定可信预检通过；187 项相关回归、94 项更新器／安装器检查和五项
确切发行迁移用例分组记录，不累加。复现旧版拒绝后，用独立验真的新脚本受锁核验
原证据，随后原更新器成功升级；活动／未知输入和篡改回执仍拒绝，未手删登记。
最终安装态 Pi→HTTP→Runtime 四步导航完成，无拒绝注入、无 Main 语义接管；清理、
重连释放及官方结算通过，验证清除 1 条登记，700 项载荷与两个测试文件摘要不变。

独立验收及商店批准仍由维护者负责；作者仅补候选材料，不自填正式收录事实，不把
CI 通过当作上架。完整字节身份、已测范围与限制见附带报告及上述不可变发布链接。
