# -*- coding: utf-8 -*-
"""查询反洗钱系统真实表结构（数据取自 assets/aml_tables.json）。

用法：
  python aml_tables.py modules                              # 列章节与对象数
  python aml_tables.py list --module 05 --keyword 名单       # 列出候选表
  python aml_tables.py search 黑名单                         # 按表名/中文名/字段注释搜索
  python aml_tables.py show T1B_DCI                         # 看字段明细
  python aml_tables.py pick T1B_DCI T1B_DCI_ATHT --user ams  # 输出 plan.json 的 design.tables 片段

设计文档「5) 引用的数据库表」只写表级信息，字段明细用于设计说明与测试要点取证。
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DICT = os.path.join(ROOT, "assets", "aml_tables.json")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def walk(data):
    for mod in data["modules"]:
        for grp in mod["groups"]:
            for obj in grp["objects"]:
                yield mod["name"], grp["name"], obj


def match_module(mod_name, want):
    if not want:
        return True
    return want.strip() in mod_name


def cmd_modules(args):
    data = load(args.dict)
    print("%-14s %-8s %-10s %s" % ("章节", "对象数", "有字段", "分组"))
    for mod in data["modules"]:
        objs = [o for g in mod["groups"] for o in g["objects"]]
        withf = sum(1 for o in objs if o["fields"])
        groups = "、".join("%s(%d)" % (g["name"], len(g["objects"])) for g in mod["groups"])
        print("%-14s %-8d %-10d %s" % (mod["name"], len(objs), withf, groups))
    print("\n来源：%s，共 %d 个对象" % (data.get("source", ""), data.get("object_count", 0)))
    return 0


def cmd_list(args):
    data = load(args.dict)
    kw = (args.keyword or "").upper()
    n = 0
    for mod_name, grp, obj in walk(data):
        if not match_module(mod_name, args.module):
            continue
        if kw and kw not in obj["en"].upper() and kw not in (obj["cn"] or "").upper():
            continue
        note = "" if obj["fields"] else "（%s）" % (obj.get("note") or "无字段定义")
        print("%-28s %-30s %3d 字段  [%s]%s"
              % (obj["en"], obj["cn"] or "-", len(obj["fields"]), mod_name.split(" ")[0], note))
        n += 1
        if args.limit and n >= args.limit:
            print("... 已达 --limit %d，请缩小关键词" % args.limit)
            break
    if not n:
        print("未找到匹配对象，试试放宽 --keyword 或去掉 --module")
    return 0


def cmd_search(args):
    data = load(args.dict)
    kw = args.keyword.upper()
    hits = 0
    for mod_name, grp, obj in walk(data):
        if not match_module(mod_name, args.module):
            continue
        name_hit = kw in obj["en"].upper() or kw in (obj["cn"] or "").upper()
        field_hits = [f for f in obj["fields"]
                      if kw in f["code"].upper() or kw in (f["comment"] or "").upper()]
        if not name_hit and not field_hits:
            continue
        hits += 1
        print("%s  %s   [%s / %s]" % (obj["en"], obj["cn"] or "-", mod_name, grp))
        if field_hits and not name_hit:
            for f in field_hits[:3]:
                print("      %-24s %-16s %s" % (f["code"], f["type"], f["comment"][:60]))
        if hits >= args.limit:
            print("... 仅显示前 %d 个命中" % args.limit)
            break
    if not hits:
        print("未找到匹配对象")
    return 0


def cmd_show(args):
    data = load(args.dict)
    want = args.table.upper()
    found = [(m, g, o) for m, g, o in walk(data) if o["en"].upper() == want]
    if not found:
        print("字典中没有 %s。先用 search 确认表名。" % args.table)
        return 1
    m, g, o = max(found, key=lambda x: len(x[2]["fields"]))
    print("表：%s  %s" % (o["en"], o["cn"] or "-"))
    print("位置：%s / %s" % (m, g))
    if o.get("note"):
        print("说明：%s" % o["note"])
    if not o["fields"]:
        print("本文档未给出该对象字段定义。")
        return 0
    print("字段 %d 个：" % len(o["fields"]))
    print("%-30s %-18s %s" % ("字段", "类型", "注释"))
    print("-" * 96)
    for f in o["fields"]:
        print("%-30s %-18s %s" % (f["code"], f["type"], f["comment"][:80]))
    return 0


def cmd_pick(args):
    data = load(args.dict)
    index = {}
    for _m, _g, o in walk(data):
        if o["fields"] or o["en"].upper() not in index:
            index[o["en"].upper()] = o
    out = []
    miss = []
    for name in args.tables:
        o = index.get(name.upper())
        if not o:
            miss.append(name)
            continue
        out.append({"db": args.db, "user": args.user, "en": o["en"], "cn": o["cn"] or ""})
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if miss:
        print("\n未在字典中找到：%s（确认为新增表后再手写）" % "、".join(miss), file=sys.stderr)
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(description="反洗钱真实表结构查询")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, help_text):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--dict", default=DEFAULT_DICT, help="字典文件，默认 assets/aml_tables.json")
        return p

    add("modules", "列出章节").set_defaults(func=cmd_modules)

    p = add("list", "列出表")
    p.add_argument("--module", default="", help="章节号或名称片段，如 05 或 名单")
    p.add_argument("--keyword", default="", help="表名或中文名关键词")
    p.add_argument("--limit", type=int, default=80)
    p.set_defaults(func=cmd_list)

    p = add("search", "按表名/中文名/字段注释搜索")
    p.add_argument("keyword")
    p.add_argument("--module", default="")
    p.add_argument("--limit", type=int, default=30)
    p.set_defaults(func=cmd_search)

    p = add("show", "查看字段明细")
    p.add_argument("table")
    p.set_defaults(func=cmd_show)

    p = add("pick", "输出 design.tables JSON 片段")
    p.add_argument("tables", nargs="+")
    p.add_argument("--user", default="amd", help="数据库用户：ams / amd")
    p.add_argument("--db", default="Oceanbase")
    p.set_defaults(func=cmd_pick)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
