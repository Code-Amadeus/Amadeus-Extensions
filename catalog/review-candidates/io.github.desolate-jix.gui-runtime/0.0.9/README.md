# Author submission: Windows Desktop Automation 0.0.9

This update replaces technical-first store copy with a customer-facing English/Chinese title and introduction: what GUI Runtime does, why to install it, desktop task examples, and setup requirements. The proposed display names are **Windows Desktop Automation (GUI Runtime)** / **Windows 桌面操作（GUI Runtime）**. This remains a connector to a separately installed and started Runtime, not a complete bundled desktop automation service.

- [Release and versioned assets](https://github.com/Desolate-Jix/agent-gui-runtime/releases/tag/amadeus-extension-v0.0.9)
- [Exact wheel](https://github.com/Desolate-Jix/agent-gui-runtime/releases/download/amadeus-extension-v0.0.9/amadeus_agent_gui_runtime-0.0.9-py3-none-any.whl): 28,977 bytes; SHA-256 `e612dff39d5650e9235eb9a36eb1918b00cc0724fd725aac88bda7f4da5e5a3b`.
- [Source ZIP](https://github.com/Desolate-Jix/agent-gui-runtime/releases/download/amadeus-extension-v0.0.9/extension-source-0.0.9.zip) and [exact source commit](https://github.com/Desolate-Jix/agent-gui-runtime/commit/beebb9de51dd5494a376647e3f216836ab8294a3).
- [English features/setup](https://github.com/Desolate-Jix/agent-gui-runtime/blob/amadeus-extension-v0.0.9/integrations/amadeus/agent-review-instant/README.md) / [中文功能与安装说明](https://github.com/Desolate-Jix/agent-gui-runtime/blob/amadeus-extension-v0.0.9/integrations/amadeus/agent-review-instant/README.zh-CN.md).
- [Release scope and rebuild command](https://github.com/Desolate-Jix/agent-gui-runtime/blob/amadeus-extension-v0.0.9/docs/releases/AMADEUS_CONNECTOR_009_20261106.md).

## Checks and scope

[Fixed preflight](preflight.json) passes package format, target Host and curated policy. It uses Host `1840c8e4f646992ddaebea3139c8895f29743a8f` and Windows CPython 3.12.10. Independent human/runtime review remains pending (`not_reviewed`). [Build verification](BUILD_VERIFICATION.json) records two identical offline wheel builds, wheel RECORD and packaged source correspondence, final commit binding, no effective dependencies, and two passing Host contract checks. All six published assets were anonymously downloaded and matched their frozen hashes.

[Actual wheel diff from approved 0.0.8](candidate-diff-from-0.0.8.json) covers the new display name/description, bilingual README in metadata, homepage/version references, version-only Skill/reference edits and wheel metadata. The package ID, transport, connection fields, permissions, Host engines and contribution declarations are unchanged. Execution/review policy is unchanged. Runtime stays 0.1.11; this submission publishes no Runtime code.

Existing 0.0.8 configuration needs no migration. Runtime must still be installed/configured/started/stopped independently. The supported model API route sends screenshots/task information to the chosen providers and can incur fees. Local connection tokens are separate from model credentials. Local input authorization and operator-only disconnected recovery remain required.

No new installed 0.0.9 GUI flow or paid model API benchmark was run for this wording-only release. Existing Runtime examples and historical Amadeus/Pi evidence remain labeled by their actual versions and scope in the linked guide; none is claimed as a new 0.0.9 acceptance result.

## Ownership and rights

Reuse the established publisher/maintainer and ISC code-rights evidence from [review #11](https://github.com/Code-Amadeus/Amadeus-Extensions/pull/11) and [the approved 0.0.8 record](../../../packages/io.github.desolate-jix.gui-runtime/0.0.8.json). Publisher control and bundled assets have not changed; no new images, sound, fonts, native binaries or dependencies are included. [Versioned license](https://github.com/Desolate-Jix/agent-gui-runtime/blob/amadeus-extension-v0.0.9/integrations/amadeus/agent-review-instant/LICENSE).

This PR supplies author evidence only. It does not modify formal catalog package records, invent reviewer/approval facts or publish an index. Please review these exact bytes and prepare the maintainer-owned catalog/publication change.

## 中文摘要

本次把插件名称和说明改为面向用户的双语文案，先讲能做什么、为什么安装、适用场景，再说明独立 Runtime 和模型 API 等准备条件。仅更新文案及版本引用，不改变执行能力、权限、连接配置或恢复边界，已有 0.0.8 配置无需迁移。

固定预检、两次一致构建、包体与源码核对、两项 Host 合同检查及六项公开资产下载校验通过。本次未重跑安装态 GUI 流程或付费 API benchmark。0.0.8 的历史批准不作为 0.0.9 的批准；正式目录记录和商店发布仍由维护者独立审核后处理。
