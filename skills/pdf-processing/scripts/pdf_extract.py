#!/usr/bin/env python3
"""PDF 文本/元数据/表单字段提取（pypdf）。"""
import argparse
import sys

from pypdf import PdfReader


def parse_pages(spec: str, total: int) -> list[int]:
    pages: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            pages.extend(range(int(lo), int(hi) + 1))
        elif part:
            pages.append(int(part))
    return [p - 1 for p in pages if 1 <= p <= total]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf")
    ap.add_argument("--pages", help="页码范围，如 1-5,8（1 起）")
    ap.add_argument("--out", help="输出文件（默认 stdout）")
    ap.add_argument("--meta", action="store_true", help="输出元数据")
    ap.add_argument("--fields", action="store_true", help="输出表单字段")
    args = ap.parse_args()

    reader = PdfReader(args.pdf)
    lines: list[str] = []

    if args.meta:
        meta = reader.metadata or {}
        lines.append(f"pages: {len(reader.pages)}")
        for key in ("/Title", "/Author", "/Subject", "/Creator", "/Producer", "/CreationDate"):
            if meta.get(key):
                lines.append(f"{key.strip('/')}: {meta[key]}")
    elif args.fields:
        fields = reader.get_fields() or {}
        if not fields:
            lines.append("(无表单字段)")
        for name, field in fields.items():
            lines.append(f"{name}\ttype={field.get('/FT')}\tvalue={field.get('/V', '')}")
    else:
        targets = parse_pages(args.pages, len(reader.pages)) if args.pages else range(len(reader.pages))
        for i in targets:
            lines.append(f"--- Page {i + 1} ---")
            lines.append(reader.pages[i].extract_text() or "(无文本，可能为扫描件)")

    text = "\n".join(lines)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"已写入 {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
