# Author revision — Connector 0.0.8 / 未启动 owner 释放修复

This candidate addresses only the proven never-started HTTP-owner release fix
in Runtime 0.1.11. An initialized owner with cleanup_verified=false can release
only with original lifecycle proof of no start attempt, attached resources or
pending work. Initial-looking status alone is insufficient; started, active,
unknown and unclean owners retain the existing cleanup gates. The normal
cleanup_verified=true path remains. No model, threshold or input authority is
changed.

Final release source reference: `323099100b04beeb6ee67a846f0e530998c19bbc`. Original wheel build anchor:
`db9dc10dacf3534949cd59e3e83804232fb227dd`. The frozen package inventory is checked against the final
commit, allowing only documented CRLF/LF normalization. A later commit is not
represented as the wheel's original build HEAD.

- Wheel: `amadeus_agent_gui_runtime-0.0.8-py3-none-any.whl`, 27,990 bytes, SHA-256 `2f532faf152faf2e1e3ab3140e1097487689be34d638e4ee86539e06886cbcaf`.
- Source ZIP: `extension-source-0.0.8.zip`, 52,657 bytes, SHA-256 `b54afe548dae17c04600f48553b9e27033db4a370f6963ad2ea518b585cff3b4`.
- Comparison baseline: final published 0.0.7 wheel `43e5a22e9a289ee7ad9852f66128096e1f361449a54dbb619038e870b5b852b7` and
  source ZIP `ef3bd6fd3dacbaaceb4f3c79e6e68b3030c60bc9e86b99ade011c882d20d3ae9`; 0.0.5/0.0.6/0.0.7 history is retained separately.

Two offline wheel builds matched byte for byte. RECORD, metadata, source ZIP
and packaged resources matched. Fixed catalog `3c739e1a5c177d585db3ed63868725dae5cadc32`, Host `1840c8e4f646992ddaebea3139c8895f29743a8f` and
lock `eca122787362dc7d39b309b931c5e17ce7fb0507f79524589f2978bb018c17e7` checks retain `review_status=not_reviewed`; human/runtime review
in that static checker remains pending. The 215 source lifecycle checks, 139
package/settlement checks and four independent source counterexamples each
passed within their own scope; they are not added into a unique-test total.

The exact installed report `PUBLIC_INSTALLED_HTTP_LIFECYCLE_ACCEPTANCE.json` passed two raw TCP
HTTP rounds and two real Host SDK auto-negotiation/automatic DELETE rounds,
all DELETEs returning 200 while cleanup_verified remained false with original
never-started proof. Native temporary-check install/uninstall, retained
installation lease until server shutdown and owned-file hash equality passed.
It launched no execution host, performed no desktop input and called no model
API. This is installed HTTP/SDK lifecycle evidence, not new Amadeus/Pi GUI
execution. Old GUI author results are not rerun or recounted here.

The first external harness attempt is retained separately: its two raw TCP
rounds passed, then a Windows subprocess-audit Path conversion TypeError
occurred before SDK launch. Native temporary-check cleanup/uninstall succeeded;
the four original diagnostic/cleanup hashes remain in AUTHOR_VALIDATION.json.
The second complete attempt supplies the two raw TCP and two SDK rounds above.
This is not an error-free first-attempt claim, and partial rounds are not added
to the final complete-attempt count.

Connector settings, permissions, contributions, runtime kind and Host engines
remain unchanged from 0.0.7. Runtime and connector are installed and managed
separately. Recommend Runtime 0.1.11; minimum HTTP protocol 0.1.6 is not a promise
of compatibility with future patches. Disconnected recovery stays operator-only;
Pi must not use recovery tools to take over an old workflow. Same-session Main
bound-image review and explicit continuation retain existing gates.

Publication was not performed at validation freeze. Actual uploads, tag/source
identity and anonymous downloaded-asset hash verification are recorded in a
separate delivery receipt. Independent final review and catalog approval remain
the maintainers' responsibility. No new speed, token-saving or accuracy claim
is made. The already sanitized public fixed-checker reports are copied byte for
byte, retaining the original wheel-inventory list shape. They remain the original
fixed-check results bound to the wheel SHA-256 and are not represented as checks
rerun at the final source commit. Final source binding belongs to
BUILD_VERIFICATION.json, AUTHOR_VALIDATION.json and this README; the author
report records the exact original static-report hashes.

本次仅返修未启动 HTTP owner 的释放。215、139、4 项分别为原始限定范围的源码
结果，不相加；真实安装态 HTTP／Host SDK 生命周期、临时检查安装／卸载及载荷
摘要核对另列，不冒充新的 Pi GUI 验收，旧 GUI 作者结果不重算。连接器配置、权限、
贡献与模型／输入门禁不变，最低协议不是未来补丁的通用兼容承诺；断线恢复仍仅限
操作员。公开材料冻结时尚未发布，实际上传／匿名下载摘要另记 receipt，商店独立
批准仍为 `not_reviewed`。
首轮外部 harness 在 raw TCP 两轮通过后、SDK 启动前出现 Windows 审计 TypeError，
原部分结果及成功清理、四份原诊断／清理摘要继续保留；第二轮才是完整 raw2＋SDK2，
不宣称无错首跑，不把部分轮次加进最终完整轮次。
