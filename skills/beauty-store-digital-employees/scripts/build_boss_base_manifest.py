#!/usr/bin/env python3
"""Render the owner-facing boss Base template manifest."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = PACKAGE_ROOT / "manifests" / "boss-base-template.json"


def load_manifest() -> dict:
    with TEMPLATE_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def to_markdown(data: dict) -> str:
    homepage = data["homepage"]
    lines = [
        f"# {data['template_name']} 老板 Base 模板",
        "",
        f"- 模板角色: `{data['template_role']}`",
        f"- 安装模式: `{data['install_mode']}`",
        f"- 复制真实记录: `{data['copy_real_records']}`",
        f"- 保存真实 token: `{data['store_real_tokens']}`",
        "",
        "## 原生分组",
        "",
    ]
    for folder in data["native_folders"]:
        lines.append(f"### {folder['name']}")
        lines.append("")
        lines.append("表格: " + ", ".join(folder["tables"]))
        lines.append("仪表盘: " + ", ".join(folder["dashboards"]))
        lines.append("")

    lines.extend([
        "## 首页总览",
        "",
        f"- 看板名: {homepage['dashboard_name']}",
        f"- 核心统计: {', '.join(homepage['core_statistics'])}",
        f"- 日数据图表: {', '.join(homepage['daily_charts'])}",
        f"- 月数据图表: {', '.join(homepage['monthly_charts'])}",
        f"- 快捷入口: {', '.join(homepage['quick_entries'])}",
        "",
        "## 经营数据字段",
        "",
    ])
    for table_name, fields in data["required_operating_fields"].items():
        lines.append(f"### {table_name}")
        lines.append("")
        lines.extend([f"- {field}" for field in fields])
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output", help="Optional output file. Defaults to stdout.")
    args = parser.parse_args()

    data = load_manifest()
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else to_markdown(data) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
