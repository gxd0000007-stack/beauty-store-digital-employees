#!/usr/bin/env python3
"""Validate the beauty-store-digital-employees skill package."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


PRODUCT_NAME = "门店表格管理系统｜一张表管公司"

REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "examples/first-run-prompt.md",
    "manifests/boss-base-template.json",
    "manifests/employee-folder-template.json",
    "references/standard-system.md",
    "references/write-policy.md",
    "references/lark-bot-setup.md",
    "references/lark-channel-bridge.md",
    "references/boss-dashboard-template.md",
    "references/employee-assets-folder.md",
    "references/install-flow.md",
    "references/all-seven-bots.md",
    "references/long-running-daemons.md",
    "scripts/build_manifest.py",
    "scripts/build_boss_base_manifest.py",
    "scripts/build_employee_folder_manifest.py",
    "scripts/doctor.py",
    "scripts/bot_doctor.py",
    "scripts/open_feishu_console.py",
    "scripts/build_bridge_profile.py",
    "scripts/setup_all_employee_bots.py",
    "scripts/install_bot_daemons.py",
    "scripts/bot_smoke_test.py",
    "scripts/bot_status.py",
    "scripts/validate_package.py",
]

SCRIPT_FILES = [path for path in REQUIRED_FILES if path.startswith("scripts/")]

FORBIDDEN_PRIVATE_STRINGS = [
    "BM" + "66bgzfDaNX0WsocUzcW4NGnHd",
    "X0" + "X0fE6q0lKA0udChROcopAdn9d",
    "zk8mfimksh" + ".feishu.cn",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_json(script: Path, *args: str) -> tuple[dict | None, str | None]:
    proc = subprocess.run([sys.executable, str(script), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        return None, proc.stderr.strip() or proc.stdout.strip()
    try:
        return json.loads(proc.stdout), None
    except Exception as exc:  # pragma: no cover - validation output path
        return None, str(exc)


def check_keywords(errors: list[str], root: Path, rel: str, keywords: list[str]) -> None:
    path = root / rel
    if not path.is_file():
        return
    text = read(path)
    for keyword in keywords:
        if keyword not in text:
            errors.append(f"{rel} missing keyword: {keyword}")


def check_no_private_strings(errors: list[str], root: Path) -> None:
    suffixes = {".md", ".json", ".py", ".yaml", ".yml"}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        try:
            text = read(path)
        except UnicodeDecodeError:
            continue
        for forbidden in FORBIDDEN_PRIVATE_STRINGS:
            if forbidden in text:
                errors.append(f"private source string leaked in {path.relative_to(root)}: {forbidden}")


def check_manifest(errors: list[str], root: Path) -> None:
    data, err = run_json(root / "scripts" / "build_manifest.py", "--format", "json")
    if err:
        errors.append("build_manifest.py failed: " + err)
        return
    assert data is not None
    if data.get("schema_version") != "2.0.0":
        errors.append("manifest schema_version mismatch")
    if data.get("product_name") != PRODUCT_NAME:
        errors.append("manifest product_name mismatch")
    if data.get("install_strategy") != "create_new_boss_base_and_employee_assets":
        errors.append("manifest install_strategy mismatch")
    if data.get("adapt_existing_workspace") is not False:
        errors.append("manifest must not adapt existing workspace by default")
    if data.get("store_real_tokens") is not False:
        errors.append("manifest must not store real tokens")
    if data.get("copy_real_records") is not False:
        errors.append("manifest must not copy real records")

    boss = data.get("boss_base_template", {})
    if boss.get("template_name") != PRODUCT_NAME:
        errors.append("boss template name mismatch in manifest")
    if len(boss.get("native_folders", [])) != 9:
        errors.append("boss template must include 9 native folders")
    if len(boss.get("homepage", {}).get("quick_entries", [])) != 19:
        errors.append("boss homepage must include 19 quick entries")

    folder = data.get("employee_assets_template", {})
    if folder.get("template_name") != "美业门店数字员工资料与备份":
        errors.append("employee assets folder name mismatch")
    if len(folder.get("employees", [])) != 7:
        errors.append("employee assets folder must include 7 employees")

    if len(data.get("digital_employee_control_tables", [])) < 9:
        errors.append("manifest has too few digital employee control tables")

    bot = data.get("bot_reply_setup", {})
    if bot.get("runtime") != "lark-channel-bridge":
        errors.append("manifest bot runtime mismatch")
    if bot.get("first_profile") != "store-ops-lead":
        errors.append("manifest first bot profile mismatch")
    if bot.get("all_seven_supported") is not True:
        errors.append("manifest must support all seven bots")
    if len(bot.get("profiles", [])) != 7:
        errors.append("manifest must include 7 bot profiles")


def check_template_scripts(errors: list[str], root: Path) -> None:
    boss, err = run_json(root / "scripts" / "build_boss_base_manifest.py", "--format", "json")
    if err:
        errors.append("build_boss_base_manifest.py failed: " + err)
    elif boss is not None:
        if boss.get("template_name") != PRODUCT_NAME:
            errors.append("boss Base template script name mismatch")
        if len(boss.get("homepage", {}).get("quick_entries", [])) != 19:
            errors.append("boss Base template script quick entry mismatch")

    folder, err = run_json(root / "scripts" / "build_employee_folder_manifest.py", "--format", "json")
    if err:
        errors.append("build_employee_folder_manifest.py failed: " + err)
    elif folder is not None:
        if folder.get("template_name") != "美业门店数字员工资料与备份":
            errors.append("employee folder template script name mismatch")
        if len(folder.get("folders", [])) < 7:
            errors.append("employee folder template needs 7 folders")

    bots, err = run_json(root / "scripts" / "setup_all_employee_bots.py", "--mode", "all-seven", "--format", "json")
    if err:
        errors.append("setup_all_employee_bots.py failed: " + err)
    elif bots is not None:
        if bots.get("acceptance") != "7_BOTS_OK":
            errors.append("all-seven bot plan acceptance mismatch")
        if len(bots.get("bots", [])) != 7:
            errors.append("all-seven bot plan must include 7 bots")
        if bots.get("writes_performed") is not False:
            errors.append("all-seven bot plan must not write")

    daemons, err = run_json(root / "scripts" / "install_bot_daemons.py", "--mode", "all-seven", "--dry-run", "--format", "json")
    if err:
        errors.append("install_bot_daemons.py dry run failed: " + err)
    elif daemons is not None:
        if daemons.get("writes_performed") is not False:
            errors.append("daemon dry run must not write")
        if daemons.get("launchctl_executed") is not False:
            errors.append("daemon dry run must not run launchctl")
        if len(daemons.get("items", [])) != 7:
            errors.append("daemon dry run must include 7 items")


def check_py_compile(errors: list[str], root: Path) -> None:
    for rel in SCRIPT_FILES:
        path = root / rel
        if not path.is_file():
            continue
        proc = subprocess.run([sys.executable, "-m", "py_compile", str(path)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            errors.append(rel + " py_compile failed: " + proc.stderr.strip())


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append("missing file: " + rel)

    check_keywords(errors, root, "SKILL.md", [
        "name: beauty-store-digital-employees",
        PRODUCT_NAME,
        "references/boss-dashboard-template.md",
        "references/employee-assets-folder.md",
        "BOT_OK",
        "7_BOTS_OK",
        "lark-channel-bridge",
    ])
    check_keywords(errors, root, "references/standard-system.md", [
        PRODUCT_NAME,
        "美业门店数字员工资料与备份",
        "客户主表",
        "写入日志与确认表",
        "7 个数字员工",
    ])
    check_keywords(errors, root, "references/boss-dashboard-template.md", [
        PRODUCT_NAME,
        "01 首页",
        "09 医疗合规管理",
        "Quick Entry Contract",
        "本月未消耗卡金合计",
    ])
    check_keywords(errors, root, "references/employee-assets-folder.md", [
        "美业门店数字员工资料与备份",
        "Role docs",
        "Backup Policy",
    ])
    check_keywords(errors, root, "references/lark-bot-setup.md", [
        "SYSTEM_OK",
        "BOT_OK",
        "7_BOTS_OK",
        "运营总助 Agent",
        "im.message.receive_v1",
        "App Secret",
    ])
    check_keywords(errors, root, "references/lark-channel-bridge.md", [
        "Node.js",
        "lark-channel-bridge",
        "store-ops-lead",
        "setup_all_employee_bots.py",
        "install_bot_daemons.py",
    ])
    check_keywords(errors, root, "references/write-policy.md", [
        "L1",
        "L2",
        "L3",
        "L4",
        "L5",
        "BLOCKED: waiting for write confirmation",
    ])

    check_no_private_strings(errors, root)
    check_manifest(errors, root)
    check_template_scripts(errors, root)
    check_py_compile(errors, root)

    if errors:
        print("PACKAGE FAIL")
        for err in errors:
            print(" -", err)
        return 1
    print("PACKAGE OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
