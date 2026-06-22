#!/usr/bin/env python3
"""Validate the beauty-store-digital-employees skill package."""
import json
import os
import subprocess
import sys


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/standard-system.md",
    "references/write-policy.md",
    "references/lark-bot-setup.md",
    "references/lark-channel-bridge.md",
    "scripts/build_manifest.py",
    "scripts/doctor.py",
    "scripts/bot_doctor.py",
    "scripts/open_feishu_console.py",
    "scripts/build_bridge_profile.py",
    "scripts/bot_smoke_test.py",
    "scripts/validate_package.py",
    "examples/first-run-prompt.md",
]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), ".."))
    errors = []

    for rel in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(root, rel)):
            errors.append("missing file: " + rel)

    skill = os.path.join(root, "SKILL.md")
    if os.path.isfile(skill):
        text = read(skill)
        for kw in [
            "name: beauty-store-digital-employees",
            "新建",
            "标准",
            "真实飞书写入前必须完成授权",
            "references/standard-system.md",
            "references/write-policy.md",
            "references/lark-bot-setup.md",
            "lark-channel-bridge",
        ]:
            if kw not in text:
                errors.append("SKILL.md missing keyword: " + kw)

    standard = os.path.join(root, "references/standard-system.md")
    if os.path.isfile(standard):
        text = read(standard)
        for kw in ["客户主表", "回访任务表", "复购机会表", "客诉处理表", "财务记录表", "写入日志与确认表", "7 个数字员工"]:
            if kw not in text:
                errors.append("standard-system.md missing keyword: " + kw)

    policy = os.path.join(root, "references/write-policy.md")
    if os.path.isfile(policy):
        text = read(policy)
        for kw in ["L1", "L2", "L3", "L4", "L5", "BLOCKED: waiting for write confirmation"]:
            if kw not in text:
                errors.append("write-policy.md missing keyword: " + kw)

    bot_setup = os.path.join(root, "references/lark-bot-setup.md")
    if os.path.isfile(bot_setup):
        text = read(bot_setup)
        for kw in ["SYSTEM_OK", "BOT_OK", "运营总助 Agent", "im.message.receive_v1", "App Secret"]:
            if kw not in text:
                errors.append("lark-bot-setup.md missing keyword: " + kw)

    bridge_ref = os.path.join(root, "references/lark-channel-bridge.md")
    if os.path.isfile(bridge_ref):
        text = read(bridge_ref)
        for kw in ["Node.js", "lark-channel-bridge", "store-ops-lead", "bot_smoke_test.py"]:
            if kw not in text:
                errors.append("lark-channel-bridge.md missing keyword: " + kw)

    manifest_script = os.path.join(root, "scripts/build_manifest.py")
    if os.path.isfile(manifest_script):
        proc = subprocess.run([sys.executable, manifest_script, "--format", "json"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            errors.append("build_manifest.py failed: " + proc.stderr.strip())
        else:
            try:
                data = json.loads(proc.stdout)
                if data.get("install_strategy") != "create_new_standard_feishu_business_system":
                    errors.append("manifest install_strategy mismatch")
                if data.get("adapt_existing_workspace") is not False:
                    errors.append("manifest must not adapt existing workspace by default")
                if len(data.get("base", {}).get("tables", [])) < 9:
                    errors.append("manifest has too few tables")
                if len(data.get("employees", [])) != 7:
                    errors.append("manifest must include 7 employees")
                bot = data.get("bot_reply_setup", {})
                if bot.get("runtime") != "lark-channel-bridge":
                    errors.append("manifest bot runtime mismatch")
                if bot.get("first_profile") != "store-ops-lead":
                    errors.append("manifest first bot profile mismatch")
            except Exception as exc:
                errors.append("manifest JSON parse failed: " + str(exc))

    for rel in [
        "scripts/doctor.py",
        "scripts/bot_doctor.py",
        "scripts/open_feishu_console.py",
        "scripts/build_bridge_profile.py",
        "scripts/bot_smoke_test.py",
        "scripts/validate_package.py",
    ]:
        path = os.path.join(root, rel)
        if os.path.isfile(path):
            proc = subprocess.run([sys.executable, "-m", "py_compile", path], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode != 0:
                errors.append(rel + " py_compile failed: " + proc.stderr.strip())

    if errors:
        print("PACKAGE FAIL")
        for err in errors:
            print(" -", err)
        return 1
    print("PACKAGE OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
