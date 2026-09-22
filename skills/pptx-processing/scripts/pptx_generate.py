#!/usr/bin/env python3
"""从 Markdown 大纲生成 pptx（python-pptx）。

约定：`#` 节标题页；`##` 幻灯片页标题；`-`/`*` 列表项为正文要点。
--template 沿用公司模板的母版版式（版式 0=标题页，1=标题+内容，按模板实际布局尽力匹配）。
"""
import argparse
import re
import sys

from pptx import Presentation
from pptx.util import Pt


def pick_layout(prs, kind: str):
    layouts = prs.slide_layouts
    if kind == "section":
        for layout in layouts:
            name = layout.name.lower()
            if "section" in name or "节" in layout.name:
                return layout
        return layouts[0]
    for layout in layouts:
        name = layout.name.lower()
        if "content" in name or "内容" in layout.name or "bullet" in name:
            return layout
    return layouts[min(1, len(layouts) - 1)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("outline", help="Markdown 大纲文件")
    ap.add_argument("--out", required=True)
    ap.add_argument("--template", help="公司模板 .pptx")
    ap.add_argument("--title", help="首页标题（缺省用大纲第一个 # 或文件名）")
    args = ap.parse_args()

    prs = Presentation(args.template) if args.template else Presentation()

    lines = open(args.outline, encoding="utf-8").read().splitlines()
    doc_title = args.title or next((l.lstrip("# ").strip() for l in lines if l.startswith("# ")), "演示文稿")

    # 首页
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = doc_title
    if len(slide.placeholders) > 1:
        slide.placeholders[1].text = ""

    current: list[tuple[str, list[str]]] | None = None
    slides: list[tuple[str, list[str], str]] = []  # (kind, title, bullets)
    kind = "content"
    title = None
    bullets: list[str] = []

    def flush():
        if title is not None:
            slides.append((kind, title, list(bullets)))

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            section_title = stripped[2:].strip()
            if section_title == doc_title:
                continue  # 大纲首个 # 与演示标题重复，不另起节页
            flush()
            kind, title, bullets = "section", section_title, []
        elif stripped.startswith("## "):
            flush()
            kind, title, bullets = "content", stripped[3:].strip(), []
        elif re.match(r"^[-*]\s+", stripped) and title is not None:
            bullet = re.sub(r"^[-*]\s+", "", stripped)
            bullet = re.sub(r"\*\*(.+?)\*\*|\*([^*]+?)\*|`([^`]+?)`", lambda m: m.group(1) or m.group(2) or m.group(3), bullet)
            bullets.append(bullet)
    flush()

    for kind, title, bullets in slides:
        slide = prs.slides.add_slide(pick_layout(prs, kind))
        if slide.shapes.title is not None:
            slide.shapes.title.text = title
        body_ph = next(
            (p for p in slide.placeholders if p.placeholder_format.idx != 0 and p.has_text_frame),
            None,
        )
        if body_ph is not None:
            tf = body_ph.text_frame
            tf.clear()
            for i, bullet in enumerate(bullets):
                para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                para.text = bullet
                para.font.size = Pt(18)
        elif bullets:
            print(f"警告：页 '{title}' 模板无正文占位符，{len(bullets)} 条要点未写入", file=sys.stderr)

    prs.save(args.out)
    print(f"已生成 {len(slides) + 1} 页 -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
