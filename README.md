# 功能组工作量设计大佬 · workload-design-master

> WorkBuddy 技能（Skill）：输入一份**用户需求说明书** + 一个**人月数**，自动产出两份可直接提交的交付物——
> 《项目工作量评估表》`.xlsx` 与《详细设计说明书》`.docx`，并保证三处口径严格对齐。

[English summary](#english-summary) · 详细中文手册见 [`使用说明.md`](./使用说明.md) · 技能主文件见 [`SKILL.md`](./SKILL.md)

---

## 这个技能解决什么问题

在银行科技侧项目中，把"需求文档"翻译成"工作量评估表"和"详细设计说明书"是高频、强模板约束的重复劳动。本技能将这套经验沉淀为可复用的规则与脚本：

- **人天一律由脚本计算**，杜绝手改数字导致总计与人月对不上。
- **模块数量 / 名称在三处逐字一致**：需求文档业务功能条目 = Excel 系统模块列 = Word 第七章小标题。
- **内置真实数据库表结构字典**：抽取自《AML_6.0 数据库表结构文档》（10 章节 / 822 个对象 / 9694 个字段），设计文档优先引用真实表、保留原名大写。
- **模板纪律不可协商**：Excel 只改一个工作表，Word 只生成第七章，不臆造模板外章节。

## 两份交付物

| 交付物 | 内容 |
| --- | --- |
| 《项目工作量评估表》`.xlsx` | 8 个阶段（需求／设计／开发／技术测试／性能测试／业务测试／准生产／上线支持）+ 逐功能行人天；保留模板四页工作表、合并规则与合计公式（`=总计/21.75`）。 |
| 《详细设计说明书》`.docx` | 严格按基础模板：封面 + 修改记录 + 目录 + **七、模块设计（功能设计细化）**，逐模块 7 段（需求描述、操作界面、模块流程、关联模块、设计说明、引用的数据库表、测试要点）。 |

## 核心估算规则

| 规则 | 取值 |
| --- | --- |
| 人月换算 | 1 人月 = **21.75** 人天（与模板公式绑定） |
| 阶段占比 | 需求 5.2% · 设计 10.7% · 开发 39.0% · 技术测试 29.1% · 业务测试 10.7% · 准生产 5.4%（占扣除固定段后的剩余量） |
| 性能测试 | 全表 1 行，1–3 人天（<150 人天取 1.0，<350 取 2.0，其余 3.0） |
| 上线支持 | 全表 1 行，**固定 1 人天** |
| 功能行数 | 开发总人天 ÷ 7.5（例：7.5 人月 → 开发 60 人天 → 8 行） |
| 开发单条 | 3.5–9.5 人天，步长 0.5，硬上限 10，均值≈7.5 |

> 比例、区间、行数规律来自 4 份已评估样例的反演，详见 [`references/estimation-rules.md`](./references/estimation-rules.md)。

## 目录结构

```
workload-design-master/
├── SKILL.md                 技能主文件（触发条件与工作流）
├── 使用说明.md               中文详细手册
├── README.md                本文件
├── references/
│   ├── estimation-rules.md  人天比例、区间、行数规律
│   ├── excel-spec.md        Excel 列结构、合并规则、8 类文案范式
│   ├── design-doc-spec.md   Word 章节与模块 7 段写法
│   └── aml-table-index.md   真实表索引（按章节分组，生成物勿改）
├── scripts/
│   ├── wldlib.py            分配算法、规则校验、库用户推断
│   ├── plan.py              init / fill / check / show 四个子命令
│   ├── render_xlsx.py       渲染工作量评估表
│   ├── render_docx.py       渲染详细设计说明书
│   ├── doc_read.py          读取 .doc/.docx 并抽取业务功能条目
│   ├── aml_tables.py        查询真实表结构（modules/list/search/show/pick）
│   └── build_aml_dict.py    从表结构文档重建字典
└── assets/
    ├── workload_template.xlsx   Excel 底版（勿改）
    ├── aml_tables.json          真实表结构字典（生成物勿改）
    └── example_plan.json        完整填充范例（7.5 人月 / 6 模块 / 8 行）
```

## 安装（作为 WorkBuddy 技能使用）

将本仓库整体复制到 WorkBuddy 的技能目录即可被自动识别：

```bash
# Windows（PowerShell）
Copy-Item -Recurse workload-design-master "C:\Users\<你的用户名>\.workbuddy\skills\"

# 或 macOS / Linux
cp -r workload-design-master ~/.workbuddy/skills/
```

技能标识为 `workload-design-master`，显示名「功能组工作量设计大佬」。

## 依赖

脚本为 Python 3，渲染与解析依赖以下库：

```bash
python -m pip install openpyxl python-docx olefile
```

- `openpyxl`：读写 `.xlsx` 模板与输出
- `python-docx`：生成 `.docx` 详细设计说明书
- `olefile`：识别并解析旧版 `.doc`（OLE2 二进制，含伪扩展名）

## 快速使用

### 1. 读取需求文档，抽取模块清单

```bash
python scripts/doc_read.py "<需求文档路径>" --modules
```

### 2. 初始化计划骨架（人天由脚本计算）

```bash
python scripts/plan.py init --pm 7.5 \
  --project "<项目名称>" --system "<系统名称>" \
  --modules "模块A:3,模块B:2,模块C:1" \
  --version V1.0 --date "2026年11月4日" \
  --out plan.json
```

`--system` 同时决定数据库用户：反洗钱管理系统2.0 → `ams`，反洗钱客户尽职调查管理系统 → `amd`。

### 3. 编辑 `plan.json` 填写文案

按 [`references/excel-spec.md`](./references/excel-spec.md) 与 [`references/design-doc-spec.md`](./references/design-doc-spec.md) 的范式填写每个模块的「需求 / 设计 / 开发 / 测试要点 / 引用的数据库表」等字段。选表优先用字典：

```bash
python scripts/aml_tables.py modules                 # 章节与对象数
python scripts/aml_tables.py list --module 05 --keyword 名单
python scripts/aml_tables.py show T5A_BLACK_LIST     # 字段明细
python scripts/aml_tables.py pick T5A_BLACK_LIST --user ams
```

### 4. 回填人天并校验（不通过不渲染）

```bash
python scripts/plan.py fill  plan.json
python scripts/plan.py check plan.json
```

### 5. 渲染两份交付物

```bash
python scripts/render_xlsx.py plan.json "<输出目录>/<项目简称>_工作量评估表_V1.0.xlsx"
python scripts/render_docx.py plan.json "<输出目录>/<项目简称>详细设计说明书_V1.0.docx"
```

> 打开 Word 后按 **F9** 更新目录生成实际页码。

## 硬约束（每次交付前自查）

1. 模块数 = 需求文档业务功能条目数，名称逐字一致。
2. Excel 每个模块在系统模块列成段合并；Word 每个模块一个小标题。
3. 开发单条 3.5–9.5 人天，硬上限 10，均值≈7.5，步长 0.5。
4. 需求 / 设计 / 开发每行 6–10 条编号；最小单位 0.5 人天。
5. Word 每模块严格 7 段，且只含模板既有内容（封面／修改记录／目录／七），不新增章节。
6. 需求描述 / 模块流程 / 设计说明各约 150 字（不少于 100 字）。
7. 1 人月 = 21.75 人天，总计人月与输入一致（±0.15）。
8. 数据库用户与系统名称绑定；引用的表优先取自真实字典，不虚构字段。

完整约束清单见 [`SKILL.md`](./SKILL.md) 的「硬约束清单」。

## 许可

本仓库以 **MIT License** 发布，可自由使用、修改与再分发。详见 [`LICENSE`](./LICENSE)（若存在）。

---

## English Summary

**workload-design-master** is a [WorkBuddy](https://www.workbuddy.cn) Skill that turns a requirements document plus a person-month figure into two submission-ready deliverables:

- **`项目工作量评估表.xlsx`** — an 8-stage, per-function effort breakdown with locked template formulas (`total / 21.75`).
- **`详细设计说明书.docx`** — a design spec following a fixed template (cover, revision log, TOC, and Chapter 7 module design with 7 subsections per module).

Key guarantees: module counts/names are byte-identical across the requirements doc, the Excel "system module" column, and the Word Chapter 7 headings; all person-day numbers are computed by script (never hand-edited); an embedded real database schema dictionary (822 objects / 9694 fields from the AML 6.0 spec) is used so design docs reference real tables.

To install, copy this folder into `~/.workbuddy/skills/`. Python dependencies: `openpyxl`, `python-docx`, `olefile`.
