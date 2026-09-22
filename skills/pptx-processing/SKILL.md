---
name: pptx-processing
description: 处理 PowerPoint 演示文稿：提取大纲与备注、从大纲生成 pptx、基于公司模板填充内容。当用户需要读取或制作 .pptx 时使用。
---

# PowerPoint 处理

依赖：桌面壳已捆绑 Python 与 python-pptx。脚本位于本 skill 的 `scripts/` 目录。

## 提取大纲

```
python scripts/pptx_extract.py <输入.pptx> [--notes] [--out 输出.md]
```

按页输出标题 + 正文要点 + 演讲者备注（`--notes`），转 Markdown 大纲。

## 从大纲生成

```
python scripts/pptx_generate.py <大纲.md> --out 输出.pptx [--template 公司模板.pptx] [--title "演示标题"]
```

大纲格式约定：`#` = 节标题页，`##` = 一页幻灯片（标题），`-` 列表项 = 正文要点。
`--template` 提供公司模板时沿用其母版与版式（**做正式汇报前先问用户要模板**）；无模板用简洁默认版式。

## 工作守则

- 永不覆盖原件。
- python-pptx 不渲染图形/动画/SmartArt，提取时遇到会标注 `[无法提取的形状]`，如实告知用户。
- 生成幻灯片时每页要点不超过 6 条、每条不超过 2 行——超了就拆页，不要塞字。
- 图表类内容优先建议用户在 Excel 中做好后粘贴，脚本生成的原生图表能力有限。
