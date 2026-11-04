# -*- coding: utf-8 -*-
"""功能组工作量设计大佬 —— 人天分配核心算法库。

本模块只做数学计算与规则校验，不生成文字，不渲染文档。
所有比例参数均从已评估样例反演得到（1 人月 = 21.75 人天）。
"""
from __future__ import annotations

# ---------------------------------------------------------------- 常量

DAYS_PER_PM = 21.75  # 人月换算人天，取自模板公式 =D/21.75

STAGE_ORDER = ["需求", "设计", "开发", "技术测试", "性能测试", "业务测试", "准生产", "上线支持"]

# 六个浮动阶段在“扣除性能测试与上线支持后的剩余量”中的占比
STAGE_SHARE = {
    "需求": 0.052,
    "设计": 0.107,
    "开发": 0.390,
    "技术测试": 0.291,
    "业务测试": 0.107,
    "准生产": 0.054,
}

# 每行允许区间 (下限, 上限, 步长)
STAGE_RANGE = {
    "需求": (0.5, 2.0, 0.5),
    "设计": (1.0, 4.0, 0.5),
    "开发": (3.5, 9.5, 0.5),
    "技术测试": (2.5, 9.5, 0.25),
    "业务测试": (1.0, 3.5, 0.5),
    "准生产": (0.5, 1.5, 0.5),
}

DEV_MEAN_TARGET = 7.5  # 开发单条均值目标
DEV_HARD_CAP = 10.0    # 开发单条硬上限（绝对不可超过）

# 固定行阶段
FIXED_STAGES = ("性能测试", "上线支持")

# ---------------------------------------------------------------- 数据库命名

# 详细设计「5) 引用的数据库表」中「数据库」列固定取值
DB_NAME = "Oceanbase"

# 系统名 → 数据库用户（schema）。按顺序匹配，先命中更具体的系统名。
#   反洗钱客户尽职调查管理系统 -> amd
#   反洗钱管理系统 2.0（含“反洗钱管理系统”）-> ams
DB_USER_RULES = (
    ("反洗钱客户尽职调查", "amd"),
    ("反洗钱管理系统", "ams"),
)

DB_USER_ALIAS = {"amd": "反洗钱客户尽职调查管理系统", "ams": "反洗钱管理系统2.0"}


def resolve_db_user(system_name: str) -> str | None:
    """按系统名称推断数据库用户；无法判断时返回 None（调用方必须询问用户）。"""
    name = (system_name or "").replace(" ", "")
    for key, user in DB_USER_RULES:
        if key in name:
            return user
    return None



def _round_to(value: float, step: float) -> float:
    return round(round(value / step) * step, 4)


def perf_test_days(total: float) -> float:
    """性能测试人天：正常区间 1–3 人天，按项目规模取 1.0 / 2.0 / 3.0。"""
    if total < 150:
        return 1.0
    if total < 350:
        return 2.0
    return 3.0


def launch_days(total: float) -> float:
    """上线支持人天：固定 1 人天，不随规模变化。"""
    return 1.0


def split_remainder(rem: float, fixed_dev: float | None = None) -> dict:
    """把剩余人天按固定占比拆到六个浮动阶段。fixed_dev 给定时开发阶段锁定该值。"""
    keys = ["需求", "设计", "技术测试", "业务测试", "准生产"]
    if fixed_dev is None:
        base = sum(STAGE_SHARE.values())
        return {k: rem * STAGE_SHARE[k] / base for k in STAGE_SHARE}
    pool = rem - fixed_dev
    other_total = sum(STAGE_SHARE[k] for k in keys)
    out = {k: pool * STAGE_SHARE[k] / other_total for k in keys}
    out["开发"] = fixed_dev
    return out


def distribute_rows(total_rows: int, weights: list[float]) -> list[int]:
    """把总行数按权重分配到各模块（每模块至少 1 行，最大余数法）。"""
    n = len(weights)
    if total_rows < n:
        total_rows = n
    alloc = [1] * n
    rest = total_rows - n
    if rest <= 0:
        return alloc
    wsum = sum(weights) or float(n)
    quotas = [rest * w / wsum for w in weights]
    floors = [int(q) for q in quotas]
    alloc = [a + f for a, f in zip(alloc, floors)]
    leftover = rest - sum(floors)
    order = sorted(range(n), key=lambda i: (quotas[i] - floors[i]), reverse=True)
    for i in range(leftover):
        alloc[order[i % n]] += 1
    return alloc


