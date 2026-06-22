---
name: beauty-store-digital-employees
description: "用于把 Codex 接入学员自己的飞书，并初始化一套标准的美业门店数字员工业务系统。适用于 GitHub 安装后创建客户主表、回访、复购、客诉、财务、经营分析、知识库、7 个数字员工工作流，以及引导配置飞书机器人通过 lark-channel-bridge 回消息；真实飞书写入前必须完成授权、预览和确认。"
---

# Beauty Store Digital Employees

## Core Position

This skill installs and operates a standard Feishu-based beauty store digital employee system for a learner's own Feishu tenant.

Default v1 path: create a new standard business system inside the learner's existing Feishu workspace. In Chinese product terms: 第一版默认「新建标准飞书业务系统」，不适配学员已有飞书结构. Do not adapt an existing Feishu structure unless the user explicitly asks for the advanced adaptation path.

## Workflow

1. Run the local diagnostic:
   `python3 <skill-dir>/scripts/doctor.py --json`
2. If Feishu auth is missing, stop and ask the user to finish `lark-cli auth login` or the local equivalent before continuing.
3. Read `references/standard-system.md` before creating any Feishu objects.
4. Read `references/write-policy.md` before any real write, message send, finance write, customer data update, compensation record, batch change, or delete.
5. Generate the install manifest:
   `python3 <skill-dir>/scripts/build_manifest.py --format markdown`
6. Show the user the target Feishu objects and ask for explicit confirmation before real writes.
7. Use the installed Lark / Feishu skills when available. For raw calls, inspect schema first with `lark-cli schema <service.resource.method> --format pretty`.
8. After writing, create or update a local install record such as `state/beauty-store-install.json` with created URLs, tokens, table IDs, and timestamp. Do not store app secrets, access tokens, cookies, private keys, or raw customer exports.

## Bot Reply Setup

When the user wants Feishu chat replies, run it as a separate stage after the standard system install.

1. Read `references/lark-bot-setup.md` and `references/lark-channel-bridge.md`.
2. Run `python3 <skill-dir>/scripts/bot_doctor.py --json`.
3. If required tools are missing, ask before installing anything globally.
4. Run `python3 <skill-dir>/scripts/open_feishu_console.py --page bot-setup` to open the Feishu Open Platform pages and show the manual checklist.
5. Ask the learner to manually create or configure the `运营总助 Agent` app, enable bot ability, add IM permissions, subscribe to `im.message.receive_v1`, choose long connection, and publish the app version.
6. Run `python3 <skill-dir>/scripts/build_bridge_profile.py --app-id <APP_ID> --workspace <project-path>` to generate safe `lark-channel-bridge` commands. Do not ask the learner to paste App Secret into project files or chat logs.
7. Start with one bot: `运营总助`. Only expand to all 7 bots after `BOT_OK`.
8. Run `python3 <skill-dir>/scripts/bot_smoke_test.py --profile store-ops-lead --json` and ask the learner to send a Feishu message to the bot.

## Default Write Scope

The package may create and write:

- Feishu docs for system overview, SOP, weekly reports, and employee role instructions.
- Feishu Base apps and tables for customers, follow-up, repurchase, complaints, finance, card/session, analytics, knowledge, and action logs.
- Feishu tasks for digital employee work queues.
- Feishu calendar events for recurring review rhythms.
- Feishu IM drafts or messages after explicit preview and confirmation.
- One Feishu bot reply channel for `运营总助 Agent` through `lark-channel-bridge`, after manual Feishu Open Platform configuration.

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
python3 <skill-dir>/scripts/bot_doctor.py --json
```

Expected validation output: `PACKAGE OK`.
