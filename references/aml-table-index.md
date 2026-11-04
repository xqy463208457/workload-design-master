# 反洗钱系统真实表结构索引

> 来源：`AML_6.0数据库表结构文档.docx`（由 `scripts/build_aml_dict.py` 自动生成，勿手改）。
> 用途：写详细设计「引用的数据库表」时，优先在此选取真实表；
> 需要字段明细时执行 `python scripts/aml_tables.py show <表名>`，不要整份读入 JSON。

## 01 系统管理

### 表的清单

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T18_BACKSERVER | T18_后台服务配置 | 11 |
| T18_BACKSERVER_LOG | T18_后台服务操作日志 | 6 |
| T18_DATASOURCE | T18_商业银行可能需要从多个系统取数据 | 24 |
| T18_DEPENDENT | T18_依赖关系 | 4 |
| T18_DM_TABLE | T18_审计数据表管理DM | 13 |
| T18_DS_LOG | T18_各类标识方式表 | 3 |
| T18_DS_S58_FLAG | T18_ | 3 |
| T18_ERROR_LOG | T18_后台错误日志 | 7 |
| T18_FLAGFILE | T18_文件名规则 | 5 |
| T18_FLAGTABLE | T18_外部数据源准备完毕后通知系统可以装载的标识 | 5 |
| T18_FLAGTABLE_COLS | T18_对标识表的各个字段进行定义 | 14 |
| T18_JOB_COMPUTE_LOG | T18_定时作业计算情况日志表 | 11 |
| T18_JOB_FLOW | T18_作业流 | 12 |
| T18_JOB_INSTANCE | T18_作业实例 | 28 |
| T18_JOB_MODEL | T18_作业模型 | 22 |
| T18_JOB_TYPE | T18_作业类型 | 8 |
| T18_MUTEX_LOCK | T18_互斥锁 | 10 |
| T18_ODS2DMETL | T18_ODS2DM ETL脚本 | 11 |
| T18_ODS_DBLINK | T18_DBLINK 方式，表对表抽取数据 | 13 |
| T18_ODS_FETCH | T18_JDBC 、 客户端 | 16 |
| T18_ODS_FTP | T18_数据抽取(FTP) | 10 |
| T18_ODS_LOAD | T18_源业务数据装载脚本 | 13 |
| T18_ODS_TABLE | T18_业务数据源管理表 | 9 |
| T18_ONLINE_JOB | T18_即时作业实例 | 18 |
| T18_ONLINE_TYPE | T18_即时作业类型 | 11 |
| T18_PROJECT | T18_工程 | 8 |
| T18_REGULAR_INSTANTIATION_LOG | T18_每日定时作业实例生成情况表 | 5 |
| T1A_ATTN_AREA | T1A_关注地区 | 9 |
| T1A_CITY_AREA | T1A_城市与地区映射 | 9 |
| T1A_IP_CITY_MAP | T1A_IP与城市映射 | 12 |
| T1A_TAB_MAINTAIN | T1A_表维护配置 | 12 |
| T1A_WF_MOVE | T1A_案例节点流向定义表 | 12 |
| T1A_WF_NODE | T1A_案例节点定义表 | 9 |
| T1A_WORKDAY | T1A_工作日配置表 | 8 |
| T1B_NOTICE | T1B_信息公告 | 11 |
| T1B_NOTICE_ATHT | T1B_信息公告附件 | 7 |
| T1B_ORG_MAP | T1B_机构映射 | 4 |
| T1B_PROC_LOG | T1B_存储过程日志 | 7 |
| T1B_RPT_ORG | T1B_数据报送机构 | 8 |
| T1B_RPT_ORG_MAP | T1B_数据报送机构映射 | 2 |
| T1B_RPT_SEQ | T1B_数据报送序列表 | 4 |
| T1B_SUP | T1B_工作督办 | 9 |
| T1E_CURR_MAP | T1E_币种映射 | 8 |
| T1E_EBANK_CTL_IP | T1E_网银IP控制表 | 9 |
| T1E_ETL_MAP | T1E_ETL映射 | 11 |
| T1E_UNION_ORG | T1E_支付系统行号 | 17 |
| T1P_AREA | T1P_地区代码 | 10 |
| T1P_CERT_TYPE | T1P_证件类型表 | 4 |
| T1P_COUNTRY | T1P_国家代码 | 11 |
| T1P_CURRENCY | T1P_币种代码 | 8 |
| T1P_MODULE_TYPE | T1P_首页统计菜单类型关系表 | 9 |
| T1P_ORGAN_MAP | T1P_机构对应关系表 | 6 |
| T1P_OTHER | T1P_其他代码 | 10 |
| T1P_PBC_CTVC | T1P_对公对私职业行业 | 5 |
| T1P_PBC_TCR | T1P_PBC特征代码 | 8 |
| T1P_RATE | T1P_汇率表 | 10 |
| T1P_SUBJECT | T1P_科目维护表 | 8 |
| T1P_TEMPLATE_MODULE_SKIP | T1P_首页统计模板菜单跳转关系表 | 9 |
| T1P_TR_CD | T1P_交易代码维护表 | 7 |
| T1P_TSCT | T1P_涉外收支交易代码 | 9 |
| T1P_TSTP | T1P_交易方式 | 10 |
| T1B_RISK_EVENT | T1B_客户风险事件表 | 0 |
| T1P_ELEMENT | T1P_报文标签表 | 0 |
| T1P_ELEMENT_3 | T1P_报文标签表三号令 | 0 |

## 02 基础业务

### 表的清单

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T2A_ACCT_ACCTID_MID | T2A_账户号中间表 | 1 |
| T2A_ACCT_LIMIT | T2A_外汇账户额度控制表 | 7 |
| T2A_ACCT_MID | T2A_账户中间表 | 2 |
| T2A_CARD_CREDIT | T2A_贷记卡信息 | 17 |
| T2A_CARD_CREDIT_HX | T2A_贷记卡信息 | 21 |
| T2A_CARD_DEBIT | T2A_借记卡信息 | 21 |
| T2A_CREDIT_BILL_HX | t2a_信用卡账单 | 65 |
| T2A_CREDIT_CARD_ACCT_RELA_HX | t2a_信用卡账户关系 | 4 |
| T2A_CUST_BG | 证件变更客户表 | 17 |
| T2A_CUST_C | T2A_对公客户信息 | 71 |
| T2A_CUST_CERT | T2A_客户证件信息 | 5 |
| T2A_CUST_CLCT_LOG | T2A_补录日志-客户信息 | 8 |
| T2A_CUST_DCI_MID | 计算新开户，过期户中间表 | 6 |
| T2A_CUST_HOLD | T2A_对公客户股东信息 | 9 |
| T2A_CUST_I | T2A_对私客户信息 | 50 |
| T2A_CUST_LINK | T2A_客户信息关联表 | 3 |
| T2A_CUST_MID | T2A_客户中间表 | 2 |
| T2A_DPST_ACCT_C | T2A_对公存款账户 | 35 |
| T2A_DPST_ACCT_I | T2A_对私存款账户 | 33 |
| T2A_LOAN_ACCT | T2A_贷款账户 | 37 |
| T2A_TRANS | T2A_交易流水表 | 87 |
| T2A_TRANS_CLCT_LOG | T2A_补录日志-交易信息 | 11 |
| T2A_TRANS_LMP | T2A_名单回溯交易流水表 | 83 |
| T2A_TRANS_MID | - | 5 |
| T2A_TRANS_MID_MID | - | 87 |
| T2A_TRANS_OPP_INFO | T2A_交易对手信息 | 19 |
| T2A_TRANS_PRE | T2A_交易流水表（筛查前） | 83 |
| T2A_TRANS_RISK | T2A_当日流水 | 83 |
| T2A_TRANS_SYNC_MID | - | 5 |
| T2A_TRANS_TRID_MID | T2A_交易业务标识号中间表 | 1 |
| T2A_VALIDATE_JOB_LOG | T2A_校验任务日志表 | 9 |
| T2C_RELA_BIC | - | 56 |
| T2D_EBANK_C | T2D_企业网银签约表 | 18 |
| T2D_EBANK_CTL | T2D_企业网银额度控制表 | 11 |
| T2D_EBANK_EVT | T2D_网银事件表 | 19 |
| T2D_EBANK_I | T2D_个人电子渠道签约表 | 23 |
| T2D_EBANK_OPR | T2D_企业网银操作员表 | 15 |
| T2D_MERCH | T2D_商户信息表 | 19 |
| T2D_MERCH_POS | T2D_商户设备信息表 | 10 |
| T2E_ACPT_BILL | T2E_银行承兑汇票表 | 26 |
| T2E_DISCT | T2E_贴现登记簿 | 43 |
| T2E_GUAR_RELA | T2E_信贷保证关系表 | 15 |
| T2F_OPR_INFO | T2F_柜员信息表 | 13 |
| T2F_OPR_LIMIT | T2F_柜员币种限额表 | 6 |
| T2F_STAFF | T2F_员工信息表 | 17 |

