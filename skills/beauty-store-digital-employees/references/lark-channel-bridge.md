# lark-channel-bridge

Use this reference when connecting Feishu chat to local Codex replies.

## Role In This Package

`lark-channel-bridge` is the local runtime that receives Feishu/Lark bot messages and forwards them to Codex CLI. It is used for `BOT_OK`, not for the initial standard system schema design.

## Requirements

- Node.js `>=20.12.0`
- Codex CLI installed and logged in
- `lark-channel-bridge` installed globally
- A Feishu enterprise self-built app with bot ability
- Event subscription: `im.message.receive_v1`
- Long connection / WebSocket event receiving mode
- Published app version

## Install Check

Run:

```bash
python3 <skill-dir>/scripts/bot_doctor.py --json
```

If `lark-channel-bridge` is missing, ask before installing globally:

```bash
npm i -g lark-channel-bridge
```

## Profile Naming

First bot:

| Field | Value |
| --- | --- |
| Employee | 运营总助 |
| Profile | store-ops-lead |
| App name | 运营总助 Agent |
| Agent | codex |

Future bots may use:

| Employee | Profile |
| --- | --- |
| 回访专员 | store-follow-up-specialist |
| 复购顾问 | store-repurchase-advisor |
| 客诉专员 | store-complaint-specialist |
| 财务管家 | store-finance-steward |
| 经营分析预警官 | store-business-alert-analyst |
| 知识官 | store-knowledge-officer |

## Safe Command Generation

Generate commands with:

```bash
python3 <skill-dir>/scripts/build_bridge_profile.py --app-id cli_xxx --workspace /path/to/project
```

The generated command should let `lark-channel-bridge` prompt locally for App Secret. Do not place App Secret in command-line arguments, files, docs, or logs.

## Smoke Test

After starting the bridge:

```bash
python3 <skill-dir>/scripts/bot_smoke_test.py --profile store-ops-lead --json
```

Then ask the learner to send this Feishu message to `运营总助 Agent`:

```text
状态自检：你是谁？请用一句话说明你负责什么。
```

Acceptance:

- Bridge status is running for `store-ops-lead`.
- Feishu receives a reply.
- Reply identifies `运营总助` and does not promise high-risk automatic actions.
