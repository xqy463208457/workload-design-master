# -*- coding: utf-8 -*-
"""按 bank-workload 模板渲染《项目工作量评估表》。

用法：python render_xlsx.py plan.json 输出.xlsx [--template 模板.xlsx]
"""
import argparse
import json
import math
import os
import shutil
import sys

import openpyxl
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wldlib

STAGE_CN = wldlib.STAGE_ORDER

NOTE_REQ = ("含义:此部分仅包括科技外包人员将业务需求转化为软件需求需要的工作量，"
            "不含业务部门提出、编写需求规格说明书的工作量。")
NOTE_BIZ = ("含义:此部分仅包括科技外包人员协助业务人员开展测试的工作量，"
            "不含业务部门编写案例、执行测试过程的工作量。")

DEFAULT_PERF = """1.与性能测试团队沟通，进行业务场景评测，沟通测试场景及测试方案
2.验证核心交易在业务高峰并发量下的响应时延、成功率与资源占用
3.验证批量任务与报表类功能在历史全量数据下的执行耗时
4.按照既定的交易占比进行测试，验证系统处理能力及服务器资源消耗情况
5.验证系统稳定运行 8 小时情况，是否存在内存泄漏等现象"""

DEFAULT_LAUNCH = """1、准备镜像晋级，代码封版；
2、编写上云部署序列、监控告警配置等上线序列文件；
3、参数配置、字典数据、业务流程配置等基础数据投产初始化与核对；
4、配合进行投产支持，投产首日驻场保障及核心链路验证。"""

THIN = Side(style="thin", color="FF000000")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# 列宽（字符）用于估算行高：合并后的可见宽度
COL_W = {"B": 16.88, "C": 22.5, "D": 12.5, "E": 8.43, "F": 9.38, "G": 8.43,
         "H": 8.43, "I": 8.43, "J": 8.43, "K": 33.56, "L": 18.75,
         "M": 13.75, "N": 13.75, "O": 40.88}


def est_height(text, width_units, min_h=26.0):
    """按合并宽度估算行高（中文按 2 个宽度单位）。"""
    if not text:
        return min_h
    cpl = max(width_units / 2.05, 6)
    lines = 0
    for seg in str(text).replace("\r", "").split("\n"):
        lines += max(1, math.ceil(len(seg) / cpl))
    return min(max(min_h, lines * 15.2 + 6), 409)


def build_rows(plan):
    """展开为逐行数据：[(stage, module, function, desc, days, is_stage_top, is_module_top)]"""
    mods = plan["modules"]
    alloc = plan["allocation"]["stages"]
    fixed = plan.get("fixed_rows") or {}
    rows = []

    for stage in STAGE_CN:
        if stage == "性能测试":
            txt = fixed.get("性能测试") or DEFAULT_PERF
            rows.append([stage, "性能测试", "性能测试方案与测试", txt, alloc["性能测试"][0][0], True, True])
            continue
        if stage == "上线支持":
            txt = fixed.get("上线支持") or DEFAULT_LAUNCH
            rows.append([stage, "上线准备与投产支持", "上线准备与投产支持", txt, alloc["上线支持"][0][0], True, True])
            continue
        for mi, m in enumerate(mods):
            funcs = m.get("functions") or []
            for fi, f in enumerate(funcs):
                days = alloc[stage][mi][fi]
                rows.append([stage, m["name"], f.get("name", ""), f.get(stage, ""), days,
                             fi == 0, fi == 0])
    return rows


def prepare_target(out_path):
    """目标文件被占用（如已在 Excel/WPS 中打开）时改用带时间戳的备用名，不静默失败。"""
    try:
        if os.path.exists(out_path):
            with open(out_path, "ab"):
                pass
        return out_path
    except PermissionError:
        import time
        root, ext = os.path.splitext(out_path)
        alt = "%s_%s%s" % (root, time.strftime("%H%M%S"), ext)
        print("提示：目标文件正被占用，已改存为 %s" % os.path.basename(alt))
        return alt