### 计算衍生数据

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T2A_CASE_ACCT_CUR | T2A_案例当前账户信息表 | 21 |
| T2A_CASE_ACCT_CUR_MID | T2A_案例当前账户信息中间表 | 21 |
| T2A_CASE_ACCT_CUR_VLD | T2A_案例当前账户信息表验证 | 16 |
| T2A_CASE_CUST_CERT | T2A_案例客户证件信息 | 5 |
| T2A_CASE_CUST_CUR | T2A_案例当前客户信息表 | 36 |
| T2A_CASE_CUST_CUR_MID | T2A_案例当前客户信息中间表 | 37 |
| T2A_CASE_CUST_CUR_MID2 | T2A_案例当前客户信息中间表2 | 1 |
| T2A_CASE_CUST_CUR_MID3 | T2A_案例当前客户信息中间表3 | 2 |
| T2A_CASE_CUST_CUR_VLD | T2A_案例当前客户信息表验证 | 33 |
| T2A_CASE_CUST_LINK | T2A_案例当前客户信息关联表 | 3 |
| T2A_CASE_TRANS_CUR | T2A_案例当前交易流水表 | 86 |
| T2A_CASE_TRANS_CUR_MID | T2A_案例当前交易流水表中间表 | 86 |
| T2A_CASE_TRANS_CUR_MID2 | T2A_案例当前交易流水表中间表2 | 2 |
| T2A_CASE_TRANS_CUR_MID3 | T2A_案例当前交易流水表中间表3 | 2 |
| T2A_CASE_TRANS_CUR_VLD | T2A_案例当前交易流水表验证 | 83 |
| T2A_CASE_TRANS_HST | T2A_案例历史交易流水表 | 86 |
| T2A_CASE_CUST_CERT_MID | T2A_案例客户证件信息中间表 | 0 |
| T2A_CASE_CUST_LINK_MID | T2A_案例当前客户信息关联表中间表 | 0 |
| T2A_CASE_TRANSACTION_MID | - | 0 |
| T2A_CASE_TRANS_HST_VLD | T2A_案例历史交易流水表验证 | 0 |

## 03 数据报送