# 离散化轮廓：让同一阶段的各行人天有真实的高低起伏，而非全部相同
_SPREAD = [1.30, 1.12, 0.88, 1.18, 0.78, 1.05, 1.22, 0.92, 1.14, 0.84, 1.26, 1.00]


def _pattern(count: int) -> list[float]:
    vals = [_SPREAD[i % len(_SPREAD)] for i in range(count)]
    mean = sum(vals) / count
    return [v / mean for v in vals]


def distribute_days(total: float, count: int, stage: str, weights: list[float] | None = None) -> list[float]:
    """把某阶段总量分配到 count 行：满足步长与区间，精确逼近 total，并保留高低起伏。"""
    lo, hi, step = STAGE_RANGE[stage]
    if count <= 0:
        return []
    weights = weights or [1.0] * count

    min_u, max_u = int(round(lo / step)), int(round(hi / step))
    target_units = round(total / step)
    target_units = max(min_u * count, min(target_units, max_u * count))

    mean_u = target_units / count
    pat = _pattern(count)
    units = []
    for i in range(count):
        w = (weights[i] / (sum(weights) / count)) if sum(weights) else 1.0
        u = int(round(mean_u * pat[i] * (0.75 + 0.25 * w)))
        units.append(max(min_u, min(max_u, u)))

    # 修正总量，使其严格等于 target_units
    diff = target_units - sum(units)
    guard = 0
    while diff != 0 and guard < 100000:
        order = sorted(range(count), key=lambda i: (-units[i] if diff > 0 else units[i]))
        for i in order:
            if diff > 0 and units[i] < max_u:
                units[i] += 1
                diff -= 1
            elif diff < 0 and units[i] > min_u:
                units[i] -= 1
                diff += 1
            if diff == 0:
                break
        guard += 1

    return [round(u * step, 4) for u in units]


def plan_days(total_pm: float, modules: list[dict]) -> dict:
    """根据人月与模块结构计算全表人天。

    modules: [{"name": str, "functions": [{"name": str, "complexity": 1..3}, ...]}]
    返回 {"total_days", "pm_actual", "row_count", "stages": {stage: [[days per function] per module]}}
    """
    total = total_pm * DAYS_PER_PM
    t_perf = perf_test_days(total)
    t_launch = launch_days(total)
    rem = max(total - t_perf - t_launch, 10.0)

    n_mod = len(modules)
    dev_target = rem * STAGE_SHARE["开发"] / sum(STAGE_SHARE.values())
    row_count = max(n_mod, int(round(dev_target / DEV_MEAN_TARGET)))

    # 若结构已给定功能条数，则以结构为准，并校验是否落在合理区间
    structural = sum(max(1, len(m.get("functions") or [])) for m in modules)
    if structural and structural >= n_mod:
        row_count = structural

    dev_days = round(DEV_MEAN_TARGET * row_count, 4)
    # 开发总量需落在区间内
    lo, hi, _ = STAGE_RANGE["开发"]
    dev_days = max(lo * row_count, min(hi * row_count, dev_days))

    stage_totals = split_remainder(rem, fixed_dev=dev_days)
    stage_totals["性能测试"] = t_perf
    stage_totals["上线支持"] = t_launch

    stages = {}
    for stage in STAGE_ORDER:
        if stage in FIXED_STAGES:
            stages[stage] = [[stage_totals[stage]]]
            continue
        # 逐模块逐功能行分配
        per_module = []
        flat_weights = []
        for m in modules:
            funcs = m.get("functions") or [{"name": m["name"]}]
            for f in funcs:
                flat_weights.append(float(f.get("complexity") or 2))
        flat = distribute_days(stage_totals[stage], row_count, stage, flat_weights)
        cursor = 0
        for m in modules:
            funcs = m.get("functions") or [{"name": m["name"]}]
            per_module.append(flat[cursor:cursor + len(funcs)])
            cursor += len(funcs)
        stages[stage] = per_module

    grand = 0.0
    for stage in STAGE_ORDER:
        for blk in stages[stage]:
            grand += sum(blk)

    return {
        "total_days": round(grand, 4),
        "pm_actual": round(grand / DAYS_PER_PM, 4),
        "pm_target": total_pm,
        "row_count": row_count,
        "stages": stages,
        "stage_totals": {s: round(sum(sum(b) for b in stages[s]), 4) for s in STAGE_ORDER},
    }


