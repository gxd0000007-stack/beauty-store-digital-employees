#!/usr/bin/env python3
"""Generate optional macOS launchd plists for lark-channel-bridge bot profiles."""
from __future__ import annotations

import argparse
import json
import os
import plistlib
import sys
from pathlib import Path


EMPLOYEES = [
    {"employee": "运营总助", "profile": "store-ops-lead", "label": "ai.lark-channel-bridge.bot.store-ops-lead"},
    {"employee": "回访专员", "profile": "store-follow-up-specialist", "label": "ai.lark-channel-bridge.bot.store-follow-up-specialist"},
    {"employee": "复购顾问", "profile": "store-repurchase-advisor", "label": "ai.lark-channel-bridge.bot.store-repurchase-advisor"},
    {"employee": "客诉专员", "profile": "store-complaint-specialist", "label": "ai.lark-channel-bridge.bot.store-complaint-specialist"},
    {"employee": "财务管家", "profile": "store-finance-steward", "label": "ai.lark-channel-bridge.bot.store-finance-steward"},
    {"employee": "经营分析预警官", "profile": "store-business-alert-analyst", "label": "ai.lark-channel-bridge.bot.store-business-alert-analyst"},
    {"employee": "知识官", "profile": "store-knowledge-officer", "label": "ai.lark-channel-bridge.bot.store-knowledge-officer"},
]


def selected_employees(mode: str) -> list[dict]:
    return EMPLOYEES[:1] if mode == "first-bot" else EMPLOYEES


def plist_payload(employee: dict, workspace: str, bridge_bin: str, log_dir: Path) -> dict:
    profile = employee["profile"]
    return {
        "Label": employee["label"],
        "ProgramArguments": ["/usr/bin/env", bridge_bin, "start", "--profile", profile],
        "WorkingDirectory": workspace,
        "RunAtLoad": True,
        "KeepAlive": True,
        "StandardOutPath": str(log_dir / f"{profile}.out.log"),
        "StandardErrorPath": str(log_dir / f"{profile}.err.log"),
    }


def build_plan(mode: str, workspace: str, bridge_bin: str, output_dir: str | None, install: bool, dry_run: bool) -> dict:
    workspace = os.path.abspath(workspace)
    home = Path.home()
    log_dir = home / "Library" / "Logs" / "beauty-store-digital-employees"
    target_dir = Path(output_dir).expanduser() if output_dir else home / "Library" / "LaunchAgents"
    should_write = (bool(output_dir) or install) and not dry_run
    items = []
    if should_write:
        target_dir.mkdir(parents=True, exist_ok=True)
        log_dir.mkdir(parents=True, exist_ok=True)

    for employee in selected_employees(mode):
        payload = plist_payload(employee, workspace, bridge_bin, log_dir)
        plist_name = f"{employee['label']}.plist"
        target_path = target_dir / plist_name
        plist_bytes = plistlib.dumps(payload, sort_keys=False)
        if should_write:
            target_path.write_bytes(plist_bytes)
        items.append({
            "employee": employee["employee"],
            "profile": employee["profile"],
            "label": employee["label"],
            "plist_path": str(target_path),
            "plist_preview": plist_bytes.decode("utf-8"),
            "wrote_file": should_write,
            "bootstrap_command": f"launchctl bootstrap gui/$(id -u) {target_path}",
            "kickstart_command": f"launchctl kickstart -k gui/$(id -u)/{employee['label']}",
        })
    return {
        "mode": mode,
        "workspace": workspace,
        "bridge_bin": bridge_bin,
        "platform": "macos_launchd",
        "target_dir": str(target_dir),
        "log_dir": str(log_dir),
        "dry_run": dry_run,
        "install_requested": install,
        "writes_performed": should_write,
        "launchctl_executed": False,
        "secret_policy": "Plists contain only profile names and local paths. App Secret stays inside lark-channel-bridge local profile storage.",
        "items": items,
    }


def to_markdown(plan: dict) -> str:
    lines = [
        f"# 长期在线配置：{plan['mode']}",
        "",
        f"- Platform: `{plan['platform']}`",
        f"- Workspace: `{plan['workspace']}`",
        f"- Target dir: `{plan['target_dir']}`",
        f"- Log dir: `{plan['log_dir']}`",
        f"- Writes performed: `{plan['writes_performed']}`",
        f"- launchctl executed: `{plan['launchctl_executed']}`",
        f"- Secret policy: {plan['secret_policy']}",
        "",
    ]
    for item in plan["items"]:
        lines.extend([
            f"## {item['employee']}",
            "",
            f"- Profile: `{item['profile']}`",
            f"- Label: `{item['label']}`",
            f"- Plist: `{item['plist_path']}`",
            f"- Wrote file: `{item['wrote_file']}`",
            "",
            "Install commands after reviewing the plist:",
            "",
            "```bash",
            item["bootstrap_command"],
            item["kickstart_command"],
            "```",
            "",
        ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["first-bot", "all-seven"], default="first-bot")
    parser.add_argument("--workspace", default=os.getcwd())
    parser.add_argument("--bridge-bin", default="lark-channel-bridge")
    parser.add_argument("--output-dir", help="Write plist files to this directory. Without this or --install, only preview.")
    parser.add_argument("--install", action="store_true", help="Write plists to ~/Library/LaunchAgents, but do not run launchctl.")
    parser.add_argument("--dry-run", action="store_true", help="Preview only even when --output-dir or --install is present.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    plan = build_plan(args.mode, args.workspace, args.bridge_bin, args.output_dir, args.install, args.dry_run)
    text = json.dumps(plan, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else to_markdown(plan) + "\n"
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