### 表的清单

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T3A_ATIF_N | T3A_大额新增报告账户信息 | 12 |
| T3A_ATIF_N_HST | T3A_大额新增报告账户信息历史表 | 12 |
| T3A_CASE | T3A_大额案例表 | 26 |
| T3A_CASE_CUST | T3A_大额案例客户关系表 | 7 |
| T3A_CASE_CUST_HST | T3A_大额历史案例客户关系表 | 7 |
| T3A_CASE_HST | T3A_大额历史案例表 | 26 |
| T3A_CASE_TRANS | T3A_大额案例交易关系表 | 11 |
| T3A_CASE_TRANS_HST | T3A_大额历史案例交易关系表 | 11 |
| T3A_CASE_VALID | 案例验证表 | 7 |
| T3A_CASE_WF_LOG | T3A_大额案例审查日志 | 17 |
| T3A_CASE_WF_LOG_HST | T3A_大额历史案例审查日志 | 17 |
| T3A_CBH_RBIF | T3A_大额纠错报告基本信息 | 7 |
| T3A_CBH_TSDT | T3A_大额纠错报告交易信息 | 41 |
| T3A_CBIF_LINK | 大额可疑报告客户信息关联表 | 5 |
| T3A_CBIF_N | 大额新增报告客户基本信息 | 22 |
| T3A_CBIF_N_HST | 大额新增报告客户基本信息历史 | 22 |
| T3A_DBH_DTDT | T3A_大额删除报告交易信息 | 7 |
| T3A_DBH_RBIF | T3A_大额删除报告基本信息 | 6 |
| T3A_DTDT_D | 大额删除报告交易信息 | 8 |
| T3A_FDCF | T3A_大额回执-错误 | 6 |
| T3A_FDCF_FCER | T3A_大额回执-错误明细 | 5 |
| T3A_FDCF_FCER_HST | T3A_大额历史回执-错误明细 | 5 |
| T3A_FDCF_HST | T3A_大额历史回执-错误 | 6 |
| T3A_FDCF_UMTK | T3A_大额错误回执-删除明细 | 6 |
| T3A_FDRC | T3A_大额回执-补正 | 5 |
| T3A_FDRC_FCRC | T3A_大额回执-补正清单 | 6 |
| T3A_FDRC_FCRC_HST | T3A_大额历史回执-补正清单 | 6 |
| T3A_FDRC_FCRC_RCIF | T3A_大额回执-补正明细 | 8 |
| T3A_FDRC_FCRC_RCIF_HST | T3A_大额历史回执-补正明细 | 8 |
| T3A_FDRC_HST | T3A_大额历史回执-补正 | 5 |
| T3A_HTCR_N | 大额新增报告特征信息 | 8 |
| T3A_IBH_TSDT | T3A_大额补正报告交易信息 | 50 |
| T3A_IBH_RBIF | T3A_大额补正报告基本信息 | 7 |
| T3A_MSG | T3A_大额报文 | 24 |
| T3A_MSG_HST | T3A_大额历史报文 | 23 |
| T3A_MVCR | T3A_大额更正通知 | 5 |
| T3A_MVCR_SPMT | T3A_信息补充通知表 | 6 |
| T3A_MVCR_TSDT | T3A_人工补正通知详情 | 6 |
| T3A_NBH_CTIF | T3A_大额报告客户信息 | 14 |
| T3A_NBH_CTIF_HST | T3A_大额历史报告客户信息 | 14 |
| T3A_NBH_HTCR | T3A_大额报告特征信息 | 8 |
| T3A_NBH_HTCR_HST | T3A_大额历史报告特征信息 | 8 |
| T3A_NBH_RBIF | T3A_大额报告基本信息 | 7 |
| T3A_NBH_RBIF_HST | T3A_大额历史报告基本信息 | 7 |
| T3A_NBH_TSDT | T3A_大额报告交易信息 | 49 |
| T3A_NBH_TSDT_HST | T3A_大额历史报告交易信息 | 49 |
| T3A_PACKET | T3A_大额数据包 | 16 |
| T3A_PACKET_HST | T3A_大额历史数据包 | 16 |
| T3A_RBIF_C | 大额修改报告基本信息 | 7 |
| T3A_RBIF_D | 大额删除报告基本信息 | 5 |
| T3A_RBIF_N | 大额新增报告基本信息 | 5 |
| T3A_RBIF_N_HST | 大额新增报告基本信息历史表 | 5 |
| T3A_RECEIPT | T3A_大额回执 | 11 |
| T3A_RECEIPT_HST | T3A_大额历史回执 | 11 |
| T3A_REPORT | T3A_大额报告 | 21 |
| T3A_REPORT_HST | T3A_大额历史报告 | 21 |
| T3A_REPT_TSDT | 大额可疑待更正字段详情 | 5 |
| T3A_RPT_CASE | T3A_大额报告案例关系表 | 6 |
| T3A_RPT_CASE_HST | T3A_大额历史报告案例关系表 | 6 |
| T3A_RPT_VALID | 特殊报告验证表 | 5 |
| T3A_TSDT_C | 大额修改报告交易信息 | 59 |
| T3A_TSDT_N | 大额新增报告交易信息 | 58 |
| T3A_TSDT_N_HST | 大额新增报告交易信息历史 | 58 |
| T3B_ATHT_N | T3B_可疑报告附件 | 7 |
| T3B_ATIF_N | 可疑新增报告账户信息 | 15 |
| T3B_ATIF_N_HST | 可疑新增报告账户信息 | 15 |
| T3B_CASE | T3B_可疑案例表 | 36 |
| T3B_CASE_ACCT | T3B_可疑案例账户关系表 | 6 |
| T3B_CASE_ACCT_HST | T3B_可疑历史案例账户关系表 | 5 |
| T3B_CASE_ACCT_HST_VLD | T3B_可疑历史案例账户关系表验证 | 5 |
| T3B_CASE_ACCT_VLD | T3B_可疑案例账户关系表验证 | 5 |
| T3B_CASE_APP_ASSIST | 案例协查统计表 | 6 |
| T3B_CASE_APP_SUSPICIOUS | 可疑案例审核统计表 | 7 |
| T3B_CASE_ASSIST | T3B_可疑案例协查表 | 11 |
| T3B_CASE_ASSIST_ATHT | T3B_可疑协查附件表 | 6 |
| T3B_CASE_ASSIST_HST | T3B_可疑历史案例协查表 | 11 |
| T3B_CASE_ASSIST_HST_VLD | T3B_可疑历史案例协查表验证 | 11 |
| T3B_CASE_ASSIST_VLD | T3B_可疑案例协查表验证 | 11 |
| T3B_CASE_ATHT | T3B_可疑案例附件表 | 7 |
| T3B_CASE_ATHT_HST | T3B_可疑历史案例附件表 | 7 |
| T3B_CASE_ATHT_HST_VLD | T3B_可疑历史案例附件表验证 | 7 |
| T3B_CASE_ATHT_VLD | T3B_可疑案例附件表验证 | 7 |
| T3B_CASE_CUST | T3B_可疑案例客户关系表 | 14 |
| T3B_CASE_CUST_HST | T3B_可疑历史案例客户关系表 | 14 |
| T3B_CASE_CUST_VLD | T3B_可疑案例客户关系表验证 | 14 |
| T3B_CASE_DEL_LOG | T3B_可疑案例排除日志 | 8 |
| T3B_CASE_FETR | T3B_可疑案例特征关系表 | 14 |
| T3B_CASE_FETR_HST | T3B_可疑历史案例特征关系表 | 14 |
| T3B_CASE_FETR_HST_VLD | T3B_可疑历史案例特征关系表验证 | 14 |
| T3B_CASE_FETR_VLD | T3B_可疑案例特征关系表验证 | 14 |
| T3B_CASE_FOLLOW | T3B_子接续案例表 | 36 |
| T3B_CASE_HST | T3B_可疑历史案例表 | 37 |
| T3B_CASE_HST_VLD | T3B_可疑历史案例表验证 | 30 |
| T3B_CASE_MERGE | T3B_可疑案例表 | 37 |
| T3B_CASE_MERGE_ACCT | T3B_可疑案例账户关系表 | 7 |
| T3B_CASE_MERGE_CUST | T3B_可疑案例客户关系表 | 15 |
| T3B_CASE_MERGE_FETR | T3B_可疑案例特征关系表 | 15 |
| T3B_CASE_MERGE_MODEL | T3B_可疑案例模型表 | 12 |
| T3B_CASE_MERGE_STAT | T3B_可疑案例数据统计表 | 20 |
| T3B_CASE_MERGE_TIPS | T3B_可疑案例提示信息 | 6 |
| T3B_CASE_MERGE_TRANS | T3B_可疑案例交易关系表 | 13 |
| T3B_CASE_MODEL | T3B_可疑案例模型表 | 11 |
| T3B_CASE_MODEL_HST | T3B_可疑历史案例模型表 | 10 |
| T3B_CASE_MODEL_HST_VLD | T3B_可疑历史案例模型表验证 | 10 |
| T3B_CASE_MODEL_VLD | T3B_可疑案例模型表验证 | 11 |
| T3B_CASE_RELATIVE | 案例关联表 | 2 |
| T3B_CASE_STAT | T3B_可疑案例数据统计表 | 19 |
| T3B_CASE_STAT_HST | T3B_可疑历史案例数据统计表 | 19 |
| T3B_CASE_STAT_HST_VLD | T3B_可疑历史案例数据统计表验证 | 19 |
| T3B_CASE_STAT_VLD | T3B_可疑案例数据统计表验证 | 19 |
| T3B_CASE_TIPS | T3B_可疑案例提示信息 | 5 |
| T3B_CASE_TIPS_HST | T3B_可疑历史案例提示信息 | 5 |
| T3B_CASE_TIPS_VLD | T3B_可疑案例提示信息验证 | 5 |
| T3B_CASE_TRANS | T3B_可疑案例交易关系表 | 12 |
| T3B_CASE_TRANS_HST | T3B_可疑历史案例交易关系表 | 12 |
| T3B_CASE_TRANS_HST_VLD | T3B_可疑历史案例交易关系表验证 | 11 |
| T3B_CASE_TRANS_OTHER | T3B_可疑案例交易过渡表 | 12 |
| T3B_CASE_TRANS_VLD | T3B_可疑案例交易关系表验证 | 11 |
| T3B_CASE_VALID | 案例验证表 | 7 |
| T3B_CASE_VLD | T3B_可疑甄别验证表 | 30 |
| T3B_CASE_WF_LOG | T3B_可疑案例甄别日志 | 17 |
| T3B_CASE_WF_LOG_HST | T3B_可疑历史案例甄别日志 | 17 |
| T3B_CHECKPARTY_NEW_STATISTICAL | 风险评级对新开客户完成统计 | 6 |
| T3B_FDCF | T3B_可疑回执-错误 | 4 |
| T3B_FDCF_FCER | T3B_可疑回执-错误明细 | 5 |
| T3B_FDCF_FCER_HST | T3B_可疑历史回执-错误明细 | 5 |
| T3B_FDCF_HST | T3B_可疑历史回执-错误 | 4 |
| T3B_FDRC | T3B_可疑回执-补正 | 4 |
| T3B_FDRC_FCRC | T3B_可疑回执-补正明细 | 7 |
| T3B_FDRC_FCRC_HST | T3B_可疑历史回执-补正明细 | 7 |
| T3B_FDRC_HST | T3B_可疑历史回执-补正 | 4 |
| T3B_MSG | T3B_可疑报文 | 24 |
| T3B_MSG_HST | T3B_可疑历史报文 | 23 |
| T3B_MVCR | T3B_可疑人工补正通知 | 6 |
| T3B_MVCR_REPT | T3B_可疑人工补正通知详情 | 4 |
| T3B_NBS_ATHT | T3B_可疑报告附件 | 7 |
| T3B_NBS_ATHT_HST | T3B_可疑历史报告附件 | 7 |
| T3B_NBS_ATIF | T3B_可疑报告账户信息 | 12 |
| T3B_NBS_ATIF_HST | T3B_可疑历史报告账户信息 | 12 |
| T3B_NBS_CTIF | T3B_可疑报告客户信息 | 23 |
| T3B_NBS_CTIF_HST | T3B_可疑历史报告客户信息 | 23 |
| T3B_NBS_RBIF | T3B_可疑报告基本信息 | 15 |
| T3B_NBS_RBIF_HST | T3B_可疑历史报告基本信息 | 15 |
| T3B_NBS_RPDI | T3B_可疑报告交易信息 | 43 |
| T3B_NBS_RPDI_HST | T3B_可疑历史报告交易信息 | 43 |
| T3B_NBS_SEIF | T3B_正常报告客户证件信息 | 21 |
| T3B_NBS_SIIF | - | 7 |
| T3B_PACKET | T3B_可疑数据包 | 16 |
| T3B_PACKET_HST | T3B_可疑历史数据包 | 16 |
| T3B_RBIF_N | 可疑新增报告基本信息 | 21 |
| T3B_RBIF_N_HST | 可疑新增报告基本信息历史 | 21 |
| T3B_RECEIPT | T3B_可疑回执 | 11 |
| T3B_RECEIPT_HST | T3B_可疑历史回执 | 11 |
| T3B_REPORT | T3B_可疑报告 | 21 |
| T3B_REPORT_HST | T3B_可疑历史报告 | 21 |
| T3B_RPT_CASE | T3B_可疑报告案例关系表 | 6 |
| T3B_RPT_CASE_HST | T3B_可疑历史报告案例关系表 | 6 |
| T3B_SCREENING_TEMPLATE | 甄别意见模板表 | 7 |
| T3B_SEIF_CERT | 可疑报告客户多个证件信息表 | 7 |
| T3B_SEIF_LINK | 大额可疑报告客户信息关联表 | 5 |
| T3B_SEIF_N | 可疑新增报告客户基本信息 | 29 |
| T3B_SEIF_N_HST | 可疑新增报告客户基本信息历史 | 29 |
| T3B_SESSION_CASE_VALID | 验证案例session表 | 5 |
| T3B_STIF_N | 可疑新增报告交易信息 | 56 |
| T3B_STIF_N_HST | 可疑新增报告交易信息历史表 | 56 |
| T3D_RULE_PARAM_VALUE_BK | - | 9 |
| T3D_VALIDATE_FIELD | 验证字段表 | 8 |
| T3D_VALIDATE_FIELD_FORM | - | 4 |
| T3D_VALIDATE_FIELD_RULE | 字段与验证器规则关系表 | 3 |
| T3D_VALIDATE_RULE | 校验规则定义表 | 9 |
| T3D_VALIDATE_RULE_PARAM | 规则参数表 | 9 |
| T3D_VALIDATE_RULE_PARAM_VALUE | 规则参数值表 | 9 |
| T3D_VALIDATE_STATIC | - | 2 |
| T3D_VALIDATE_TEMPLATE | 校验模板表 | 10 |
| T3B_CASE_CRIME_TYPE_TMP | 可疑案例涉罪类型中间表 | 0 |

### 包后台计算中间表

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T3A_RECEIPT_MID | T3A_大额回执中间表 | 6 |
| T3A_REPORT_MID | T3A_大额报告中间表 | 2 |
| T3A_CASE_MID | T3A_大额案例中间表 | 2 |
| T3B_RECEIPT_MID | T3B_可疑回执中间表 | 2 |
| T3B_REPORT_MID | T3B_可疑报告中间表 | 2 |
| T3B_CASE_MID | T3B_可疑案例中间表 | 2 |

## 04 风险评估

