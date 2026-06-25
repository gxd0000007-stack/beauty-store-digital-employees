# Employee Assets Folder

This reference defines the back-stage employee assets and backup area.

## Canonical Role

The employee assets folder is not the boss dashboard. It is the backstage knowledge and backup warehouse for the digital employee system.

Recommended folder name:

`美业门店数字员工资料与备份`

## Relationship To The Boss Base

| Area | User | Purpose |
| --- | --- | --- |
| 门店表格管理系统｜一张表管公司 | Boss / operator | Daily business operation, dashboards, tables, review |
| 美业门店数字员工资料与备份 | Owner / implementer / digital employees | Role docs, SOP, training, scripts, backup notes, install records |

## Folder Layout

| Folder | Purpose |
| --- | --- |
| 00-安装记录 | Created resources, URLs, dates, version notes |
| 01-7个数字员工 | Role docs for each employee |
| 02-SOP与流程 | Daily operating rules and standard procedures |
| 03-话术与知识库 | Talk tracks, cases, rules, content snippets |
| 04-培训资料 | Onboarding and classroom materials |
| 05-备份与导出说明 | Backup policy, manual export instructions, restore notes |
| 06-问题与复盘 | Debug logs, incident reviews, improvement backlog |

## Digital Employee Files

Create one document or markdown-backed doc for each employee:

- 运营总助
- 回访专员
- 复购顾问
- 客诉专员
- 财务管家
- 经营分析预警官
- 知识官

Each role document should include:

- Role mission
- Allowed low-risk actions
- Hard-stop actions requiring boss confirmation
- Input sources
- Output format
- Escalation rules
- Handoff rules to other employees

## Backup Policy

The GitHub package may create the folder skeleton and blank template docs. It must not export or store:

- App Secret
- access token
- raw customer exports
- raw finance exports
- private screenshots
- compensation/refund decisions

## Install Record

After confirmed creation, write a local install record such as:

`state/beauty-store-install.json`

The record may include:

- timestamps
- created folder URLs
- created Base URL
- dashboard IDs
- bot profile names
- daemon labels

The record must not include secrets.
