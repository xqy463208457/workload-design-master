# -*- coding: utf-8 -*-
"""工作量计划命令行工具。

用法：
  python plan.py init  --pm 7.5 --project "XX项目" --system "反洗钱管理系统2.0" \
                       --modules "受益所有人核验:2,差异分析管理:2,查询管理:1" --out plan.json
  python plan.py fill  plan.json
  python plan.py check plan.json
  python plan.py show  plan.json
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wldlib


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def parse_modules(spec):
    """解析 '模块A:2,模块B:1' -> [(name, weight)]"""
    out = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" in chunk:
            name, w = chunk.rsplit(":", 1)
            out.append((name.strip(), float(w)))
        else:
            out.append((chunk, 1.0))
    return out


def cmd_init(args):
    mods = parse_modules(args.modules)
    if not mods:
        print("错误：--modules 不能为空", file=sys.stderr)
        return 2

    db_user = (args.db_user or "").strip() or wldlib.resolve_db_user(args.system)
    if not db_user:
        print("错误：无法从系统名称「%s」推断数据库用户。" % (args.system or ""), file=sys.stderr)
        print("      反洗钱管理系统2.0 用 --db-user ams；反洗钱客户尽职调查管理系统 用 --db-user amd。",
              file=sys.stderr)
        return 2

    # 先按权重估算行数，产出骨架
    total = args.pm * wldlib.DAYS_PER_PM
    rem = max(total - wldlib.perf_test_days(total) - wldlib.launch_days(total), 10.0)
    dev_target = rem * wldlib.STAGE_SHARE["开发"] / sum(wldlib.STAGE_SHARE.values())
    row_count = max(len(mods), int(round(dev_target / wldlib.DEV_MEAN_TARGET)))
    counts = wldlib.distribute_rows(row_count, [w for _, w in mods])

    modules = []
    for (name, _w), cnt in zip(mods, counts):
        funcs = [{"name": "%s-功能%d" % (name, i + 1), "complexity": 2,
                  "需求": "", "设计": "", "开发": "", "技术测试": "", "业务测试": "", "准生产": ""}
                 for i in range(cnt)]
        modules.append({
            "name": name,
            "functions": funcs,
            "design": {
                "requirement_desc": "", "ui": "无", "flow": "", "related": "无",
                "design_note": "",
                "tables": [],
                "test_points": [],
            },
        })

    plan = {
        "project": {
            "system_name": args.system or "XX系统",
            "project_name": args.project or "XX项目",
            "doc_title": (args.project or "XX项目") + "详细设计说明书",
            "version": args.version,
            "date": args.date or "",
            "total_pm": args.pm,
            "database": wldlib.DB_NAME,
            "db_user": db_user,
        },
        "requirement_items": [n for n, _ in mods],
        "modules": modules,
    }
    plan["allocation"] = wldlib.plan_days(args.pm, modules)
    save(args.out, plan)

    print("已生成骨架：%s" % args.out)
    print("数据库：%s / 数据库用户：%s（系统：%s）"
          % (plan["project"]["database"], db_user, args.system or "未指定"))
    print("总人天目标 %.2f（%.2f 人月 → %.2f 人天），功能行数 %d，模块数 %d"
          % (plan["allocation"]["total_days"], args.pm, args.pm * wldlib.DAYS_PER_PM,
             plan["allocation"]["row_count"], len(modules)))
    print("各模块功能行数：")
    for m in modules:
        print("  - %-40s %d 行" % (m["name"][:40], len(m["functions"])))
    print("阶段人天：%s" % json.dumps(plan["allocation"]["stage_totals"], ensure_ascii=False))
    print("下一步：填写各功能的 需求/设计/开发/技术测试/业务测试/准生产 文案与 design 内容，再执行 fill。")
    print("      写测试三段前先读 references/test-case-spec.md（固定导语、场景五要素、维度矩阵）。")
    return 0


def cmd_fill(args):
    plan = load(args.plan)
    mods = plan["modules"]
    for m in mods:
        for f in m.get("functions") or []:
            f.setdefault("complexity", 2)
    plan["allocation"] = wldlib.plan_days(float(plan["project"]["total_pm"]), mods)

    # 把人天回填到每个功能行，便于阅读与二次核对
    for si, stage in enumerate(wldlib.STAGE_ORDER):
        for mi, m in enumerate(mods):
            funcs = m.get("functions") or [{"name": m["name"]}]
            block = plan["allocation"]["stages"][stage]
            if stage in wldlib.FIXED_STAGES:
                continue
            for fi, f in enumerate(funcs):
                f.setdefault("days", {})[stage] = block[mi][fi]

    save(args.plan, plan)
    print("已回填人天：总计 %.2f 人天（%.4f 人月），功能行数 %d"
          % (plan["allocation"]["total_days"], plan["allocation"]["pm_actual"],
             plan["allocation"]["row_count"]))
    print("阶段人天：%s" % json.dumps(plan["allocation"]["stage_totals"], ensure_ascii=False))
    return 0


def cmd_check(args):
    plan = load(args.plan)
    issues = wldlib.check_plan(plan)
    if not issues:
        print("校验通过：模块名称一致、开发单条在 3.5-9.5 且均值≈7.5、各阶段条目数 6-10 条、"
              "测试三段导语与场景句式合规（业务场景数≤技术测试场景数）、"
              "设计文档段落齐备、库用户（%s）与表清单一致。" % (plan.get("project", {}).get("db_user") or "-"))
        return 0
    print("发现 %d 个问题：" % len(issues))
    for i, msg in enumerate(issues, 1):
        print("  %2d. %s" % (i, msg))
    return 1


def cmd_show(args):
    plan = load(args.plan)
    print("项目：%s" % plan["project"].get("project_name"))
    print("系统：%s" % plan["project"].get("system_name"))
    print("目标人月：%s  实际折算：%.4f" % (plan["project"].get("total_pm"),
                                            plan.get("allocation", {}).get("pm_actual", 0)))
    print("阶段人天：%s" % json.dumps(plan.get("allocation", {}).get("stage_totals", {}), ensure_ascii=False))
    print("-" * 76)
    for m in plan["modules"]:
        print("[%s] %d 条功能" % (m["name"], len(m.get("functions") or [])))
        for f in m.get("functions") or []:
            days = f.get("days") or {}
            print("   - %-38s 需求%.2f 设计%.2f 开发%.2f" % (f["name"][:38],
                  days.get("需求", 0), days.get("设计", 0), days.get("开发", 0)))
    return 0


def main():
    ap = argparse.ArgumentParser(description="功能组工作量设计大佬 —— 计划工具")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("init", help="生成计划骨架")
    p1.add_argument("--pm", type=float, required=True, help="人月，例如 7.5")
    p1.add_argument("--project", default="", help="项目名称")
    p1.add_argument("--system", default="", help="系统名称（决定数据库用户：反洗钱管理系统2.0→ams，反洗钱客户尽职调查管理系统→amd）")
    p1.add_argument("--db-user", default="", help="数据库用户，默认按系统名称推断，可显式覆盖")
    p1.add_argument("--modules", required=True, help="模块清单，格式 名称:权重,名称:权重")
    p1.add_argument("--version", default="V1.0")
    p1.add_argument("--date", default="")
    p1.add_argument("--out", default="plan.json")
    p1.set_defaults(func=cmd_init)

    p2 = sub.add_parser("fill", help="按当前结构重算并回填人天")
    p2.add_argument("plan")
    p2.set_defaults(func=cmd_fill)

    p3 = sub.add_parser("check", help="校验计划是否满足全部规则")
    p3.add_argument("plan")
    p3.set_defaults(func=cmd_check)

    p4 = sub.add_parser("show", help="打印计划摘要")
    p4.add_argument("plan")
    p4.set_defaults(func=cmd_show)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