### 表的清单

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T1H_ELE_SCORE | 原T31_DEF_ELEMENT要素表 | 5 |
| T1H_FREETRADE_LVL_MAP | T1H_风险等级映射表 | 14 |
| T1H_MODEL_FOMULA_INDIC | T1H_公式指标表 | 7 |
| T1H_MODEL_FOMULA | T1H_公式表 | 15 |
| T1H_MODEL_OBJ | T1H_评级模型对象表 | 7 |
| T1H_NEXT_RISK_MONTH | T1H_评级下次评级间隔表 | 3 |
| T1H_RISK_ELE | T1H_评级风险子项表 | 15 |
| T1H_RISK_ELE_SCORE | T1H_风险子项区间分值对应表 | 6 |
| T1H_RISK_LVL_MAP | T1H_风险等级映射表 | 14 |
| T1H_RISK_MODEL | T1H_模板表 | 16 |
| T1M_OPERATE_WF_LOG | 操作记录日志 | 7 |
| T1M_PRD_ATHT | T1M_产品评估附件表 | 7 |
| T1M_PRD_WF_LOG | 产品评估记录表 | 10 |
| T1M_PRODUCT | 产品表 | 9 |
| T1M_PRODUCT_ELE | 产品评估风险子项表 | 12 |
| T1M_PRODUCT_RESULT | 产品评级结果 | 10 |
| T1M_RISK_ELE_SCORE | 评级分值表 | 7 |
| T1M_RISK_LVL_MAP | 评级分值映射表 | 12 |
| T4A_ATTR_CUST | 客户属性模板评级对象表 | 7 |
| T4A_BEFORE_RSLT_MID | 上次评级结果中间表-月粒度 | 24 |
| T4A_BEFORE_RSLT_MID1 | 上次评级结果中间表 | 24 |
| T4A_CUST_ACTIVE | 评级活跃用户 | 7 |
| T4A_CUST_ATTR_RSLT | T4A_客户属性类结果表 | 7 |
| T4A_CUST_ATTR_RSLT_HST | T4A_客户属性类结果历史表 | 7 |
| T4A_CUST_ELE_SCORE_MODI | T4A_客户要点分值重新计算表 | 11 |
| T4A_CUST_EXCP_RSLT | T4A_客户公式指标值表 | 7 |
| T4A_CUST_EXCP_RSLT_HST | T4A_客户公式指标值历史表 | 7 |
| T4A_CUST_EXCP_RSLT_MID | 非直接覆盖的公式指标值临时表 | 13 |
| T4A_CUST_EXCP_RSLT_MID1 | 直接覆盖的公式指标值临时表 | 13 |
| T4A_CUST_RE_ADJUST_LOG | T4A_客户重新调整日志记录 | 9 |
| T4A_CUST_RISK_WF_LOG | T4A_客户评级审查日志 | 18 |
| T4A_CUST_RISK_WF_LOG_HST | T4A_客户评级审查日志历史表 | 18 |
| T4A_CUST_RSLT | T4A_风险评级结果表 | 31 |
| T4A_CUST_RSLT_DEL_MID | 评级结果删除中间表 | 1 |
| T4A_CUST_RSLT_HST | T4A_风险评级结果历史表 | 31 |
| T4A_CUST_RSLT_MID | 月粒度评级结果中间表 | 18 |
| T4A_CUST_RSLT_MID1 | 日粒度评级结果中间表 | 18 |
| T4A_CUST_SCORE_RSLT | T4A_客户要点分值表 | 9 |
| T4A_CUST_SCORE_RSLT_HST | T4A_客户要点分值历史表 | 11 |
| T4A_CUST_SCORE_RSLT_MID | 客户子项分值中间表 | 9 |
| T4A_CUST_SCORE_RSLT_M_MID | 客户子项分值中间表-月粒度 | 9 |
| T4A_ELE_PCT_MID | 风险子项总权重中间表 | 4 |
| T4A_ELE_PCT_M_MID | 风险子项总权重中间表-月粒度 | 4 |
| T4A_FOMULA_COVER_RSLT_MID | 直接覆盖的公式指标值结果临时表 | 15 |
| T4A_FOMULA_RSLT_MID | 非直接覆盖的公式指标值结果临时表 | 15 |
| T4A_GRADE_RSLT_MID1 | 客户积分评级结果中间表 | 13 |
| T4A_GRADE_RSLT_MID2 | 积分客户最终评分等级结果中间表 | 13 |
| T4A_GRADE_RSLT_M_MID1 | 客户积分评级结果中间表-月粒度 | 13 |
| T4A_GRADE_RSLT_M_MID2 | 积分客户最终评分等级结果中间表-月粒度 | 13 |
| T4A_LAST_ELE_RSLT_MID | 最后一层风险子项分值中间表 | 11 |
| T4A_LAST_ELE_RSLT_M_MID | 最后一层风险子项分值中间表-月粒度 | 11 |
| T4A_LAST_ELE_SCORE_MID | 最后一层风险子项中间表 | 11 |
| T4A_LAST_ELE_SCORE_M_MID | 最后一层风险子项分值中间表-月粒度 | 11 |
| T4A_NEW_CUST | 新开客户公式模板评级对象表 | 7 |
| T4A_NEW_CUST_C | 新开对公客户评级对象表 | 7 |
| T4A_NEW_CUST_I | 新开对私客户评级对象表 | 7 |
| T4A_RISK_ASSIST | T4A_评级协查表 | 14 |
| T4A_RISK_ASSIST_ATHT | T4A_评级协查附件表 | 6 |
| T4A_RISK_ATHT | T4A_评级附件表 | 6 |
| T4A_RISK_LVL_STS | - | 7 |
| T4A_RISK_TAB_MID | 评级对象临时表 | 9 |
| T4A_RISK_TAB_M_MID | 月粒度积分评级对象临时表 | 9 |
| T4A_RISK_TAB_TOTAL_MID | 月粒度积分全量评级对象临时表 | 9 |
| T4A_STOCK_CUST | 存量客户公式模板评级对象表 | 7 |
| T4A_STOCK_CUST_ATTR | 存量客户属性类模板评级对象表 | 7 |
| T4A_STOCK_CUST_C | 存量客户对公积分模板评级对象表 | 7 |
| T4A_STOCK_CUST_I | 存量客户对私积分模板评级对象表 | 7 |
| T4A_TOP_ELE_RSLT_MID | 客户最终风险子项得分中间表 | 13 |
| T4A_TOP_ELE_RSLT_M_MID | 客户最终风险子项得分中间表-月粒度 | 13 |
| T4A_UP_ELE_RSLT_MID | 客户上层风险子项得分中间表 | 11 |
| T4A_UP_ELE_RSLT_M_MID | 客户上层风险子项得分中间表-月粒度 | 11 |
| T4A_UP_ELE_SCORE_MID | 上层风险子项分值中间表 | 13 |
| T4A_UP_ELE_SCORE_M_MID | 上层风险子项分值中间表-月粒度 | 13 |
| T4A_UP_ELE_SCORE_M_MID2 | - | 13 |

## 05 名单监控

