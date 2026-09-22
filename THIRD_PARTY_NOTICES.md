# Third-Party Notices

## MIT 许可内容（改造再利用，保留原始版权声明）

以下内容项基于 Matt Pocock 的公开 skills 仓库（MIT License, Copyright (c) 2026 Matt Pocock，
https://github.com/mattpocock/skills）改造并汉化：

- `skills/code-review`（源自 engineering/code-review）
- `skills/tdd-unit-test`（源自 engineering/tdd，含 tests.md 与 mocking.md 要点）
- `skills/log-diagnosis`（源自 engineering/diagnosing-bugs）

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
