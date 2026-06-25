#!/usr/bin/env python3
"""Generate the beauty store table-management package manifest."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_NAME = "门店表格管理系统｜一张表管公司"

EMPLOYEE_PROFILES = [
    {"employee": "运营总助", "app_name": "运营总助 Agent", "profile": "store-ops-lead", "default_stage": "BOT_OK"},
    {"employee": "回访专员", "app_name": "回访专员 Agent", "profile": "store-follow-up-specialist", "default_stage": "7_BOTS_OK"},
    {"employee": "复购顾问", "app_name": "复购顾问 Agent", "profile": "store-repurchase-advisor", "default_stage": "7_BOTS_OK"},
    {"employee": "客诉专员", "app_name": "客诉专员 Agent", "profile": "store-complaint-specialist", "default_stage": "7_BOTS_OK"},
    {"employee": "财务管家", "app_name": "财务管家 Agent", "profile": "store-finance-steward", "default_stage": "7_BOTS_OK"},
    {"employee": "经营分析预警官", "app_name": "经营分析预警官 Agent", "profile": "store-business-alert-analyst", "default_stage": "7_BOTS_OK"},
    {"employee": "知识官", "app_name": "知识官 Agent", "profile": "store-knowledge-officer", "default_stage": "7_BOTS_OK"},
]


def load_template(name: str) -> dict:
    path = PACKAGE_ROOT / "manifests" / name
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def digital_employee_tables() -> list[dict]:
    tables = [
        ("客户主表", ["客户ID", "姓名", "手机号", "性别", "生日", "来源渠道", "首次到店日期", "最近到店日期", "客户状态", "价值分层", "标签", "累计消费金额", "卡金余额", "疗程剩余", "负责顾问", "备注"]),
        ("回访任务表", ["任务ID", "关联客户", "回访节点", "负责数字员工", "状态", "优先级", "截止时间", "话术草稿", "回访结果", "风险信号"]),
        ("复购机会表", ["机会ID", "关联客户", "机会类型", "意向强度", "推荐方向", "跟进话术", "报价/优惠状态", "状态"]),
        ("客诉处理表", ["客诉ID", "关联客户", "客诉等级", "客诉类型", "事实摘要", "证据清单", "安抚话术", "处理建议", "赔付/退款状态", "状态"]),
        ("财务记录表", ["记录ID", "关联客户", "记录类型", "金额", "发生日期", "经办人", "来源单据", "核对状态", "备注"]),
        ("卡金与疗程表", ["记录ID", "关联客户", "类型", "项目名称", "初始金额/次数", "剩余金额/次数", "有效期", "状态"]),
        ("经营分析指标表", ["指标ID", "周期", "指标类型", "指标值", "口径说明", "预警等级", "分析结论"]),
        ("知识沉淀表", ["知识ID", "类型", "标题", "适用场景", "正文", "来源", "状态"]),
        ("写入日志与确认表", ["日志ID", "动作类型", "风险等级", "预览摘要", "确认人", "确认时间", "执行状态", "结果链接"]),
    ]
    return [{"name": name, "fields": fields} for name, fields in tables]


def manifest() -> dict:
    boss_base_template = load_template("boss-base-template.json")
    employee_assets_template = load_template("employee-folder-template.json")
    return {
        "schema_version": "2.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "package_name": "beauty-store-digital-employees",
        "product_name": PRODUCT_NAME,
        "install_strategy": "create_new_boss_base_and_employee_assets",
        "default_install_mode": "preview_then_create_empty_templates",
        "adapt_existing_workspace": False,
        "real_write_requires_confirmation": True,
        "store_real_tokens": False,
        "copy_real_records": False,
        "root_objects": [
            {"type": "base", "name": PRODUCT_NAME, "role": "owner_facing_boss_dashboard"},
            {"type": "drive_folder", "name": employee_assets_template["template_name"], "role": "backstage_employee_assets_and_backup"},
        ],
        "boss_base_template": boss_base_template,
        "employee_assets_template": employee_assets_template,
        "digital_employee_control_tables": digital_employee_tables(),
        "bot_reply_setup": {
            "enabled": True,
            "runtime": "lark-channel-bridge",
            "manual_feishu_console_required": True,
            "required_event": "im.message.receive_v1",
            "event_mode": "long_connection_websocket",
            "default_path": "first_bot_only",
            "first_employee": "运营总助",
            "first_profile": "store-ops-lead",
            "all_seven_supported": True,
            "profiles": EMPLOYEE_PROFILES,
            "acceptance": ["SYSTEM_OK", "BOT_OK", "7_BOTS_OK"],
        },
        "daemon_setup": {
            "enabled": True,
            "platform": "macos_launchd",
            "script": "scripts/install_bot_daemons.py",
            "default_mode": "first-bot",
            "advanced_mode": "all-seven",
            "no_secrets_in_plist": True,
        },
        "authorization_levels": {
            "L0": "diagnose_only",
            "L1": "initial_structure_write_after_confirmation",
            "L2": "customer_record_write",
            "L3": "im_send_or_group_send",
            "L4": "finance_or_complaint_compensation_write",
            "L5": "delete_batch_overwrite_privacy_export_closed_by_default",
        },
        "reference_files": [
            "references/install-flow.md",
            "references/boss-dashboard-template.md",
            "references/employee-assets-folder.md",
            "references/all-seven-bots.md",
            "references/long-running-daemons.md",
            "references/write-policy.md",
        ],
    }


def to_markdown(data: dict) -> str:
    boss = data["boss_base_template"]
    folder = data["employee_assets_template"]
    bot = data["bot_reply_setup"]
    lines = [
        f"# {data['product_name']} 安装清单",
        "",
        f"- 安装策略: `{data['install_strategy']}`",
        f"- 默认模式: `{data['default_install_mode']}`",
        f"- 适配已有空间: `{data['adapt_existing_workspace']}`",
        f"- 复制真实记录: `{data['copy_real_records']}`",
        f"- 保存真实 token: `{data['store_real_tokens']}`",
        f"- 真实写入需确认: `{data['real_write_requires_confirmation']}`",
        "",
        "## 老板 Base",
        "",
        f"- 名称: {boss['template_name']}",
        f"- 角色: `{boss['template_role']}`",
        f"- 原生分组: {len(boss['native_folders'])} 个",
        f"- 首页快捷入口: {len(boss['homepage']['quick_entries'])} 个",
        "",
        "## 员工资料与备份",
        "",
        f"- 名称: {folder['template_name']}",
        f"- 文件夹: {len(folder['folders'])} 个",
        f"- 数字员工: {', '.join(folder['employees'])}",
        "",
        "## 数字员工 BOT",
        "",
        f"- Runtime: `{bot['runtime']}`",
        f"- 默认首个 BOT: {bot['first_employee']} / `{bot['first_profile']}`",
        f"- 支持一次性规划 7 个 BOT: `{bot['all_seven_supported']}`",
        f"- Acceptance: {', '.join(bot['acceptance'])}",
        "",
        "## 长期在线",
        "",
        f"- 平台: `{data['daemon_setup']['platform']}`",
        f"- 默认模式: `{data['daemon_setup']['default_mode']}`",
        f"- 高级模式: `{data['daemon_setup']['advanced_mode']}`",
        "",
        "## 员工控制表",
        "",
    ]
    for table in data["digital_employee_control_tables"]:
        lines.append(f"- {table['name']}: {', '.join(table['fields'])}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output", help="Optional output file. Defaults to stdout.")
    args = parser.parse_args()

    data = manifest()
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else to_markdown(data)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