### 表的清单

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T5A_BLACK_LIST | T5A_黑名单信息 | 21 |
| T5A_BLACK_LIST_LOG | T5A_黑名单信息操作日志表 | 12 |
| T5A_CT_LIST | T5A_反恐名单信息 | 21 |
| T5A_CT_LIST_LOG | T5A_反恐名单信息操作日志表 | 12 |
| T5A_GREY_LIST | T5A_灰名单信息 | 21 |
| T5A_GREY_LIST_LOG | T5A_灰名单信息操作日志表 | 12 |
| T5A_WHITE_LIST | T5A_白名单信息 | 23 |
| T5A_WHITE_LIST_LOG | T5A_白名单信息操作日志表 | 12 |
| T5C_COUNTRY | 原T87_PBC_COUNTRY | 12 |
| T5D_ADDRESS_DETAIL | T5D_道琼斯-黑名单人物/实体地址明细表 | 7 |
| T5D_ADDRESS_DETAIL_HST | T5D_道琼斯-历史-黑名单人物/实体地址明细表 | 7 |
| T5D_ASSOCIATION | T5D_道琼斯-黑名单关联方表 | 9 |
| T5D_ASSOCIATION_HST | T5D_道琼斯-历史-黑名单关联方表 | 8 |
| T5D_BIRTH_PLACE | T5D_道琼斯-黑名单出生地明细表 | 2 |
| T5D_CERT_DETAIL | T5D_道琼斯-黑名单证件明细 | 5 |
| T5D_CERT_DETAIL_HST | T5D_道琼斯-历史-黑名单证件明细 | 4 |
| T5D_COUNTRY | 原T87_PBC_COUNTRY | 12 |
| T5D_COUNTRY_DETAIL | T5D_道琼斯-黑名单个人/非船只实体国家明细 | 5 |
| T5D_COUNTRY_DETAIL_HST | T5D_道琼斯-历史-黑名单个人/非船只实体国家明细 | 4 |
| T5D_COUNTRY_PARM | T5D_道琼斯-参数-黑名单国家参数表 | 6 |
| T5D_DATE_DETAIL | T5D_道琼斯-黑名单日期明细表 | 7 |
| T5D_DATE_TYPE_PARM | T5D_道琼斯-参数-黑名单日期类型参数表 | 5 |
| T5D_DESC1_PARM | T5D_道琼斯-参数-黑名单描述1参数表 | 5 |
| T5D_DESC2_PARM | T5D_道琼斯-参数-黑名单描述2参数表 | 5 |
| T5D_DESC3_PARM | T5D_道琼斯-参数-黑名单描述3参数表 | 5 |
| T5D_DESC_DETAIL | T5D_道琼斯-历史-黑名单个人/实体描述明细表 | 8 |
| T5D_DESC_DETAIL_HST | T5D_道琼斯-历史-黑名单个人/实体描述明细表 | 7 |
| T5D_DOWJONS_DOWNLOAD | 道琼斯名单下载记录 | 4 |
| T5D_IMAGE_URL | T5D_道琼斯-黑名单图像URL信息 | 4 |
| T5D_NAME_DETAIL | T5D_道琼斯-黑名单名称明细表 | 13 |
| T5D_NAME_DETAIL_HST | T5D_道琼斯-历史-黑名单名称明细表 | 12 |
| T5D_NAME_TYPE_PARM | T5D_道琼斯-参数-黑名单名称类型参数表 | 5 |
| T5D_OCCUPATION_PARM | T5D_道琼斯-参数-黑名单职业参数表 | 4 |
| T5D_PROFILE_NOTE | T5D_道琼斯-黑名单附加信息 | 2 |
| T5D_RECORD_INDEX | T5D_道琼斯-黑名单主索引表 | 25 |
| T5D_RECORD_INDEX_HST | T5D_道琼斯-历史-黑名单主索引表 | 23 |
| T5D_RELATIONSHIP_PARM | T5D_道琼斯-参数-黑名单关系参数表 | 4 |
| T5D_ROLE_DETAIL | T5D_道琼斯-黑名单职业明细表 | 12 |
| T5D_ROLE_TYPE_PARM | T5D_道琼斯-参数-黑名单职业类型参数表 | 5 |
| T5D_SANCTIONER_LIST | T5D_道琼斯-黑名单制裁参考名单表 | 6 |
| T5D_SANWLRM_LIST | T5D_道琼斯-黑名单制裁类型参数表 | 14 |
| T5D_SAN_REF_DETAIL | T5D_道琼斯-黑名单参考制裁信息明细 | 9 |
| T5D_SOURCE_DETAIL | T5D_道琼斯-黑名单信息来源 | 2 |
| T5D_VESSEL_DETAIL | T5D_道琼斯-黑名单船只实体明细表 | 7 |
| T5E_ALIASNAME_DETAIL | T5E_路透-别名表 | 3 |
| T5E_ALL_INFO | - | 32 |
| T5E_ALTERNATIVE_SPELLING | T5E_路透-其他可能拼写方式表 | 2 |
| T5E_CATEGORY | - | 2 |
| T5E_CERT_DETAIL | T5E_路透-外部资源信息表 | 4 |
| T5E_CITIZENSHIPS_DETAIL | T5E_路透-归属国表 | 2 |
| T5E_DOBS_DETAIL | T5E_路透-出生日期表 | 2 |
| T5E_ES_MIDDLE | T5E_路透-引擎中间表 | 18 |
| T5E_FOREIGN_NAME_DETAIL | T5E_路透-中文名称表 | 3 |
| T5E_FURTHER_INFO | T5E_路透-制裁信息内容表 | 2 |
| T5E_IMAGE_URL | T5E_路透-外部资源信息表 | 2 |
| T5E_INFO_USEAREA | T5E_路透-信息使用地区表 | 4 |
| T5E_KEYWORDS_DETAIL | T5E_路透-制裁机构表 | 2 |
| T5E_LINK_PERSON | T5E_路透-相关人物表 | 2 |
| T5E_LIST_INDEX | - | 16 |
| T5E_LOW_QUALITY | T5E_路透-其他别名表 | 2 |
| T5E_NAME_LIST | - | 2 |
| T5E_ORG_DETAIL | T5E_路透-信息使用地区表 | 2 |
| T5E_PASSPORTS_INFO | T5E_路透-护照信息表 | 3 |
| T5E_RECORD_INDEX | T5E_路透-主索引表 | 17 |
| T5E_SUB_CATEGORY | T5E_子分类码表 | 2 |
| T5G_ACCUITY_IMPORT | ACCUITY黑名单数据装载日志表 | 7 |
| T5G_B_ENTITY_TYPELIST | ACCUITY黑名单实体类型码表 | 3 |
| T5G_B_SDFLIST | ACCUITY黑名单补充字段码表 | 3 |
| T5G_P_ADDRESS | - | 11 |
| T5G_P_ALIASES | 实体别称列表 | 5 |
| T5G_P_BIRTHPLACE | - | 3 |
| T5G_P_DOB | 实体出生日期列表 | 7 |
| T5G_P_ENTITY_LIST | - | 14 |
| T5G_P_ID | 实体ID列表 | 9 |
| T5G_P_NATIONALITY | 实体国籍列表 | 4 |
| T5G_P_NATIVECHARNAME | 实体名称LATIN列表 | 6 |
| T5G_P_OTHERIDS | - | 3 |
| T5G_P_PROGRAM | - | 4 |
| T5G_P_ROUTING | - | 4 |
| T5G_P_SDF | - | 4 |
| T5G_P_TITLE | - | 3 |
| T5G_TERROR | - | 10 |
| T5K_BATCH_CUST | T5K_客户批量开户 | 17 |
| T5K_BATCH_CUST_DETAIL | T5K_客户批量开户明细 | 16 |
| T5K_BATCH_CUST_DETAIL_HST | T5K_历史-客户批量开户明细 | 16 |
| T5K_BATCH_CUST_HST | T5K_历史-客户批量开户 | 17 |
| T5K_BATCH_CUST_RSLT | T5K_客户批量开户筛查明细 | 19 |
| T5K_BATCH_CUST_RSLT_HST | T5K_历史-客户批量开户筛查明细 | 17 |
| T5K_BLACK_LIST | T5K_黑名单信息 | 24 |
| T5K_BLACK_LIST_LOG | T5K_黑名单信息操作日志表 | 12 |
| T5K_CFG_DB_INDEX_PARM | T5K_配置-黑名单数据库索引配置表 | 12 |
| T5K_CFG_FILE_INDEX_PARM | T5K_配置-黑名单文件索引配置表 | 12 |
| T5K_CFG_IGNORE_PARM | T5K_配置-黑名单忽略配置表 | 9 |
| T5K_CFG_MACTH_LIST | T5K_配置-黑名单匹配类型关系表 | 4 |
| T5K_CFG_MACTH_NAME | T5K_配置_黑名单匹配类型中文对照表 | 3 |
| T5K_CFG_MACTH_PARM | T5K_配置-黑名单匹配类型配置表 | 10 |
| T5K_CFG_WEIGHT_PARM | T5K_配置-黑名单权重配置表 | 12 |
| T5K_CUST_ALERT | T5K_客户回溯预警表 | 23 |
| T5K_CUST_ALERT_DETIAL | T5K_客户回溯预警明细 | 22 |
| T5K_CUST_ALERT_DETIAL_HST | T5K_历史-客户回溯预警明细 | 19 |
| T5K_CUST_ALERT_HST | T5K_历史-客户回溯预警表 | 21 |
| T5K_CUST_ALERT_MONITOR | T5K_客户回溯监控统计表 | 16 |
| T5K_CUST_ALERT_WF_LOG | T5K_客户回溯预警处理日志 | 8 |
| T5K_CUST_ALERT_WF_LOG_HST | T5K_历史-客户回溯预警处理日志 | 8 |
| T5K_CUST_DETAIL | T5K_客户开户明细 | 21 |
| T5K_CUST_DETAIL_HST | T5K_历史-客户开户明细 | 20 |
| T5K_CUST_RSLT | T5K_客户开户筛查明细 | 18 |
| T5K_CUST_RSLT_HST | T5K_历史-客户开户筛查明细 | 16 |
| T5K_DATAFILE_DOWNLOAD | - | 4 |
| T5K_FILEDOWN_LOG | t5k_数据文件下载记录 | 4 |
| T5K_IMP_LOG | T5K_黑名单数据装载日志表 | 12 |
| T5K_LIST_INDEX | - | 13 |
| T5K_LIST_INDEX_TEST | - | 16 |
| T5K_READCUSTFILE_DISP | - | 3 |
| T5K_READSWIFTFILE | - | 7 |
| T5K_READSWIFTFILE_DISP | - | 3 |
| T5K_READSWIFTFILE_INFO | - | 8 |
| T5K_TRANS_ALERT | T5K_交易回溯预警表 | 29 |
| T5K_TRANS_ALERT_DETIAL | T5K_交易回溯预警明细 | 22 |
| T5K_TRANS_ALERT_DETIAL_HST | T5K_历史-交易回溯预警明细 | 19 |
| T5K_TRANS_ALERT_HST | T5K_历史-交易回溯预警表 | 27 |
| T5K_TRANS_ALERT_MONITOR | T5K_交易回溯监控统计表 | 16 |
| T5K_TRANS_ALERT_WF_LOG | T5K_交易回溯预警处理日志 | 8 |
| T5K_TRANS_ALERT_WF_LOG_DISP | - | 8 |
| T5K_TRANS_ALERT_WF_LOG_HST | T5K_历史-交易回溯预警处理日志 | 8 |
| T5K_TRANS_DETAIL | T5K_实时交易明细 | 13 |
| T5K_TRANS_DETAIL_HST | T5K_历史-实时交易明细 | 13 |
| T5K_TRANS_INFO | T5K_实时交易 | 12 |
| T5K_TRANS_INFO_HST | T5K_历史-实时交易 | 12 |
| T5K_TRANS_RSLT | T5K_实时交易筛查明细 | 16 |
| T5K_TRANS_RSLT_HST | T5K_历史-实时交易筛查明细 | 14 |
| T5K_TRANS_SWIFT | T5K_实时汇入交易 | 16 |
| T5K_TRANS_SWIFT_HST | T5K_历史-实时汇入交易 | 16 |
| T5K_TRANS_SWIFT_RSLT | T5K_实时汇入交易筛查明细 | 15 |
| T5K_WHITE_LIST | T5K_白名单信息 | 23 |
| T5K_WHITE_LIST_LOG | T5K_白名单信息操作日志表 | 12 |
| T5D_BIRTH_PLACE_HST | T5D_道琼斯-历史-黑名单出生地明细表 | 0 |
| T5D_COUNTRY_PARM_HST | T5D_道琼斯-参数-历史-黑名单国家参数表 | 0 |
| T5D_DATE_DETAIL_HST | T5D_道琼斯-历史-黑名单日期明细表 | 0 |
| T5D_DATE_TYPE_PARM_HST | T5D_道琼斯-参数-历史-黑名单日期类型参数表 | 0 |
| T5D_DESC1_PARM_HST | T5D_道琼斯-参数-历史-黑名单描述1参数表 | 0 |
| T5D_DESC2_PARM_HST | T5D_道琼斯-参数-历史-黑名单描述2参数表 | 0 |
| T5D_DESC3_PARM_HST | T5D_道琼斯-参数-历史-黑名单描述3参数表 | 0 |
| T5D_IMAGE_URL_HST | T5D_道琼斯-历史-黑名单图像URL信息 | 0 |
| T5D_NAME_DETAIL_TEST | - | 0 |
| T5D_NAME_TYPE_PARM_HST | T5D_道琼斯-参数-历史-黑名单名称类型参数表 | 0 |
| T5D_OCCUPATION_PARM_HST | T5D_道琼斯-参数-历史-黑名单职业参数表 | 0 |
| T5D_PROFILE_NOTE_HST | T5D_道琼斯-历史-黑名单附加信息 | 0 |
| T5D_RELATIONSHIP_PARM_HST | T5D_道琼斯-参数-历史-黑名单关系参数表 | 0 |
| T5D_ROLE_DETAIL_HST | T5D_道琼斯-历史-黑名单职业明细表 | 0 |
| T5D_ROLE_TYPE_PARM_HST | T5D_道琼斯-参数-历史-黑名单职业类型参数表 | 0 |
| T5D_SANCTIONER_LIST_HST | T5D_道琼斯-历史-黑名单制裁参考名单表 | 0 |
| T5D_SAN_REF_DETAIL_HST | T5D_道琼斯-历史-黑名单参考制裁信息明细 | 0 |
| T5D_SOURCE_DETAIL_HST | T5D_道琼斯-历史-黑名单信息来源 | 0 |
| T5D_VESSEL_DETAIL_HST | T5D_道琼斯-历史-黑名单船只实体明细表 | 0 |

