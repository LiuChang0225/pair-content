---
name: xlsx-processing
description: 处理 Excel 工作簿：读取数据（转 Markdown/CSV）、按公式重算、生成新工作簿、多表汇总。当用户需要读写 .xlsx 文件、做数据核对或报表时使用。
---

# Excel 工作簿处理

依赖：桌面壳已捆绑 Python 与 openpyxl。脚本位于本 skill 的 `scripts/` 目录。

## 读取

```
python scripts/xlsx_read.py <输入.xlsx> [--sheet 名称] [--range A1:F50] [--format md|csv] [--out 输出文件]
```

- 缺省读第一个工作表的全部数据；大表先用 `--range` 截取表头 + 前几行看结构
- 含公式的单元格默认给出**公式文本**（`--values` 给缓存计算值——注意缓存值可能是上次保存时的旧值）

## 生成 / 追加

```
python scripts/xlsx_write.py --out 输出.xlsx --sheet 汇总 --csv 数据.csv
python scripts/xlsx_write.py <已有.xlsx> --sheet 新表 --csv 追加.csv --out 输出.xlsx
```

CSV 输入用 UTF-8；首行作表头（加粗 + 冻结）。

## 工作守则

- 永不覆盖原件；对已有工作簿的修改必须 `--out` 到新文件。
- openpyxl 不会执行公式重算：需要计算结果时，要么读缓存值并注明时效，要么用 Python 自己算并把结果写入为静态值——向用户明说是哪种。
- 数据量大时（>5000 行）不要整表进上下文，先在 Python 里聚合再汇报。
