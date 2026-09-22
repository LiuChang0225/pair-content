#!/usr/bin/env python3
"""xlsx 生成/追加：CSV -> 工作表（openpyxl），首行表头加粗冻结。永不覆盖输入。"""
import argparse
import csv
import sys

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("xlsx", nargs="?", help="已有工作簿（追加模式）；缺省为新建")
    ap.add_argument("--sheet", required=True, help="目标工作表名")
    ap.add_argument("--csv", required=True, help="UTF-8 CSV 输入")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    with open(args.csv, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        raise SystemExit(f"{args.csv} 为空")

    wb = load_workbook(args.xlsx) if args.xlsx else Workbook()
    if args.xlsx is None and "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])
    if args.sheet in wb.sheetnames:
        raise SystemExit(f"工作表 '{args.sheet}' 已存在（不覆盖已有数据；换名或先删除）")
    ws = wb.create_sheet(args.sheet)

    for row in rows:
        ws.append(row)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    ws.freeze_panes = "A2"
    # 粗略列宽自适应（上限 60）
    for col in ws.columns:
        width = max((len(str(c.value)) for c in col if c.value is not None), default=8)
        ws.column_dimensions[col[0].column_letter].width = min(width + 2, 60)

    wb.save(args.out)
    print(f"已写入工作表 '{args.sheet}'（{len(rows)} 行）-> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