### 视图的清单

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| V5K_LIST_INDEX | V5K_黑名单主索引视图 | 0 |

## 06 风险分析

### 表的清单

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T1B_RISK_EVENT | T1B_客户风险事件表 | 15 |
| T1B_DCI | T1B_尽职调查 | 14 |
| T1B_DCI_ATHT | T3B_可疑协查附件表 | 6 |
| T1B_DCI_IMPT | T1B_尽职调查（加强型） | 39 |
| T1B_DCI_IMPT_HOLD | T1B_尽职调查（加强型）-股东信息 | 9 |
| T1B_DCI_PEP | T1B_尽职调查（PEP） | 5 |
| T3B_SUSP_OBJ | T3B_可疑主体库 | 19 |
| T3B_SUSP_OBJ_LOG | T3B_可疑主体库操作日志表 | 11 |
| T3B_SUSP_OBJ_FETR | T3B_可疑主体库特征 | 9 |
| T3M_EXP_CHECK_DE | T3M_大额筛查检查 | 9 |
| T3M_EXP_CHECK_KY | T3M_可疑筛查检查 | 7 |
| T3M_EXP_DATA_OVERVIEW | T3M_数据概览 | 7 |
| T3M_EXP_DATA_OVERVIEW_TREE | - | 6 |
| T3M_EXP_KEYTABLE | T3M_关键表数据监控 | 8 |
| T3M_EXP_QUALITY | T3M_数据质量核查 | 6 |

## 07 统计报表

### 表的清单

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T3E_CASE_APP_ASSIST | 案例协查统计表 | 6 |
| T3E_CASE_APP_SUSPICIOUS | 可疑案例审核统计表 | 7 |
| T3E_CASE_NB_NS | - | 12 |
| T3E_CHECKPARTY_NEW_STATISTICAL | 风险评级对新开客户完成统计 | 7 |
| T3E_HOMEPAGE_STATISTICS | T3E_首页统计信息表 | 7 |
| T3E_HOMEPAGE_STATISTICS_MID | T3E_首页统计信息中间表 | 7 |
| T3E_HOMEPAGE_STATISTICS_MID2 | T3E_首页统计信息中间表 | 7 |
| T3F_ADM | T3F_报告机构配合反洗钱行政调查情况表 | 16 |
| T3F_ADV | T3F_报告机构反洗钱宣传情况表 | 20 |
| T3F_ASSIST_BS_STAT | T3F_可疑协查统计表 | 6 |
| T3F_ASSIST_BS_STAT_MID | T3F_可疑协查统计中间表 | 6 |
| T3F_AUDIT | T3F_报告机构反洗钱内部检查（审计）情况表 | 18 |
| T3F_BS_REPORT | T3F_可疑交易报告统计表 | 8 |
| T3F_CASE_ASSIST_CHK | T3F_案例协查考核表 | 7 |
| T3F_CASE_ASSIST_CHK_MID | T3F_案例协查考核表中间表 | 7 |
| T3F_CASE_BS_CHK | T3F_可疑甄别考核表 | 7 |
| T3F_CASE_BS_CHK_MID | T3F_可疑甄别考核表中间表 | 7 |
| T3F_CASE_BS_FR_STAT | T3F_可疑案例频繁客户统计表 | 7 |
| T3F_CASE_BS_FR_STAT_MID | T3F_可疑案例频繁客户统计中间表 | 7 |
| T3F_CASE_BS_STAT | T3F_可疑案例统计表 | 12 |
| T3F_CASE_BS_STAT_MID | T3F_可疑案例统计表中间表 | 12 |
| T3F_CUST_CERT_EXPIRE_STAT | T3F_客户证件到期统计表 | 13 |
| T3F_CUST_CERT_EXPIRE_STAT_MID | T3F_客户证件到期统计中间表 | 13 |
| T3F_CUST_CLCT_STAT | T3F_客户补录统计表 | 6 |
| T3F_CUST_CLCT_STAT_MID | T3F_客户补录统计中间表 | 6 |
| T3F_DCI_STAT | T3F_客户尽职调查统计表 | 12 |
| T3F_DCI_STAT_MID | T3F_客户尽职调查统计中间表 | 12 |
| T3F_FI | T3F_境外机构反洗钱工作统计表 | 23 |
| T3F_FIELD | T3F_报告机构接受人民银行反洗钱现场检查情况表 | 21 |
| T3F_INNER | T3F_报告机构基本情况表 | 20 |
| T3F_INREP_BS | T3F_年度统计报表 | 9 |
| T3F_INREP_BS_MID | T3F_年度统计报表 | 9 |
| T3F_INREP_BS_PARA | T3F_代码对照表 | 5 |
| T3F_KYC | T3F_报告机构客户身份识别及风险等级分类情况表 | 48 |
| T3F_KYC_MID | 报告机构客户身份识别及风险等级分类情况表 | 48 |
| T3F_KYC_MID2 | - | 2 |
| T3F_KYC_LOG | 报告机构客户身份识别及风险等级分类情况表 | 49 |
| T3F_NEW_CUST_RISK_CHK | T3F_新开客户风险评级考核表 | 7 |
| T3F_NEW_CUST_RISK_CHK_MID | T3F_新开客户风险评级考核表中间表 | 7 |
| T3F_NEW_CUST_RISK_STAT | T3F_新开客户风险评级统计表 | 12 |
| T3F_NEW_CUST_RISK_STAT_MID | T3F_新开客户风险评级统计表 | 12 |
| T3F_ORG | T3F_报告机构基本情况表 | 33 |
| T3F_ORG_SHAREHOLD | T3F_股权结构情况(前十股东) | 9 |
| T3F_PCOR | T3F_报告机构洗钱风险防控成果表 | 18 |
| T3F_POP | T3F_报告机构反洗钱岗位人员情况表 | 20 |
| T3F_POP_STAFF | T3F_本级机构反洗钱人员情况 | 15 |
| T3F_PRSV_CUST_RISK_STAT | T3F_存量客户风险评级统计表 | 12 |
| T3F_PRSV_CUST_RISK_STAT_MID | T3F_存量客户风险评级统计中间表 | 12 |
| T3F_RISK_D2U_STAT | T3F_风险评级高调低统计表 | 9 |
| T3F_RISK_D2U_STAT_MID | T3F_风险评级高调低统计中间表 | 9 |
| T3F_RISK_U2D_STAT | T3F_风险评级低调高统计表 | 9 |
| T3F_RISK_U2D_STAT_MID | T3F_风险评级低调高统计中间表 | 9 |
| T3F_RPT_Y_CHECKLOG | T3F_年报审核日志表 | 9 |
| T3F_TRAIN | T3F_报告机构反洗钱培训情况表 | 20 |
| T3F_TRANSBHBS | T3F_报告机构大额和可疑交易报告情况表 | 18 |
| T3F_TRANSBHBS_MID | T3F_报告机构大额和可疑交易报告情况表 | 18 |
| T3F_TRANSBHBS_D | - | 18 |
| T3F_TRANSBHBS_LOG | 报告机构大额和可疑交易报告情况表 | 18 |
| T3F_TRANS_CLCT_CHK | T3F_交易补录考核表 | 11 |
| T3F_TRANS_CLCT_CHK_MID | T3F_交易补录考核表中间表 | 11 |
| T3F_TRANS_CLCT_STAT | T3F_交易补录统计表 | 9 |
| T3F_TRANS_CLCT_STAT_MID | T3F_交易补录统计表中间表 | 9 |
| T3F_TRANS_CLCT_STAT_INFO | T2A_案例当前交易流水表 | 86 |
| T3V_ALERT_RATIOS | 预警率表 | 6 |
| T3V_ALERT_TRANS_RATIOS_MID | 预警率中间表 | 4 |
| T3V_CASE_DAYS | 每天可疑案例数表 | 4 |
| T3V_DEL_RATIOS | 排除率表 | 5 |
| T3V_FACUS_RATIOS | 集中率表 | 4 |
| T3V_REPORT_RATIOS | 报告率表 | 4 |
| T3V_TRANS_DAYS | 每天交易数量表 | 2 |
| T3V_TRANS_DAYS_MID | 每天交易数量表 | 2 |

