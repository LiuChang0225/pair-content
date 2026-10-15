# Third-Party Notices

## MIT 许可内容（原样再分发，未修改）

以下内容项为 Matt Pocock 的公开 skills 仓库（MIT License, Copyright (c) 2026 Matt Pocock，
https://github.com/mattpocock/skills，上游 commit `b0618bc436ad893b3c5e84e55fba86586d34a404`，2026-10-08）
中 `skills/` 目录下对应子目录的**逐字节原样拷贝**（含 SKILL.md 及全部随包文件），未做任何修改：

- engineering（20 项）：`ask-matt`、`code-review`、`codebase-design`、`diagnosing-bugs`、
  `domain-modeling`、`grill-with-docs`、`implement`、`implement-spec`、`improve-codebase-architecture`、
  `pr`、`prototype`、`research`、`retro`、`setup-matt-pocock-skills`、`tdd`、`to-spec`、`to-tickets`、
  `triage`、`wayfinder`、`wizard`
- productivity（3 项，为上述 skill 的调用依赖）：`grill-me`、`grilling`、`handoff`

历史说明：v0.1.0 曾收录改编版 `skills/code-review` 与 `skills/tdd-unit-test`，v0.2.0 起由上游原版取代并移除。

## MIT 许可内容（改造再利用，保留原始版权声明）

以下内容项基于 Matt Pocock 的公开 skills 仓库（MIT License, Copyright (c) 2026 Matt Pocock，
https://github.com/mattpocock/skills）改造并汉化：

- `skills/requirements-parsing`（源自 engineering/to-spec，改造为面向 RFQ/会议纪要的需求解析）
- `skills/log-diagnosis`（源自 engineering/diagnosing-bugs）

## MIT 许可内容（改造再利用 — daymade/claude-code-skills）

`skills/transcript-fixer` 为 daymade 公开 skills 仓库（MIT License, Copyright (c) 2025 daymade，
https://github.com/daymade/claude-code-skills，上游 commit `b5b5173ae7ff6ace8292ec97e95d2f0dff38d59b`，
2026-10-15）中 `daymade-audio/transcript-fixer` 的原样收录（含全部 99 个 Python 脚本、25 个
references 文档、tests、requirements.txt、CHANGELOG），仅对 SKILL.md 做 4 处悬空引用修复：
`/daymade-audio:meeting-minutes-taker` 改指本库 `pair-meeting-minutes-skill`（description 与
Handoff 两处）；`/daymade-audio:asr-transcribe-to-text`（未收录，且其本地转写依赖 macOS/Apple
Silicon 的 MLX）改为 PAIR 会议记录（百炼 ASR）全量重转写路径并保留同引擎非独立佐证声明；
MLX runner 示例注释改为不可用声明。references/ 中对 asr-transcribe-to-text 的高级路径引用
（跨 ASR 引擎音频验证）保持原样：该路径依赖未收录的姊妹 skill，在 PAIR（Windows）部署按
skill 自带的证据升级政策自然降级，不构成悬空调用。

`skills/pair-meeting-minutes-skill` 基于 daymade 的公开 skills 仓库（MIT License,
Copyright (c) 2025 daymade，https://github.com/daymade/claude-code-skills，上游 commit
`1c199056100694c1be522c2f3f045b48cf51a8c2`，2026-10-15）中 `daymade-audio/meeting-minutes-taker`
改造收录。改动范围：更名为 pair-meeting-minutes-skill；移除 `disable-model-invocation`
（允许按"会议纪要/整理纪要"等触发词自动调用）；对未收录配套 skill 的悬空引用
（doc-to-markdown、transcript-fixer、pdf-creator、ppt-creator）替换为本库等价 skill
（docx-processing、pdf-processing、pptx-processing）或内联替代步骤。主体工作流、
references 模板与检查清单保持原样。v0.4.0 起 transcript-fixer 已收录为同库配对 skill，
原"内联修错字"降级方案改回指向上游设计的 transcript-fixer 预处理管线，并补充
PAIR 会议记录转写稿作为输入来源的说明。

MIT License 全文：

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 明确不使用的来源

Anthropic 官方 skills 仓库（anthropics/skills）为 "All rights reserved"，其许可明确禁止
复制、创建衍生作品与再分发。本库的 `pdf-processing`、`docx-processing`、`pptx-processing`、
`xlsx-processing` 为**原创实现**，仅依赖各自许可证允许的开源 Python 库
（pypdf: BSD-3-Clause, python-docx: MIT, python-pptx: MIT, openpyxl: MIT）。

## MCP 案例

`mcp/filesystem` 引用官方 `@modelcontextprotocol/server-filesystem`（MIT License），
本库仅包含其连接配置模板，不复制其源代码；工位侧通过包管理器运行时拉取或由桌面壳预置。