def render(plan_path, out_path, template):
    with open(plan_path, encoding="utf-8") as fh:
        plan = json.load(fh)

    out_path = prepare_target(out_path)
    shutil.copyfile(template, out_path)
    wb = openpyxl.load_workbook(out_path)
    ws = wb["项目工作量评估表"]

    # 清空第 5 行及以下
    if ws.max_row >= 5:
        for rng in list(ws.merged_cells.ranges):
            if rng.min_row >= 5:
                ws.unmerge_cells(str(rng))
        ws.delete_rows(5, ws.max_row - 4)

    proj = plan["project"]
    ws["B3"] = "项目编号："
    ws["E3"] = "项目名称：%s" % proj.get("project_name", "")
    ws["L3"] = "系统名称：%s" % proj.get("system_name", "")
    for ref in ("B3", "E3", "L3"):
        ws[ref].font = Font(name="宋体", size=12)
        ws[ref].alignment = Alignment(horizontal="left", vertical="center")

    rows = build_rows(plan)
    r = 5
    for stage, module, func, desc, days, stage_top, module_top in rows:
        ws.cell(r, 2, stage if stage_top else None)
        ws.cell(r, 3, module if module_top else None)
        ws.cell(r, 4, func)
        ws.cell(r, 6, desc)
        ws.cell(r, 13, days)
        for c in range(2, 16):
            cell = ws.cell(r, c)
            cell.border = BORDER
            cell.font = Font(name="宋体", size=11)
            if c in (2, 3, 13):
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            elif c == 4:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws.cell(r, 13).number_format = "0.0_ "
        ws.row_dimensions[r].height = max(
            est_height(desc, COL_W["F"] + sum(COL_W[k] for k in "GHIJK"), 60.0),
            est_height(module, COL_W["C"], 26.0),
            est_height(func, COL_W["D"] + COL_W["E"], 26.0),
        )
        r += 1

    # 合并：阶段块、模块块、功能 D:E、描述 F:K、合计 N
    start = 5
    idx = 0
    while idx < len(rows):
        stage = rows[idx][0]
        end = idx
        while end + 1 < len(rows) and rows[end + 1][0] == stage:
            end += 1
        r1, r2 = 5 + idx, 5 + end
        if r2 > r1:
            ws.merge_cells("B%d:B%d" % (r1, r2))
        if stage not in wldlib.FIXED_STAGES:
            # 模块块合并 C
            i = idx
            while i <= end:
                j = i
                while j + 1 <= end and rows[j + 1][1] == rows[i][1]:
                    j += 1
                if j > i:
                    ws.merge_cells("C%d:C%d" % (5 + i, 5 + j))
                i = j + 1
        ws.merge_cells("N%d:N%d" % (r1, r2)) if r2 > r1 else None
        ws.cell(r1, 14, "=SUM(M%d:M%d)" % (r1, r2))
        ws.cell(r1, 14).number_format = "0.0_ "
        ws.cell(r1, 14).font = Font(name="宋体", size=11)
        ws.cell(r1, 14).alignment = Alignment(horizontal="center", vertical="center")
        ws.cell(r1, 14).border = BORDER

        note = None
        if stage == "需求":
            note = NOTE_REQ
        elif stage in ("业务测试",):
            note = NOTE_BIZ
        if note:
            ws.cell(r1, 15, note)
            ws.cell(r1, 15).font = Font(name="宋体", size=9)
            ws.cell(r1, 15).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            ws.cell(r1, 15).border = BORDER
            if r2 > r1:
                ws.merge_cells("O%d:O%d" % (r1, r2))
        idx = end + 1
        start = r2 + 1

    # 合并每行 D:E、F:K
    for i in range(len(rows)):
        rr = 5 + i
        ws.merge_cells("D%d:E%d" % (rr, rr))
        ws.merge_cells("F%d:K%d" % (rr, rr))

    # 总计
    last = 4 + len(rows)
    tr1 = last + 1
    ws.cell(tr1, 2, "总计（人天）")
    ws.cell(tr1, 4, "=SUM(N5:N%d)" % last)
    ws.cell(tr1 + 1, 2, "总计（人月）")
    ws.cell(tr1 + 1, 4, "=D%d/21.75" % tr1)
    for rr in (tr1, tr1 + 1):
        for c in range(2, 16):
            cell = ws.cell(rr, c)
            cell.border = BORDER
            cell.font = Font(name="宋体", size=11, bold=(c in (2, 4)))
            cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[rr].height = 26.0
    ws.merge_cells("B%d:C%d" % (tr1, tr1))
    ws.merge_cells("D%d:O%d" % (tr1, tr1))
    ws.merge_cells("B%d:C%d" % (tr1 + 1, tr1 + 1))
    ws.merge_cells("D%d:O%d" % (tr1 + 1, tr1 + 1))
    ws.cell(tr1, 4).number_format = "0.00_ "
    ws.cell(tr1 + 1, 4).number_format = "0.0000_ "

    ws.print_area = "A1:O%d" % (tr1 + 1)
    wb.save(out_path)
    total = plan["allocation"]["total_days"]
    print("已生成工作量评估表：%s" % out_path)
    print("  功能行数 %d，阶段 %d 段，合计 %.2f 人天（%.4f 人月）"
          % (len(rows), len(STAGE_CN), total, total / wldlib.DAYS_PER_PM))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("out")
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--template", default=os.path.join(here, "assets", "workload_template.xlsx"))
    a = ap.parse_args()
    sys.exit(render(a.plan, a.out, a.template))


if __name__ == "__main__":
    main()