## 08 模型实验室

### 表的清单

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T1D_AREA_PARM | T1D_地区国家参数 | 9 |
| T1D_AREA_PARM_TEMP | T1D_地区国家参数分类 | 3 |
| T1D_ATTN_AREA | T1D_地区名单表 | 4 |
| T1D_ENTITY | T1D_结果主体 | 15 |
| T1D_ENTITY_COPY | 原T03_OBJECT_COPYCONF | 3 |
| T1D_ENTITY_KIND | 原T03_ENTITY_KIND | 15 |
| T1D_ENTITY_TABLE | T1D_结果主体事实表 | 16 |
| T1D_FEATURE | T1D_特征定义表 | 16 |
| T1D_FETR_DEF_PARM | T1D_特征输入参数 | 10 |
| T1D_FETR_DEF_PARM_VAL | T1D_特征输入参数值 | 11 |
| T1D_FETR_FOMULA | T1D_特征指标公式 | 5 |
| T1D_FETR_FUNC | T1D_特征函数表 | 6 |
| T1D_FETR_INDIC | T1D_特征指标表 | 7 |
| T1D_FETR_ORG_PARM | T1D_特征机构参数 | 11 |
| T1D_FETR_ORG_PARM_VAL | T1D_特征机构参数值 | 9 |
| T1D_FETR_PARM | T1D_特征公共参数 | 12 |
| T1D_FETR_PARM_ORG_VAL | T1D_特征公共机构参数值 | 7 |
| T1D_FETR_RTET | T1D_特征结果主体关系 | 2 |
| T1D_FETR_SQL | T1D_特征手工SQL表 | 6 |
| T1D_INDIC | T1D_指标表 | 17 |
| T1D_INDIC_MAP | T1D_指标表映射 | 3 |
| T1D_INDIC_PARM | T1D_指标参数 | 12 |
| T1D_INDIC_SQL | T1D_指标表SQL | 3 |
| T1D_INDIC_TR_SQL | T1D_指标表交易SQL | 3 |
| T1D_NONET_TRANS | T1D_资金网络交易SQL维护表 | 5 |
| T1D_RTET_COPY_MAP | T1D_结果主体字段映射表 | 3 |
| T1D_SUB_FEATURE | T1D_特征定义子表 | 13 |
| T1F_SUSP_ACTN_CODE | T1F_可疑交易行为代码表 | 8 |
| T1F_SUSP_MODEL | T1F_可疑涉罪模型表 | 15 |
| T1F_SUSP_MODEL_COND | T1F_可疑模型触发条件 | 7 |
| T1F_SUSP_MODEL_FETR | T1F_可疑涉罪模型特征关系 | 7 |
| T1F_SUSP_MODEL_KEY_FETR | T1F-可疑涉罪模型关键主体特征表 | 7 |
| T1F_SUSP_MODEL_NO_FETR | T1F_模型未量化规则 | 6 |

## 09 运维管理

### 后台规则计算

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T3H_ALERT | T3H_预警表 | 15 |
| T3H_ALERT_ACCT | T3H_预警账户表 | 7 |
| T3H_ALERT_CASE | T3H_预警案例表 | 9 |
| T3H_ALERT_CASE_HST | T3H_预警案例历史表 | 9 |
| T3H_ALERT_CUST | T3H_预警客户表 | 6 |
| T3H_ALERT_CUST_D | - | 3 |
| T3H_ALERT_CUST_OBJ | - | 2 |
| T3H_ALERT_CUST_TEMP | - | 4 |
| T3H_ALERT_MERGE | T3H_预警合并表 | 12 |
| T3H_ALERT_PARTY | 原T3H_ALERT_PARTY | 5 |
| T3H_ALERT_SPLIT_MID | T3H_预警拆分临时表 | 4 |
| T3H_ALERT_TRANS | T3H_预警交易表 | 10 |
| T3H_ALERT_TRANS_MODEL | 原T27_ALERT_TRANS | 9 |
| T3H_ALERT_TRANS_TEMP | - | 2 |
| T3H_ALERT_TRAN_MID | T3H_预警交易中间表 | 12 |
| T3H_ALERT_TR_SP_MID | T3H_预警交易拆分临时表 | 12 |
| T3H_MID_ALERT_PARTY_TEMP | 原T27_MID_ALERT_PARTY_TEMP | 6 |
| T3H_MID_RULETRANS_MID | 原T27_MID_ALERT_PARTY_TEMP | 4 |
| T3H_MODEL_ALERT | - | 6 |
| T3H_MODEL_SCORE | - | 6 |
| T3K_ALERT_MID | T3K_预警临时中间表 | 12 |
| T3K_ALERT_TMP_HIS | T3K_预警主体临时历史表 | 8 |
| T3K_ALERT_TMP | T3K_预警主体临时表 | 8 |
| T3K_ALERT_FACT_RLTV_MID | T3K_预警事实临时表 | 11 |
| T3K_ALERT_FACT_RLTV_MID1 | T3K_预警事实临时表1 | 11 |
| T3K_ALERT_FACT_RLTV | T3K_预警事实表 | 7 |
| T3K_SEQUENCE | - | 3 |

### 后台资金网络计算

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T3X_TRANS_MID | T3X_网络交易中间表 | 3 |
| T3X_TRANS_NET_D | T3X_当日网络交易表 | 29 |
| T3X_TRANS_NET_D_MID | - | 29 |
| T3X_TRANS_NET_MODEL | T47_TRANSACTION_MFA_MODEL | 29 |
| T3X_TRANS_OPP_D | T3X_当日网络对手关系表 | 7 |
| T3X_NET_CUST_DAY | T3X_网络客户表 | 4 |
| T3X_NET_CUST_DAY_MID | T3X_网络客户中间表 | 6 |
| T3X_NET_DAY_MID | T3X_网络预警关系中间表 | 4 |
| T3X_NET_MERGE_MID | T3X_网络合并中间表 | 2 |
| T3X_NET_MID | T3X_网络中间表 | 2 |
| T3X_NET_MID1 | T3X_网络关系中间表1 | 2 |
| T3X_NET_MID2 | T3X_网络关系中间表2 | 6 |
| T3X_NET_MID3 | T3X_网络关系中间表3 | 1 |
| T3X_NET_MUTI_MID1 | T3X_网络多元关系中间表1 | 4 |
| T3X_NET_TRANS_DAY | T3X_网络交易表 | 31 |
| T3X_NET_TRANS_DAY_TEMP | T3X_网络交易中间表 | 31 |

### 后台计算模型预警计算

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T3H_SINGLE_SCORE_TEMP | T3H_单主体模型分数中间表 | 4 |
| T3H_SINGLE_ALERT_TEMP | T3H_单主体模型预警中间表 | 8 |
| T3H_ALERT_TRANS_SINGLE_TEMP | T3H_单主体预警交易中间表 | 14 |
| T3H_MULTI_SCORE_TEMP | T3H_多主体模型分数中间表 | 4 |
| T3H_MULTI_ALERT_TEMP1 | T3H_多主体模型预警中间表 | 7 |
| T3H_ALERT_TRANS_MULTI_TEMP | T3H_多主体预警交易中间表 | 15 |

