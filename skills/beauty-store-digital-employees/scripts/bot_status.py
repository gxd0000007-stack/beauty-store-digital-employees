#!/usr/bin/env python3
"""Check lark-channel-bridge status for one or seven bot profiles."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys


EMPLOYEES = [
    {"employee": "运营总助", "profile": "store-ops-lead"},
    {"employee": "回访专员", "profile": "store-follow-up-specialist"},
    {"employee": "复购顾问", "profile": "store-repurchase-advisor"},
    {"employee": "客诉专员", "profile": "store-complaint-specialist"},
    {"employee": "财务管家", "profile": "store-finance-steward"},
    {"employee": "经营分析预警官", "profile": "store-business-alert-analyst"},
    {"employee": "知识官", "profile": "store-knowledge-officer"},
]


def selected_employees(mode: str) -> list[dict]:
    return EMPLOYEES[:1] if mode == "first-bot" else EMPLOYEES


def check_profile(employee: dict, bridge_bin: str) -> dict:
    if not shutil.which(bridge_bin):
        return {
            **employee,
            "ok": False,
            "error": f"{bridge_bin} not found on PATH",
            "stdout": "",
            "stderr": "",
        }
    proc = subprocess.run(
        [bridge_bin, "status", "--profile", employee["profile"]],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = (proc.stdout + "\n" + proc.stderr).lower()
    ok = proc.returncode == 0 and any(signal in output for signal in ["running", "online", "connected", "active"])
    return {
        **employee,
        "ok": ok,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def build_result(mode: str, bridge_bin: str) -> dict:
    checks = [check_profile(employee, bridge_bin) for employee in selected_employees(mode)]
    all_ok = all(item["ok"] for item in checks)
    return {
        "mode": mode,
        "bridge_bin": bridge_bin,
        "ok": all_ok,
        "acceptance": "BOT_OK" if mode == "first-bot" and all_ok else "7_BOTS_OK" if mode == "all-seven" and all_ok else "BLOCKED",
        "writes_performed": False,
        "checks": checks,
    }


def to_markdown(result: dict) -> str:
    lines = [
        f"# BOT 状态：{result['mode']}",
        "",
        f"- OK: `{result['ok']}`",
        f"- Acceptance: `{result['acceptance']}`",
        f"- Writes performed: `{result['writes_performed']}`",
        "",
    ]
    for item in result["checks"]:
        lines.extend([
            f"## {item['employee']}",
            "",
            f"- Profile: `{item['profile']}`",
            f"- OK: `{item['ok']}`",
        ])
        if item.get("error"):
            lines.append(f"- Error: {item['error']}")
        if item.get("stdout"):
            lines.append(f"- Stdout: `{item['stdout']}`")
        if item.get("stderr"):
            lines.append(f"- Stderr: `{item['stderr']}`")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["first-bot", "all-seven"], default="first-bot")
    parser.add_argument("--bridge-bin", default="lark-channel-bridge")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    result = build_result(args.mode, args.bridge_bin)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else to_markdown(result) + "\n"
    sys.stdout.write(text)
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
