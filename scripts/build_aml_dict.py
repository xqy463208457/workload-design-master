# -*- coding: utf-8 -*-
"""把《AML_6.0数据库表结构文档.docx》抽取为结构化字典，供设计文档引用真实表结构。

用法：
  python build_aml_dict.py "<表结构文档.docx>" [--out assets/aml_tables.json] [--index references/aml-table-index.md]

抽取规则（对应文档实际版式）：
  一级标题  01 系统管理        -> 模块
  二级标题  表的清单/视图的清单 -> 分组
  二级标题  表 XX / 视图 XX    -> 对象标题
  紧随其后的表格：
      表头 名称|代码           -> 对象中文名与英文名
      表头 名称|代码|长度|数据类型|注释 -> 字段行
"""
import argparse
import json
import os
import re
import sys

try:
    import docx
    from docx.table import Table
    from docx.text.paragraph import Paragraph
except ImportError:
    print("缺少依赖：python -m pip install python-docx", file=sys.stderr)
    raise

OBJ_HEAD = re.compile(r"^(表|视图)\s*([A-Za-z0-9_]+)\s*(?:[（(].*[）)]\s*)?$")


def clean(text):
    return re.sub(r"\s+", " ", text).strip()


def iter_block(doc):
    for child in doc.element.body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag == "p":
            yield "p", Paragraph(child, doc)
        elif tag == "tbl":
            yield "t", Table(child, doc)


def cell_text(row):
    return [c.text.strip() for c in row.cells]


def extract(path):
    doc = docx.Document(path)
    blocks = list(iter_block(doc))

    modules = []
    cur_mod = None
    cur_group = None
    cur_obj = None
    pending_names = {}      # 英文名 -> 中文名（来自"表的清单"）

    def close_obj():
        nonlocal cur_obj
        if cur_obj is not None and cur_group is not None:
            cur_group["objects"].append(cur_obj)
        cur_obj = None

    i = 0
    while i < len(blocks):
        kind, blk = blocks[i]
        if kind == "p":
            style = blk.style.name
            text = blk.text.strip()
            if style == "Heading 1" and text:
                close_obj()
                cur_mod = {"name": text, "groups": []}
                modules.append(cur_mod)
                cur_group = None
            elif style == "Heading 2" and text:
                close_obj()
                cur_group = {"name": text, "objects": [], "listed": {}}
                if cur_mod is not None:
                    cur_mod["groups"].append(cur_group)
            elif style in ("Heading 3", "Heading 4") and text:
                close_obj()
                m = OBJ_HEAD.match(text)
                if m and cur_group is not None:
                    cur_obj = {"type": m.group(1), "en": m.group(2),
                               "cn": "", "fields": []}
            i += 1
            continue

        # 表格
        if blk.rows:
            header = [clean(x) for x in cell_text(blk.rows[0])]
            if header[:2] == ["名称", "代码"] and len(header) == 2:
                for row in blk.rows[1:]:
                    c = [clean(x) for x in cell_text(row)]
                    if len(c) >= 2 and c[1]:
                        pending_names[c[1].upper()] = c[0]
                        if cur_group is not None:
                            cur_group["listed"][c[1].upper()] = c[0]
            elif header[:2] == ["名称", "代码"] and len(header) >= 5:
                if cur_obj is not None:
                    for row in blk.rows[1:]:
                        c = [clean(x) for x in cell_text(row)]
                        if len(c) < 5 or not c[1]:
                            continue
                        cur_obj["fields"].append({
                            "code": c[1],
                            "len": c[2],
                            "type": c[3],
                            "comment": c[4],
                        })
        i += 1
    close_obj()

    # 去重：同名对象合并，保留字段较多的一份；清单中无字段定义的对象补入
    for mod in modules:
        for grp in mod["groups"]:
            merged = {}
            order = []
            for obj in grp["objects"]:
                key = obj["en"].upper()
                if key not in merged:
                    merged[key] = obj
                    order.append(key)
                elif len(obj["fields"]) > len(merged[key]["fields"]):
                    merged[key]["fields"] = obj["fields"]
            grp["objects"] = [merged[k] for k in order]

            listed = {}
            for obj in grp["objects"]:
                listed[obj["en"].upper()] = True
            for en, cn in grp.get("listed", {}).items():
                if en not in listed:
                    grp["objects"].append({"type": "表", "en": en,
                                           "cn": cn, "fields": [],
                                           "note": "文档仅列名称，无字段定义"})
                    listed[en] = True

    # 全局补注：清单中只列名称的对象，若其他地方有字段定义，注明出处
    defined = {}
    for mod in modules:
        for grp in mod["groups"]:
            for obj in grp["objects"]:
                if obj["fields"]:
                    defined.setdefault(obj["en"].upper(), mod["name"])
    for mod in modules:
        for grp in mod["groups"]:
            for obj in grp["objects"]:
                if not obj["fields"] and obj["en"].upper() in defined:
                    obj["note"] = "文档仅列名称，字段定义见 %s" % defined[obj["en"].upper()]

    # 回填中文名，并清理中间字段
    total = 0
    for mod in modules:
        for grp in mod["groups"]:
            grp.pop("listed", None)
            for obj in grp["objects"]:
                if not obj.get("cn"):
                    obj["cn"] = pending_names.get(obj["en"].upper(), "")
                total += 1
    return modules, total


def to_index(modules, source):
    lines = ["# 反洗钱系统真实表结构索引", "",
             "> 来源：`%s`（由 `scripts/build_aml_dict.py` 自动生成，勿手改）。" % source,
             "> 用途：写详细设计「引用的数据库表」时，优先在此选取真实表；",
             "> 需要字段明细时执行 `python scripts/aml_tables.py show <表名>`，不要整份读入 JSON。", ""]
    for mod in modules:
        lines.append("## %s" % mod["name"])
        lines.append("")
        for grp in mod["groups"]:
            if not grp["objects"]:
                continue
            lines.append("### %s" % grp["name"])
            lines.append("")
            lines.append("| 表英文名 | 中文名 | 字段数 |")
            lines.append("|---|---|---|")
            for obj in grp["objects"]:
                lines.append("| %s | %s | %d |" % (obj["en"], obj["cn"] or "-", len(obj["fields"])))
            lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="抽取 AML 数据库表结构字典")
    ap.add_argument("docx")
    ap.add_argument("--out", default=os.path.join("assets", "aml_tables.json"))
    ap.add_argument("--index", default=os.path.join("references", "aml-table-index.md"))
    args = ap.parse_args()

    modules, total = extract(args.docx)
    data = {
        "source": os.path.basename(args.docx),
        "object_count": total,
        "modules": modules,
    }
    for p in (args.out, args.index):
        d = os.path.dirname(os.path.abspath(p))
        if d and not os.path.isdir(d):
            os.makedirs(d)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    with open(args.index, "w", encoding="utf-8") as f:
        f.write(to_index(modules, os.path.basename(args.docx)))

    field_total = sum(len(o["fields"]) for m in modules for g in m["groups"] for o in g["objects"])
    named = sum(1 for m in modules for g in m["groups"] for o in g["objects"] if o["cn"])
    print("模块 %d 个，对象 %d 个，字段 %d 个，其中 %d 个对象取到中文名"
          % (len(modules), total, field_total, named))
    print("字典：%s" % args.out)
    print("索引：%s" % args.index)
    return 0


if __name__ == "__main__":
    sys.exit(main())