### 后台计算案例计算

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T3A_CASE_MID2 | T3A_大额案例表中间表2 | 27 |
| T3A_CASE_MID3 | T3A_大额案例表中间表3 | 3 |
| T3A_CASE_MID4 | T3A_大额案例表中间表4 | 7 |
| T3A_CASE_TRANS_MID | T3A_大额交易表中间表 | 14 |
| T3B_CASE_CUST_MID | T3B_可疑案例客户关系中间表 | 15 |
| T3B_CASE_CUST_MID2 | T3B_可疑案例客户关系中间表2 | 14 |
| T3B_CASE_CUST_MID3 | T3B_可疑案例客户关系中间表3 | 15 |
| T3B_CASE_CUST_MID4 | T3B_可疑案例客户关系中间表4 | 2 |
| T3B_CASE_CRIME_TYPE_TMP | T3B_可疑案例涉罪类型中间表 | 2 |
| T3B_CASE_FETR_MID | T3B_可疑案例特征关系中间表 | 14 |
| T3B_CASE_FOLLOW_MID | - | 2 |
| T3B_CASE_MERGE_MID | - | 36 |
| T3B_CASE_MID2 | T3B_可疑案例中间表2 | 35 |
| T3B_CASE_MID3 | T3B_可疑案例中间表3 | 6 |
| T3B_CASE_MODEL_FOLLOW_MID | 已上报接续案例中间表 | 5 |
| T3B_CASE_MODEL_FOLLOW_MID2 | 未完成的模型、特征案例中间表 | 6 |
| T3B_CASE_MODEL_MID | T3B_可疑案例模型中间表 | 11 |
| T3B_CASE_MODEL_MID2 | T3B_可疑案例模型中间表2 | 11 |
| T3B_CASE_MODEL_MID3 | T3B_可疑案例模型中间表3 | 4 |
| T3B_CASE_MODEL_RELATICE_MID | - | 4 |
| T3B_CASE_MODEL_RELATIVE_MID | - | 4 |
| T3B_CASE_OPPCUST_MID | T3B_可疑案例对手客户中间表 | 4 |
| T3B_CASE_ORG_MID | - | 2 |
| T3B_CASE_RELATIVE_MID | - | 2 |
| T3B_CASE_STAT_MID | T3B_可疑案例数据统计中间表 | 19 |
| T3B_CASE_STAT_MID2 | T3B_可疑案例数据统计中间表2 | 3 |
| T3B_CASE_STAT_MID3 | T3B_可疑案例数据统计中间表3 | 3 |
| T3B_CASE_TIPS_MID | T3B_可疑案例提示中间表 | 5 |
| T3B_CASE_TIPS_MID2 | T3B_可疑案例提示中间表2 | 6 |
| T3B_CASE_TIPS_MID3 | T3B_可疑案例提示中间表3 | 6 |
| T3B_CASE_TIP_CUST_MID | T3B_可疑案例客户提示中间表 | 5 |
| T3B_CASE_TRANS_CUR_MID | T3B_可疑案例当前交易关系中间表 | 6 |
| T3B_CASE_TRANS_CUR_MID1 | T3B_可疑案例当前交易关系中间表1 | 6 |
| T3B_CASE_TRANS_MID | T3B_可疑案例交易关系中间表 | 14 |
| T3B_CASE_TRANS_MID2 | T3B_可疑案例交易关系中间表2 | 11 |
| T3B_CASE_TRANS_MID3 | T3B_可疑案例交易关系中间表3 | 11 |
| T3B_CASE_TRANS_MID4 | T3B_可疑案例交易关系中间表4 | 4 |
| T3B_CASE_VALID_MID | T3B_可疑案例验证中间表 | 5 |
| T3B_SUSP_OBJ_FETR_TEMP | T3B_可疑主体特征中间表 | 2 |
| T3B_SUSP_OBJ_MID | - | 3 |
| T3B_MULTI_CUST_TEMP | T3B_匹配主体客户中间表 | 4 |
| T3H_ALERT_MID1 | T3H_预警中间表1 | 16 |
| T3H_ALERT_MID2 | T3H_预警中间表2 | 15 |
| T3H_ALERT_MERGE_MID | T3H_预警合并中间表 | 5 |

## 10 系统参数

### 表清单

| 表英文名 | 中文名 | 字段数 |
|---|---|---|
| T00_ACTION | - | 12 |
| T00_ASYNDOWNLOAD | - | 7 |
| T00_CANCELABLE_SQL | - | 12 |
| T00_CATEGORY | - | 12 |
| T00_COM_AUTH | - | 6 |
| T00_CURRENCY | - | 17 |
| T00_DICT | - | 8 |
| T00_EXPWORDTEMP_MODULE | T00_word模块表 | 16 |
| T00_EXPWORDTEMP_SQL | T00_ word模块查询sql配置表 | 7 |
| T00_EXPWORD_TEMP | T00_ word模板表临时表 | 4 |
| T00_FAVORITES | - | 5 |
| T00_ICON_CONF | - | 8 |
| T00_INDEX_SYSCONFIG | - | 5 |
| T00_INDEX_SYSTEMPLATE | - | 9 |
| T00_INDEX_SYSTEMPLATE_CONF | - | 6 |
| T00_JCS_LOCATION | - | 16 |
| T00_JCS_SQL | - | 14 |
| T00_LOGIN_ONLINE | T00_用户登录信息表 | 6 |
| T00_MODULE | - | 15 |
| T00_MODULE_TEST | - | 15 |
| T00_NOTICE | - | 12 |
| T00_NOTICERECORGAN | T00_公告接收机构 | 2 |
| T00_ONLINE_LOG | - | 6 |
| T00_OPERATE_LOG | - | 18 |
| T00_ORGAN | - | 25 |
| T00_RESOURCE_CONF | T00_子系统资源定义表 | 8 |
| T00_ROLE | - | 11 |
| T00_ROLE_RESOURCE | - | 8 |
| T00_SEQUENCE | - | 10 |
| T00_SYSTEM | - | 13 |
| T00_SYSTEM_LOG | - | 14 |
| T00_SYSTEM_PARAM | - | 11 |
| T00_TREE | - | 17 |
| T00_USER | - | 31 |
| T00_USER_INDEXTEMPLATE | - | 6 |
| T01_ATTACHMENT | T01_附件表 | 9 |
| T01_ATTACHMENT_HIS | T01_附件历史表 | 8 |
| T01_ATTACHMENT_LOG | T01_附件日志表 | 6 |
| T01_ATTACH_MAP | T01_附件业务对应关系表 | 4 |
| T02_COND_SUB | T02_定义指定模版的跳转条件子表 | 8 |
| T02_JUMP_TP | T02_定义显示列模版跳转表 | 6 |
| T02_PAGE_IN_PARM | T02_定义指定模版的输入参数 | 14 |
| T02_PAGE_IN_PARM_CACHE | T02_参数类型缓存表 | 3 |
| T02_PARM_SUB | T02_定义指定模版的跳转参数 | 7 |
| T02_SYS_FUNC | T02_静态参数存储表 | 7 |
| T02_TP_BAS_INF | T02_定义模版的基本属性信息 | 15 |
| T02_TP_CUSTOM_URL | T02_模版自定义url | 2 |
| T02_TP_DISP_RST | T02_定义模版显示结果列 | 13 |
| T02_TP_EXEC_QRY_SEQ | T02_模版执行SQL表 | 3 |
| T00_ACTION, | T00_ACTION | 0 |
| T00_ASYNDOWNLOAD, | T00_异步下载文件 | 0 |
| T00_CANCELABLE_SQL, | T00_取消SQL管理 | 0 |
| T00_CATEGORY, | T00_系统码表 | 0 |
| T00_COM_AUTH, | T00_用户角色表 | 0 |
| T00_CURRENCY, | T00_币种表 | 0 |
| T00_DICT, | T00_数据字典表, | 0 |
| T00_FAVORITES, | T00_存储当前登录用户收藏的功能菜单 | 0 |
| T00_ICON_CONF, | T00_字体图标管理 | 0 |
| T00_INDEX_SYSCONFIG, | T00_首页系统模块配置 | 0 |
| T00_INDEX_SYSTEMPLATE, | T00_首页模板信息表 | 0 |
| T00_INDEX_SYSTEMPLATE_CONF, | T00_首页模板定制表 | 0 |
| T00_JCS_LOCATION, | T00_缓存location表 | 0 |
| T00_JCS_SQL, | T00_缓存SQL表 | 0 |
| T00_MODULE, | T00_功能列表 | 0 |
| T00_MODULE_TEST, | T00_ | 0 |
| T00_NOTICE, | T00_信息公告维护 | 0 |
| T00_ONLINE_LOG, | T00_异步请求操作系统的日志信息 | 0 |
| T00_OPERATE_LOG, | T00_操作日志 | 0 |
| T00_ORGAN, | T00_机构表 | 0 |
| T00_ROLE, T00_ROLE_RESOURCE, T00_SEQUENCE, T00_SYSTEM, T00_SYSTEM_LOG, T00_SYSTEM_PARAM, T00_TREE, T00_USER, T00_USER_INDEXTEMPLATE | T00_角色表 T00_角色资源表 T00_序列表 T00_子系统表 T00_日志管理 T00_系统参数表 T00_树配置表 T00_用户表 用户首页模板数据 | 0 |
