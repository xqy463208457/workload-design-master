# -*- coding: utf-8 -*-
"""按基础模板渲染《详细设计说明书》。

严格遵循基础模板的表达范围：封面、修改记录、目录、七、模块设计（功能设计细化）。
模板中未提供正文的章节一律不生成，不擅自补充。

用法：python render_docx.py plan.json 输出.docx
"""
import argparse
import json
import os
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BODY_FONT_CN = "宋体"
HEAD_FONT_CN = "黑体"
LATIN_FONT = "Times New Roman"


# ------------------------------------------------------------------ 基础工具
def set_run_font(run, cn=BODY_FONT_CN, size=10.5, bold=False, latin=LATIN_FONT):
    run.font.name = latin
    run.font.size = Pt(size)
    run.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), latin)
    rfonts.set(qn("w:hAnsi"), latin)
    rfonts.set(qn("w:eastAsia"), cn)


def para(doc, text="", size=10.5, bold=False, cn=BODY_FONT_CN, align=None,
         indent=True, spacing=1.5, space_before=0, space_after=0):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = spacing
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    if indent:
        pf.first_line_indent = Pt(size * 2)
    if align is not None:
        p.alignment = align
    if text:
        run = p.add_run(text)
        set_run_font(run, cn=cn, size=size, bold=bold)
    return p


def heading(doc, text, level=None, size=None, space_before=8, space_after=6,
            align=None, outline=True):
    """level 为空或 outline=False 时不进入目录，仅作视觉标题。"""
    sizes = {1: 15, 2: 13, 3: 12, 4: 10.5}
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.keep_with_next = True
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    set_run_font(run, cn=HEAD_FONT_CN, size=size or sizes.get(level or 1, 10.5), bold=True)
    if outline and level:
        ppr = p._element.get_or_add_pPr()
        outline_el = OxmlElement("w:outlineLvl")
        outline_el.set(qn("w:val"), str(level - 1))
        ppr.append(outline_el)
    return p


def make_table(doc, headers, rows, widths=None, font_size=9):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        set_run_font(run, size=font_size, bold=True)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row[:len(headers)]):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if i == 1 else WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(v))
            set_run_font(run, size=font_size)
    if widths:
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Cm(w)
    return t


def field(paragraph, instr, hint_text="按 F9 更新目录"):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr_el = OxmlElement("w:instrText")
    instr_el.set(qn("xml:space"), "preserve")
    instr_el.text = instr
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    hint = OxmlElement("w:t")
    hint.text = hint_text
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for el in (begin, instr_el, sep, hint, end):
        run._r.append(el)
    set_run_font(run, size=10.5)


def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def add_footer_page_number(section, title_text):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title_text + "    第 ")
    set_run_font(run, size=9)
    field(p, " PAGE ", "1")
    tail = p.add_run(" 页")
    set_run_font(tail, size=9)


# ------------------------------------------------------------------ 正文渲染
def build(plan, out_path):
    proj = plan.get("project", {})
    mods = plan.get("modules") or []

    system_name = proj.get("system_name", "")
    project_name = proj.get("project_name", "")
    title = proj.get("doc_title") or (project_name + "详细设计说明书")
    version = proj.get("version", "V1.0")
    date_str = proj.get("date", "")

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.top_margin, sec.bottom_margin = Cm(2.54), Cm(2.54)
    sec.left_margin, sec.right_margin = Cm(3.17), Cm(3.17)

    normal = doc.styles["Normal"]
    normal.font.name = LATIN_FONT
    normal.font.size = Pt(10.5)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT_CN)

    # ---------------- 封面
    p = doc.add_paragraph()
    r = p.add_run("本资料仅供内部使用！")
    set_run_font(r, size=9)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for _ in range(6):
        doc.add_paragraph()
    for text, size in ((system_name, 22), (project_name, 18), ("详细设计说明书", 26)):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(18)
        r = p.add_run(text)
        set_run_font(r, cn=HEAD_FONT_CN, size=size, bold=True)
    for _ in range(6):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(date_str)
    set_run_font(r, size=12)
    page_break(doc)

    # ---------------- 修改记录
    heading(doc, "修改记录", size=15, outline=False)
    make_table(doc, ["制定日期", "内容摘要", "版本", "拟稿"],
               [[date_str, project_name, version, ""]], widths=[3.6, 6.2, 2.2, 2.6])
    page_break(doc)

    # ---------------- 目录
    heading(doc, "目　录", size=15, align=WD_ALIGN_PARAGRAPH.CENTER, outline=False)
    p = doc.add_paragraph()
    field(p, ' TOC \\o "1-3" \\h \\u ')
    page_break(doc)

    # ---------------- 七、模块设计（功能设计细化）
    heading(doc, "七、 模块设计（功能设计细化）", 1, space_before=0)
    for i, m in enumerate(mods, 1):
        d = m.get("design") or {}
        heading(doc, "%d. %s" % (i, m["name"]), 2)
        para(doc, d.get("requirement_desc", ""))

        heading(doc, "1) 操作界面", 3)
        para(doc, (d.get("ui") or "无").rstrip("。") + "。")

        heading(doc, "2) 模块流程", 3)
        para(doc, d.get("flow", ""))

        heading(doc, "3) 关联模块", 3)
        para(doc, (d.get("related") or "无").rstrip("。") + "。")

        heading(doc, "4) 设计说明", 3)
        para(doc, d.get("design_note", ""))

        heading(doc, "5) 引用的数据库表", 3)
        tbls = d.get("tables") or []
        if tbls:
            db_default = proj.get("database") or "Oceanbase"
            user_default = proj.get("db_user") or ""
            make_table(doc, ["数据库", "数据库用户", "表英文名", "表中文名"],
                       [[t.get("db") or db_default, t.get("user") or user_default,
                         t.get("en", ""), t.get("cn", "")] for t in tbls],
                       widths=[2.6, 2.4, 5.4, 4.2])
        else:
            para(doc, "无。")

        heading(doc, "6) 测试要点", 3)
        points = d.get("test_points") or []
        if points:
            for pt in points:
                para(doc, pt)
        else:
            para(doc, "无。")

    add_footer_page_number(sec, title)
    out_path = safe_save(doc, out_path)
    print("已生成详细设计说明书：%s" % out_path)
    print("  仅含模板内容：封面 + 修改记录 + 目录 + 七、模块设计（%d 个模块，每模块 6 个小节）" % len(mods))
    return 0


def safe_save(doc, out_path):
    """目标文件被占用（如已在 Word/WPS 中打开）时另存为带时间戳的文件，不静默失败。"""
    try:
        doc.save(out_path)
        return out_path
    except PermissionError:
        import time
        root, ext = os.path.splitext(out_path)
        alt = "%s_%s%s" % (root, time.strftime("%H%M%S"), ext)
        doc.save(alt)
        print("提示：目标文件正被占用，已改存为 %s" % os.path.basename(alt))
        return alt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("out")
    a = ap.parse_args()
    with open(a.plan, encoding="utf-8") as fh:
        plan = json.load(fh)
    sys.exit(build(plan, a.out))


if __name__ == "__main__":
    main()
