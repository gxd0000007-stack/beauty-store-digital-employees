---
name: beauty-store-digital-employees
description: "用于把 Codex 接入学员自己的飞书，并初始化「门店表格管理系统｜一张表管公司」：老板看的 Base、员工资料/备份文件夹、7 个数字员工 BOT 配置计划、lark-channel-bridge 长期在线方案。真实飞书写入前必须完成授权、预览和确认；安装包不得复制维护者真实 Base token、真实数据或 App Secret。"
---

# Beauty Store Digital Employees

## Core Position

This skill installs a Feishu-based beauty store operating package for a learner's own Feishu tenant.

Canonical product name:

`门店表格管理系统｜一张表管公司`

Default path: create a new empty owner-facing Base plus a new employee assets/backup folder. Do not adapt an existing learner Feishu structure, copy the maintainer's live Base, import real records, or store private tokens unless the user explicitly chooses a separate advanced migration path.

## Install Workflow

1. Run environment checks:
   `python3 <skill-dir>/scripts/doctor.py --json`
   `python3 <skill-dir>/scripts/bot_doctor.py --json`
2. Read `references/install-flow.md`, `references/boss-dashboard-template.md`, and `references/employee-assets-folder.md`.
3. Generate the full install manifest:
   `python3 <skill-dir>/scripts/build_manifest.py --format markdown`
4. Generate the boss Base preview:
   `python3 <skill-dir>/scripts/build_boss_base_manifest.py --format markdown`
5. Generate the employee assets folder preview:
   `python3 <skill-dir>/scripts/build_employee_folder_manifest.py --format markdown`
6. Read `references/write-policy.md` before any real write.
7. Show the user exactly what will be created and ask for explicit confirmation before writing real Feishu objects.
8. After writing, create or update a local install record such as `state/beauty-store-install.json` with created URLs, tokens, table IDs, and timestamp. Do not store app secrets, access tokens, cookies, private keys, or raw customer exports.

## Boss Base Scope

Create a new Base named `门店表格管理系统｜一张表管公司` after confirmation.

The Base template contains:

- 9 native folder groups: 首页、经营看板、顾客管理、员工管理、库存管理、营销管理、培训管理、财务管理、医疗合规管理.
- Owner homepage: 首页总览.
- Daily operating data fields: cash performance, card consumption, channel sales, payment methods, traffic, tomorrow arrivals, reviews.
- Monthly operating data fields: traffic, actual consumption, average order value, cash income, product cash, project recharge cash, new customers by source, unused card value.
- 19 homepage quick entries for commonly used tables and dashboards.

The package must not ship the maintainer's real Base token, real test rows, customer data, finance data, private screenshots, or hidden links.

## Employee Assets Scope

Create a new Drive folder named `美业门店数字员工资料与备份` after confirmation.

It is the backstage area for:

- install records and version changes
- 7 digital employee role docs
- SOP and process backups
- talk tracks and knowledge
- training materials
- backup/export instructions
- issue records and retrospectives

This folder is different from the boss Base. The boss Base is for operating data; the employee folder is for role brains, training, backup, and recovery materials.

## Bot Reply Setup

Bot reply is a separate stage after the standard system is created.

1. Read `references/lark-bot-setup.md`, `references/lark-channel-bridge.md`, `references/all-seven-bots.md`, and `references/long-running-daemons.md`.
2. Run `python3 <skill-dir>/scripts/bot_doctor.py --json`.
3. Start with `运营总助 Agent`:
   `python3 <skill-dir>/scripts/build_bridge_profile.py --employee 运营总助 --app-id <APP_ID> --workspace <project-path>`
4. Run `python3 <skill-dir>/scripts/bot_smoke_test.py --profile store-ops-lead --json`.
5. Acceptance for first bot: `BOT_OK`.
6. Only after `BOT_OK`, plan all 7 bots:
   `python3 <skill-dir>/scripts/setup_all_employee_bots.py --mode all-seven --format markdown`.
   Acceptance for all seven bots: `7_BOTS_OK`.
7. Optional long-running macOS launchd preview:
   `python3 <skill-dir>/scripts/install_bot_daemons.py --mode all-seven --dry-run --format markdown`.
8. Status check:
   `python3 <skill-dir>/scripts/bot_status.py --mode all-seven --format json`.

Do not ask the learner to paste App Secret into project files, chat logs, docs, or Base records. Each Feishu app still requires manual bot ability, IM permissions, `im.message.receive_v1`, long connection mode, and published app version.

## Digital Employees

The first stage can run one bot; the advanced stage can configure all seven:

- 运营总助
- 回访专员
- 复购顾问
- 客诉专员
- 财务管家
- 经营分析预警官
- 知识官

## Default Write Scope

The package may create and write after explicit confirmation:

- A new owner-facing Base named `门店表格管理系统｜一张表管公司`.
- A new employee assets/backup Drive folder named `美业门店数字员工资料与备份`.
- Docs, tables, fields, dashboards, tasks, calendar events, and IM drafts needed by the template.
- One Feishu bot reply channel first, then optional seven bot profiles and launchd plist previews.

## Required Risk Gate

Real write ability is built in, but high-risk operations are not silent.

Before any of these actions, show a preview and require explicit user confirmation:

- Sending or group-sending IM messages.
- Creating or modifying real customer records.
- Writing finance records, balances, refunds, card value, or session counts.
- Recording complaint compensation or refund decisions.
- Modifying Base fields or structure after the initial standard-system creation.
- Batch updates, deletes, privacy exports, or production automation.

If the user has not confirmed the exact action, stop with `BLOCKED: waiting for write confirmation`.

## Validation

Before considering the package healthy, run:

```bash
python3 <skill-dir>/scripts/validate_package.py <skill-dir>
python3 <skill-dir>/scripts/build_manifest.py --format json
python3 <skill-dir>/scripts/build_boss_base_manifest.py --format json
python3 <skill-dir>/scripts/build_employee_folder_manifest.py --format json
python3 <skill-dir>/scripts/setup_all_employee_bots.py --mode all-seven --format json
python3 <skill-dir>/scripts/install_bot_daemons.py --mode all-seven --dry-run --format json
```

Expected validation output: `PACKAGE OK`.
