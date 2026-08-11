"""Markdown -> PDF, using only reportlab.

Written for Sanad: both Claude Skills emit Markdown reports (headings, tables,
bullets, bold), and Discord needs a PDF attachment. pandoc would need a LaTeX
install of several GB; this needs `pip install reportlab` and nothing else.

Usage:
    python md2pdf.py input.md output.pdf ["Optional Title"]
"""
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (HRFlowable, ListFlowable, ListItem, PageBreak,
                                Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

ACCENT = colors.HexColor("#1F3864")
GREY = colors.HexColor("#555555")
LIGHT = colors.HexColor("#EEF1F6")

_ss = getSampleStyleSheet()
S = {
    "h1": ParagraphStyle("h1", parent=_ss["Normal"], fontName="Helvetica-Bold",
                         fontSize=16, textColor=ACCENT, spaceBefore=10, spaceAfter=5, leading=19),
    "h2": ParagraphStyle("h2", parent=_ss["Normal"], fontName="Helvetica-Bold",
                         fontSize=12.5, textColor=ACCENT, spaceBefore=9, spaceAfter=4, leading=15),
    "h3": ParagraphStyle("h3", parent=_ss["Normal"], fontName="Helvetica-Bold",
                         fontSize=10.5, spaceBefore=7, spaceAfter=3, leading=13),
    "body": ParagraphStyle("body", parent=_ss["Normal"], fontName="Helvetica",
                           fontSize=9.5, leading=13, spaceAfter=4, alignment=TA_LEFT),
    "bullet": ParagraphStyle("bullet", parent=_ss["Normal"], fontName="Helvetica",
                             fontSize=9.5, leading=12.5, spaceAfter=1.5),
    "cell": ParagraphStyle("cell", parent=_ss["Normal"], fontName="Helvetica",
                           fontSize=8.5, leading=11),
    "cellh": ParagraphStyle("cellh", parent=_ss["Normal"], fontName="Helvetica-Bold",
                            fontSize=8.5, leading=11, textColor=colors.white),
    "quote": ParagraphStyle("quote", parent=_ss["Normal"], fontName="Helvetica-Oblique",
                            fontSize=9.5, leading=13, leftIndent=10,
                            textColor=GREY, spaceAfter=4),
}


def inline(text):
    """Convert inline markdown to reportlab's mini-HTML. Order matters."""
    text = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    text = re.sub(r"`([^`]+)`", r'<font face="Courier" size="8.5">\1</font>', text)
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<b><i>\1</i></b>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<font color="#1F3864"><u>\1</u></font>', text)
    return text


def is_table_row(line):
    return line.strip().startswith("|") and line.strip().endswith("|")


def is_separator(line):
    return bool(re.fullmatch(r"\|[\s:\-|]+\|", line.strip()))


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def build_table(rows):
    header, *body = rows
    data = [[Paragraph(inline(c), S["cellh"]) for c in header]]
    for r in body:
        r = r + [""] * (len(header) - len(r))
        data.append([Paragraph(inline(c), S["cell"]) for c in r[:len(header)]])

    avail = A4[0] - 34 * mm
    t = Table(data, colWidths=[avail / len(header)] * len(header), repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D2E0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def convert(md_text):
    story, lines, i = [], md_text.replace("\r\n", "\n").split("\n"), 0
    pending_bullets = []

    def flush_bullets():
        if pending_bullets:
            story.append(ListFlowable(
                [ListItem(Paragraph(inline(b), S["bullet"]), leftIndent=12)
                 for b in pending_bullets],
                bulletType="bullet", bulletFontSize=6, leftIndent=10, spaceAfter=4))
            pending_bullets.clear()

    in_fence = False
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        if line.strip().startswith("```"):
            in_fence = not in_fence
            i += 1
            continue
        if in_fence:
            flush_bullets()
            story.append(Paragraph(
                inline(line) or "&nbsp;",
                ParagraphStyle("code", parent=S["body"], fontName="Courier",
                               fontSize=8, leading=10, leftIndent=8, spaceAfter=0)))
            i += 1
            continue

        if not line.strip():
            flush_bullets()
            i += 1
            continue

        # table
        if is_table_row(line) and i + 1 < len(lines) and is_separator(lines[i + 1]):
            flush_bullets()
            rows = [split_row(line)]
            i += 2
            while i < len(lines) and is_table_row(lines[i]):
                rows.append(split_row(lines[i]))
                i += 1
            story.append(Spacer(1, 3))
            story.append(build_table(rows))
            story.append(Spacer(1, 6))
            continue

        # horizontal rule
        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", line.strip()):
            flush_bullets()
            story.append(HRFlowable(width="100%", thickness=0.6, color=ACCENT,
                                    spaceBefore=5, spaceAfter=5))
            i += 1
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_bullets()
            level = len(m.group(1))
            style = S["h1"] if level == 1 else S["h2"] if level == 2 else S["h3"]
            story.append(Paragraph(inline(m.group(2)), style))
            i += 1
            continue

        # blockquote
        if line.strip().startswith(">"):
            flush_bullets()
            story.append(Paragraph(inline(line.strip().lstrip(">").strip()), S["quote"]))
            i += 1
            continue

        # bullets
        m = re.match(r"^\s*[-*+•]\s+(.*)$", line)
        if m:
            pending_bullets.append(m.group(1))
            i += 1
            continue

        # numbered list -> render inline so numbering is preserved verbatim
        m = re.match(r"^\s*(\d+)[.)]\s+(.*)$", line)
        if m:
            flush_bullets()
            story.append(Paragraph(f"<b>{m.group(1)}.</b> {inline(m.group(2))}",
                                   ParagraphStyle("num", parent=S["bullet"], leftIndent=12)))
            i += 1
            continue

        flush_bullets()
        story.append(Paragraph(inline(line.strip()), S["body"]))
        i += 1

    flush_bullets()
    return story


def main():
    if len(sys.argv) < 3:
        print("usage: python md2pdf.py input.md output.pdf [title]")
        raise SystemExit(2)

    src, dst = sys.argv[1], sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else "Sanad Report"

    with open(src, encoding="utf-8") as f:
        md = f.read()

    doc = SimpleDocTemplate(
        dst, pagesize=A4,
        leftMargin=17 * mm, rightMargin=17 * mm,
        topMargin=15 * mm, bottomMargin=15 * mm,
        title=title, author="Sanad",
    )
    doc.build(convert(md))
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
