#!/usr/bin/env python3
"""Render the employee assets and backup folder template manifest."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = PACKAGE_ROOT / "manifests" / "employee-folder-template.json"


def load_manifest() -> dict:
    with TEMPLATE_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def to_markdown(data: dict) -> str:
    lines = [
        f"# {data['template_name']} 文件夹模板",
        "",
        f"- 模板角色: `{data['template_role']}`",
        f"- 安装模式: `{data['install_mode']}`",
        f"- 复制真实文件: `{data['copy_real_files']}`",
        f"- 保存密钥: `{data['store_secrets']}`",
        f"- 数字员工: {', '.join(data['employees'])}",
        "",
        "## 文件夹结构",
        "",
    ]
    for folder in data["folders"]:
        lines.append(f"### {folder['name']}")
        lines.append("")
        lines.extend([f"- {doc}" for doc in folder["docs"]])
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
