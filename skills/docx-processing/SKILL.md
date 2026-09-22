---
name: docx-processing
description: 处理 Word 文档：提取文本（保留标题层级）、读取表格、从 Markdown 生成 docx、修改替换文本。当用户需要读写 .docx 文件时使用。
---

# Word 文档处理

依赖：桌面壳已捆绑 Python 与 python-docx。脚本位于本 skill 的 `scripts/` 目录。

## 提取内容

```
python scripts/docx_extract.py <输入.docx> [--tables] [--out 输出.md]
```

- 默认输出全文，标题按 `#`/`##` 层级转 Markdown，便于模型阅读
- `--tables` 同时把表格转为 Markdown 表格

## 从 Markdown 生成 docx

```
python scripts/docx_generate.py <输入.md> --out 输出.docx [--template 模板.docx]
```

支持 `#` 标题层级、列表、粗体/斜体、表格。`--template` 指定公司模板时沿用其样式（字体、页眉页脚），没有模板时用默认样式。**给同事交付文档时优先问有没有公司模板。**

## 文本替换

```
python scripts/docx_generate.py <输入.docx> --replace "旧文本=新文本" --out 输出.docx
```

## 工作守则

- 永不覆盖原件，输出到新文件。
- 提取长文档先输出到文件再按需分段读取，避免一次性灌满上下文。
- 复杂排版（文本框、SmartArt、公式）python-docx 不支持提取，遇到时明确告知用户局限，不要假装内容完整。
