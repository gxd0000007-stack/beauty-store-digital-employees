#!/usr/bin/env python3
"""Generate safe setup plans for one or seven Feishu bot profiles."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]

EMPLOYEES = [
    {
        "employee": "运营总助",
        "app_name": "运营总助 Agent",
        "profile": "store-ops-lead",
        "daemon_label": "ai.lark-channel-bridge.bot.store-ops-lead",
        "stage": "BOT_OK",
    },
    {
        "employee": "回访专员",
        "app_name": "回访专员 Agent",
        "profile": "store-follow-up-specialist",
        "daemon_label": "ai.lark-channel-bridge.bot.store-follow-up-specialist",
        "stage": "7_BOTS_OK",
    },
    {
        "employee": "复购顾问",
        "app_name": "复购顾问 Agent",
        "profile": "store-repurchase-advisor",
        "daemon_label": "ai.lark-channel-bridge.bot.store-repurchase-advisor",
        "stage": "7_BOTS_OK",
    },
    {
        "employee": "客诉专员",
        "app_name": "客诉专员 Agent",
        "profile": "store-complaint-specialist",
        "daemon_label": "ai.lark-channel-bridge.bot.store-complaint-specialist",
        "stage": "7_BOTS_OK",
    },
    {
        "employee": "财务管家",
        "app_name": "财务管家 Agent",
        "profile": "store-finance-steward",
        "daemon_label": "ai.lark-channel-bridge.bot.store-finance-steward",
        "stage": "7_BOTS_OK",
    },
    {
        "employee": "经营分析预警官",
        "app_name": "经营分析预警官 Agent",
        "profile": "store-business-alert-analyst",
        "daemon_label": "ai.lark-channel-bridge.bot.store-business-alert-analyst",
        "stage": "7_BOTS_OK",
    },
    {
        "employee": "知识官",
        "app_name": "知识官 Agent",
        "profile": "store-knowledge-officer",
        "daemon_label": "ai.lark-channel-bridge.bot.store-knowledge-officer",
        "stage": "7_BOTS_OK",
    },
]


def q(value: str) -> str:
    return shlex.quote(value)


def selected_employees(mode: str) -> list[dict]:
    return EMPLOYEES[:1] if mode == "first-bot" else EMPLOYEES


def build_plan(mode: str, workspace: str) -> dict:
    workspace = os.path.abspath(workspace)
    bots = []
    for employee in selected_employees(mode):
        app_id_placeholder = f"<{employee['employee']}_APP_ID>"
        bots.append({
            **employee,
            "required_feishu_steps": [
                f"创建或选择飞书自建应用：{employee['app_name']}",
                "启用机器人能力",
                "添加最小 IM 收发权限",
                "订阅 im.message.receive_v1",
                "选择长连接 / WebSocket 接收事件",
                "发布应用版本",
                "把机器人加入测试会话",
            ],
            "commands": {
                "create_profile": " ".join([
                    "python3",
                    q(str(PACKAGE_ROOT / "scripts" / "build_bridge_profile.py")),
                    "--employee",
                    q(employee["employee"]),
                    "--app-id",
                    q(app_id_placeholder),
                    "--workspace",
                    q(workspace),
                ]),
                "start": " ".join(["lark-channel-bridge", "start", "--profile", q(employee["profile"])]),
                "status": " ".join(["lark-channel-bridge", "status", "--profile", q(employee["profile"])]),
                "smoke_test": " ".join([
                    "python3",
                    q(str(PACKAGE_ROOT / "scripts" / "bot_smoke_test.py")),
                    "--profile",
                    q(employee["profile"]),
                    "--json",
                ]),
            },
        })
    return {
        "mode": mode,
        "workspace": workspace,
        "runtime": "lark-channel-bridge",
        "secret_policy": "App Secret must be entered only into the local bridge prompt; never store it in this package, Base, docs, or chat logs.",
        "writes_performed": False,
        "acceptance": "BOT_OK" if mode == "first-bot" else "7_BOTS_OK",
        "bots": bots,
    }


def to_markdown(plan: dict) -> str:
    lines = [
        f"# BOT 配置计划：{plan['mode']}",
        "",
        f"- Workspace: `{plan['workspace']}`",
        f"- Runtime: `{plan['runtime']}`",
        f"- Acceptance: `{plan['acceptance']}`",
        f"- 写入动作: `{plan['writes_performed']}`",
        f"- Secret policy: {plan['secret_policy']}",
        "",
    ]
    for bot in plan["bots"]:
        lines.extend([
            f"## {bot['employee']} / {bot['app_name']}",
            "",
            f"- Profile: `{bot['profile']}`",
            f"- Daemon label: `{bot['daemon_label']}`",
            "",
            "Feishu 手动步骤:",
            "",
        ])
        lines.extend([f"- {step}" for step in bot["required_feishu_steps"]])
        lines.extend([
            "",
            "Commands:",
            "",
            "```bash",
            bot["commands"]["create_profile"],
            bot["commands"]["start"],
            bot["commands"]["status"],
            bot["commands"]["smoke_test"],
            "```",
            "",
        ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["first-bot", "all-seven"], default="first-bot")
    parser.add_argument("--workspace", default=os.getcwd(), help="Local Codex workspace for the bridge.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    plan = build_plan(args.mode, args.workspace)
    text = json.dumps(plan, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else to_markdown(plan) + "\n"
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
