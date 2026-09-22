#!/usr/bin/env python3
"""PDF 页面操作：extract / merge / rotate / split（pypdf）。永不覆盖输入文件。"""
import argparse
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_extract import parse_pages


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_ex = sub.add_parser("extract", help="抽取指定页为新 PDF")
    p_ex.add_argument("pdf")
    p_ex.add_argument("--pages", required=True)
    p_ex.add_argument("--out", required=True)

    p_mg = sub.add_parser("merge", help="合并多个 PDF")
    p_mg.add_argument("pdfs", nargs="+")
    p_mg.add_argument("--out", required=True)

    p_ro = sub.add_parser("rotate", help="旋转页面")
    p_ro.add_argument("pdf")
    p_ro.add_argument("--angle", type=int, default=90)
    p_ro.add_argument("--pages", help="缺省为全部页")
    p_ro.add_argument("--out", required=True)

    p_sp = sub.add_parser("split", help="按页拆分为多个 PDF")
    p_sp.add_argument("pdf")
    p_sp.add_argument("--out-dir", required=True)

    args = ap.parse_args()

    if args.cmd == "extract":
        reader = PdfReader(args.pdf)
        writer = PdfWriter()
        for i in parse_pages(args.pages, len(reader.pages)):
            writer.add_page(reader.pages[i])
        with open(args.out, "wb") as fh:
            writer.write(fh)
        print(f"已抽取 {len(writer.pages)} 页 -> {args.out}")
    elif args.cmd == "merge":
        writer = PdfWriter()
        for path in args.pdfs:
            writer.append(path)
        with open(args.out, "wb") as fh:
            writer.write(fh)
        print(f"已合并 {len(args.pdfs)} 个文件 -> {args.out}")
    elif args.cmd == "rotate":
        reader = PdfReader(args.pdf)
        targets = set(parse_pages(args.pages, len(reader.pages))) if args.pages else set(range(len(reader.pages)))
        writer = PdfWriter()
        for i, page in enumerate(reader.pages):
            if i in targets:
                page.rotate(args.angle)
            writer.add_page(page)
        with open(args.out, "wb") as fh:
            writer.write(fh)
        print(f"已旋转 {len(targets)} 页 x {args.angle}° -> {args.out}")
    elif args.cmd == "split":
        reader = PdfReader(args.pdf)
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        stem = Path(args.pdf).stem
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            target = out_dir / f"{stem}-p{i + 1:03d}.pdf"
            with open(target, "wb") as fh:
                writer.write(fh)
        print(f"已拆分为 {len(reader.pages)} 个文件 -> {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
