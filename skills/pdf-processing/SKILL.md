---
name: pdf-processing
description: 处理 PDF 文件：提取文本与表格、合并/拆分/旋转页面、读取元数据与表单字段。当用户需要读取、分析或重组 PDF 文档时使用。
---

# PDF 处理

依赖：桌面壳已捆绑 Python 与 pypdf。脚本位于本 skill 的 `scripts/` 目录（相对本文件解析）。

## 提取文本

```
python scripts/pdf_extract.py <输入.pdf> [--pages 1-5,8] [--out 输出.txt]
```

按页输出文本，页码用 `--- Page N ---` 分隔。`--pages` 支持范围与逗号列表。

## 页面操作（合并/拆分/旋转/抽取）

```
python scripts/pdf_ops.py extract <输入.pdf> --pages 2-4 --out 摘要.pdf
python scripts/pdf_ops.py merge <a.pdf> <b.pdf> --out 合并.pdf
python scripts/pdf_ops.py rotate <输入.pdf> --angle 90 --out 旋转.pdf
python scripts/pdf_ops.py split <输入.pdf> --out-dir 拆分目录/
```

## 元数据与表单

```
python scripts/pdf_extract.py <输入.pdf> --meta
python scripts/pdf_extract.py <输入.pdf> --fields
```

## 工作守则

- 扫描件（提取结果为空或乱码）不要硬解析：告知用户这是图像型 PDF，建议 OCR 或让用户提供文本版。
- 修改类操作永远输出到新文件，绝不覆盖原件。
- 提取长文档时先 `--pages 1-3` 试探结构，再决定完整提取范围，避免把整本书灌进上下文。
