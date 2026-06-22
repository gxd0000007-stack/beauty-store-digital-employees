# Standard Feishu Business System

Use this reference when creating the v1 standard system in a learner's Feishu workspace.

## Product Decision

- Install path: create a new standard Feishu business system.
- Do not adapt existing learner structures in v1.
- The learner connects their own Feishu account and tenant.
- Real writes are allowed only after explicit confirmation.
- The system is for beauty store customer management and finance operations, not generic project management.

## Root Objects

Create these top-level objects when the user confirms initial real write:

| Object | Suggested name | Purpose |
| --- | --- | --- |
| Root folder | 美业门店数字员工系统-v1 | Contains all generated docs and links |
| Main Base | 美业门店数字员工系统-v1 | Holds structured business data |
| System overview doc | 00-系统总览与使用说明 | Owner-facing entry doc |
| Employee roles doc | 01-7个数字员工职责说明 | Human-readable role map |
| SOP doc | 02-客户管理与财务SOP | Daily operating rules |
| Weekly report doc | 03-经营分析周报模板 | Analysis output template |
| Knowledge doc folder | 04-知识库 | Talk tracks, cases, SOP, retrospectives |

## Base Tables

### 1. 客户主表

The customer table is the spine of the system.

| Field | Type | Notes |
| --- | --- | --- |
| 客户ID | auto number/text | Stable customer key |
| 姓名 | text | Required |
| 手机号 | text | Preferred unique key; allow missing with 待补手机号 |
| 性别 | single select | 女/男/未知 |
| 生日 | date | Birthday follow-up |
| 来源渠道 | single select | 门店/转介绍/小红书/抖音/美团/其他 |
| 首次到店日期 | date | Customer lifecycle |
| 最近到店日期 | date | Sleep/loss judgment |
| 客户状态 | single select | 新客/活跃/沉睡/流失/客诉中/已归档 |
| 价值分层 | single select | 高价值/普通/待判断 |
| 标签 | multi select | Skin needs, preference, risk tags |
| 累计消费金额 | number | Can be manually entered or summarized |
| 卡金余额 | number | Reconcile with card/session table |
| 疗程剩余 | number | Reconcile with card/session table |
| 负责顾问 | text/user | Human owner |
| 备注 | text | No private exports |

### 2. 回访任务表

| Field | Type | Notes |
| --- | --- | --- |
| 任务ID | auto number/text | Stable task key |
| 关联客户 | relation | Link to 客户主表 |
| 回访节点 | single select | 次日/3天/7天/生日/沉睡/高价值/其他 |
| 负责数字员工 | single select | 默认回访专员 |
| 状态 | single select | 待办/进行中/已完成/已升级老板 |
| 优先级 | single select | 高/中/低 |
| 截止时间 | date | Follow-up deadline |
| 话术草稿 | text | Draft before real touch |
| 回访结果 | text | Result summary |
| 风险信号 | multi select | 复购/客诉/财务异常/无 |

### 3. 复购机会表

| Field | Type | Notes |
| --- | --- | --- |
| 机会ID | auto number/text | Stable opportunity key |
| 关联客户 | relation | Link to 客户主表 |
| 机会类型 | single select | 续卡/疗程消耗/卡金不足/未成交/项目推荐 |
| 意向强度 | single select | 高/中/低/待判断 |
| 推荐方向 | text | Project direction, not final quote |
| 跟进话术 | text | Draft |
| 报价/优惠状态 | single select | 未涉及/需老板确认/已老板确认 |
| 状态 | single select | 待跟进/跟进中/成交/暂停/已升级老板 |

### 4. 客诉处理表

| Field | Type | Notes |
| --- | --- | --- |
| 客诉ID | auto number/text | Stable case key |
| 关联客户 | relation | Link to 客户主表 |
| 客诉等级 | single select | 轻/中/重 |
| 客诉类型 | single select | 效果/服务/价格/退款/公开投诉/其他 |
| 事实摘要 | text | Separate facts from emotions |
| 证据清单 | text | Records, screenshots, staff notes |
| 安抚话术 | text | Draft before sending |
| 处理建议 | text | Recommendation only |
| 赔付/退款状态 | single select | 不涉及/需老板确认/已老板确认 |
| 状态 | single select | 新建/处理中/已升级老板/已关闭 |

### 5. 财务记录表

| Field | Type | Notes |
| --- | --- | --- |
| 记录ID | auto number/text | Stable finance key |
| 关联客户 | relation | Optional link to 客户主表 |
| 记录类型 | single select | 收款/退款/扣次/卡金调整/成本/对账异常 |
| 金额 | number | Confirm before real finance write |
| 发生日期 | date | Business date |
| 经办人 | text/user | Human owner |
| 来源单据 | text/url | Receipt or source reference |
| 核对状态 | single select | 待核对/已核对/异常/已升级老板 |
| 备注 | text | Avoid private exports |

### 6. 卡金与疗程表

| Field | Type | Notes |
| --- | --- | --- |
| 记录ID | auto number/text | Stable key |
| 关联客户 | relation | Link to 客户主表 |
| 类型 | single select | 卡金/赠送额/疗程 |
| 项目名称 | text | Course or card item |
| 初始金额/次数 | number | Starting value |
| 剩余金额/次数 | number | Current value |
| 有效期 | date | Optional |
| 状态 | single select | 正常/待核对/异常/已结束 |

### 7. 经营分析指标表

| Field | Type | Notes |
| --- | --- | --- |
| 指标ID | auto number/text | Stable key |
| 周期 | date/text | Week or month |
| 指标类型 | single select | 业绩/客单/复购/留存/客诉/成本/利润 |
| 指标值 | number | Metric value |
| 口径说明 | text | Formula or source |
| 预警等级 | single select | 无/低/中/高 |
| 分析结论 | text | Draft conclusion |

### 8. 知识沉淀表

| Field | Type | Notes |
| --- | --- | --- |
| 知识ID | auto number/text | Stable key |
| 类型 | single select | 话术/SOP/案例/失败复盘/规则 |
| 标题 | text | Knowledge title |
| 适用场景 | text | When to use |
| 正文 | text | Content |
| 来源 | text | Task, complaint, meeting, owner |
| 状态 | single select | 草稿/已确认/已废弃 |

### 9. 写入日志与确认表

| Field | Type | Notes |
| --- | --- | --- |
| 日志ID | auto number/text | Stable key |
| 动作类型 | single select | 文档/Base/任务/日历/IM/财务/客诉/删除 |
| 风险等级 | single select | L1/L2/L3/L4/L5 |
| 预览摘要 | text | What will change |
| 确认人 | text/user | Owner who approved |
| 确认时间 | date | Confirmation timestamp |
| 执行状态 | single select | 待执行/已执行/BLOCKED/失败 |
| 结果链接 | text/url | Created object URL if any |

## Digital Employees

Create docs or sections for these 7 个数字员工:

1. 运营总助
2. 回访专员
3. 复购顾问
4. 客诉专员
5. 财务管家
6. 经营分析预警官
7. 知识官

## Task, Calendar, And IM Defaults

- Tasks: create queues for follow-up, repurchase, complaints, finance checks, analytics review, and knowledge updates.
- Calendar: create optional weekly business review and monthly finance review events after confirmation.
- IM: generate previewable message templates first. Send only after the user confirms recipient, content, and timing.
