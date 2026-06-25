# Boss Dashboard Template

This reference defines the owner-facing Base template for the GitHub package.

## Canonical Name

`门店表格管理系统｜一张表管公司`

This is the learner-facing template name. The package must not use the maintainer's real Feishu Base token as an install target.

## Product Role

The boss dashboard is the front-stage operating system that a store owner opens every day. It is different from the employee assets folder:

- Boss dashboard: business tables, operating views, dashboards, quick entries, and review pages.
- Employee assets folder: role docs, SOP backups, training materials, knowledge, and install records.

## Install Mode

Default install mode is `create_new_boss_base`.

The package should create a new empty Base structure in the learner's Feishu tenant after explicit confirmation. It should not copy real customer records, real finance records, test records, screenshots, private links, app secrets, or access tokens.

## Native Folder Layout

Use native Base folder blocks where available:

| Folder | Purpose |
| --- | --- |
| 01 首页 | Owner entry, homepage, daily/monthly review shortcuts |
| 02 经营看板 | Daily, monthly, annual operating data and charts |
| 03 顾客管理 | Appointments, consumption, member levels, birthdays, member planning |
| 04 员工管理 | Staff performance, payroll-related analysis, attendance, notes |
| 05 库存管理 | Product cost and inventory movement |
| 06 营销管理 | Activity card sales and marketing budget |
| 07 培训管理 | Onboarding training and project SOP |
| 08 财务管理 | Store expenses, wages, finance dashboards |
| 09 医疗合规管理 | Rescue cart, fridge temperature, product/device filing, sewage disinfection |

## Tables

| Folder | Tables |
| --- | --- |
| 01 首页 | 表格目录与权限 |
| 02 经营看板 | 日经营数据表, 月度经营数据表, 年度经营数据表 |
| 03 顾客管理 | 预约表, 消费表格, 会员等级表, 会员生日提醒, 会员月度规划表, 会员数据统计表 |
| 04 员工管理 | 员工业绩表, 各岗位绩效考核表, 考勤表, 员工日常扣分加分详情表, 员工每日小记 |
| 05 库存管理 | 产品耗材成本表, 出入库台账 |
| 06 营销管理 | 活动购卡登记表, 营销活动预算表 |
| 07 培训管理 | 入职培训表, 全项目流程SOP |
| 08 财务管理 | 店内支出明细, 员工工资表 |
| 09 医疗合规管理 | 抢救车物品登记表, 冰箱温湿度登记表, 产品仪器资质备案, 污水消毒登记表 |

## Homepage

Homepage dashboard name: `首页总览`.

Recommended first screen:

- Button/quick-entry row for key pages.
- Core statistic cards: 今日实收总金额, 本月总现金收入, 今日到店服务客数, 明日预约到店数.
- Daily charts: 近7日实收趋势, 到店成交好评趋势, 今日收款方式拆分, 今日客源业绩拆分, 今日好评平台分布.
- Monthly charts: 本月现金收入结构, 本月实耗与卡金结构, 本月新客来源拆分, 本月客流与客单.

## Daily Operating Fields

`日经营数据表` should include:

- 今日耗卡金额
- 今日项目现金业绩
- 今日产品现金业绩
- 今日实收总金额
- 抖音团购业绩
- 美团团购业绩
- 大众团购业绩
- 小红书散客业绩
- 老带新散客业绩
- 自然流散客业绩
- 微信收款
- 二维码扫码
- 现金收款
- 美团扫码收款
- 今日到店服务客数
- 明日到店服务客数
- 今日好评数
- 好评平台

## Monthly Operating Fields

`月度经营数据表` should include:

- 本月客流量
- 本月实耗合计
- 本月均客单价
- 本月总现金收入
- 本月产品现金合计
- 本月项目充值现金合计
- 新客人数
- 新客数量-抖音
- 新客数量-美团
- 新客数量-转介绍
- 本月未消耗卡金合计

## Quick Entry Contract

Quick entries should point to commonly used tables and dashboards:

- 每天必看
- 每月复盘
- 日经营分析
- 月经营分析
- 年经营分析
- 预约表
- 消费表格
- 会员等级表
- 会员生日提醒
- 会员月度规划表
- 会员数据统计表
- 库存总览
- 产品耗材成本表
- 出入库台账
- 财务总览
- 店内支出明细
- 员工工资表
- 员工业绩
- 合规总览

When a native button component is available, use it. When only text blocks are available, prefer visible raw URLs over hidden links because Feishu dashboard text blocks do not reliably support hidden Markdown links.

## Safety Rules

- Do not ship real Base tokens in public package defaults.
- Do not ship real records or TEST records.
- Do not ship customer names, phones, finance details, or screenshots.
- Generate a preview manifest before writing.
- Ask for explicit confirmation before creating the Base in a learner's tenant.