def check_plan(plan: dict) -> list[str]:
    """校验一份完整 plan，返回问题清单（空表示全部通过）。"""
    issues: list[str] = []
    mods = plan.get("modules") or []
    if not mods:
        return ["plan 中没有 modules"]

    names = [m["name"].strip() for m in mods]
    if len(set(names)) != len(names):
        issues.append("系统模块名称存在重复：%s" % names)

    req_items = plan.get("requirement_items")
    if req_items:
        if [x.strip() for x in req_items] != names:
            issues.append("系统模块与需求条目不一致：需求=%s 模块=%s" % (req_items, names))

    rows = 0
    dev_values: list[float] = []
    for m in mods:
        funcs = m.get("functions") or []
        if not funcs:
            issues.append("模块「%s」没有功能行" % m["name"])
        rows += len(funcs)
        for f in funcs:
            for stage in ("需求", "设计", "开发"):
                items = split_items(f.get(stage, ""))
                if stage == "开发":
                    dev_values.append(float(f.get("days", {}).get("开发", 0)))
                if not (6 <= len(items) <= 10):
                    issues.append("「%s / %s」%s 工作项描述为 %d 条，要求 6-10 条"
                                  % (m["name"], f.get("name", ""), stage, len(items)))

    for m in mods:
        d = m.get("design") or {}
        for key in ("requirement_desc", "flow", "design_note"):
            txt = (d.get(key) or "").strip()
            if len(txt) < 100:
                issues.append("模块「%s」设计文档 %s 过短（%d 字，要求约 150 字）" % (m["name"], key, len(txt)))
        if (d.get("ui") or "").strip() not in ("无", "无。"):
            issues.append("模块「%s」操作界面应填写“无”" % m["name"])
        if not d.get("test_points"):
            issues.append("模块「%s」缺少测试要点" % m["name"])
        if not (d.get("tables") or []):
            issues.append("模块「%s」未填写引用的数据库表" % m["name"])

    proj = plan.get("project") or {}
    db_user = (proj.get("db_user") or "").strip()
    db_name = (proj.get("database") or DB_NAME).strip()
    if not db_user:
        issues.append("project.db_user 为空：反洗钱管理系统2.0 填 ams，反洗钱客户尽职调查管理系统填 amd")
    for m in mods:
        for t in (m.get("design") or {}).get("tables") or []:
            en = (t.get("en") or "").strip()
            if not en:
                issues.append("模块「%s」存在空表名" % m["name"])
            if db_user and (t.get("user") or "").strip() not in ("", db_user):
                issues.append("模块「%s」表 %s 的数据库用户为 %s，与项目库用户 %s 不一致"
                              % (m["name"], en, t.get("user"), db_user))
            if (t.get("db") or "").strip() not in ("", db_name):
                issues.append("模块「%s」表 %s 的数据库应为 %s" % (m["name"], en, db_name))

    if dev_values:
        mx = max(dev_values)
        mn = min(dev_values)
        avg = sum(dev_values) / len(dev_values)
        if mx > DEV_HARD_CAP:
            issues.append("开发存在超过 10 人天的行：%.2f" % mx)
        if mn < STAGE_RANGE["开发"][0] or mx > STAGE_RANGE["开发"][1]:
            issues.append("开发单条超出 3.5-9.5 区间：min=%.2f max=%.2f" % (mn, mx))
        if abs(avg - DEV_MEAN_TARGET) > 0.5:
            issues.append("开发单条均值 %.2f 偏离 7.5 过多" % avg)
        bad = [v for v in dev_values if abs(v * 10 - round(v * 10)) > 1e-6]
        if bad:
            issues.append("开发存在非 0.5 步长的行：%s" % bad)

    target = float(plan.get("project", {}).get("total_pm") or 0)
    actual = float(plan.get("allocation", {}).get("pm_actual") or 0)
    if target and abs(actual - target) > 0.15:
        issues.append("折算人月 %.2f 与目标人月 %.2f 偏差过大" % (actual, target))
    return issues


def split_items(text: str) -> list[str]:
    """把工作项描述按编号切条，用于统计条目数量。"""
    if not text:
        return []
    marks = ("1、", "2、", "3、", "4、", "5、", "6、", "7、", "8、", "9、", "10、", "11、", "12、",
             "1)、", "2)、", "3)、", "4)、", "5)、", "6)、", "7)、", "8)、", "9)、", "10)、")
    lines = [ln.strip() for ln in text.replace("\r", "").split("\n") if ln.strip()]
    counted = 0
    for ln in lines:
        if any(ln.startswith(mk) for mk in marks):
            counted += 1
    return [""] * counted
