#!/usr/bin/env python3
"""Generate the standard beauty store digital employee install manifest."""
import argparse
import json
import sys
from datetime import datetime, timezone


EMPLOYEES = ["运营总助", "回访专员", "复购顾问", "客诉专员", "财务管家", "经营分析预警官", "知识官"]


def manifest():
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
    return {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "install_strategy": "create_new_standard_feishu_business_system",
        "adapt_existing_workspace": False,
        "real_write_requires_confirmation": True,
        "root_folder": "美业门店数字员工系统-v1",
        "base": {
            "name": "美业门店数字员工系统-v1",
            "tables": [{"name": name, "fields": fields} for name, fields in tables],
        },
        "docs": [
            "00-系统总览与使用说明",
            "01-7个数字员工职责说明",
            "02-客户管理与财务SOP",
            "03-经营分析周报模板",
            "04-知识库/话术库",
            "04-知识库/案例库",
            "04-知识库/SOP库",
            "04-知识库/失败复盘库",
        ],
        "task_queues": ["回访任务", "复购跟进", "客诉处理", "财务核对", "经营分析", "知识沉淀"],
        "calendar_events": ["每周经营复盘", "每月财务核对"],
        "im_templates": ["客户回访确认", "复购跟进提醒", "客诉安抚草稿", "老板审批提醒"],
        "employees": EMPLOYEES,
        "bot_reply_setup": {
            "enabled": True,
            "first_bot_only": True,
            "first_employee": "运营总助",
            "first_profile": "store-ops-lead",
            "runtime": "lark-channel-bridge",
            "manual_feishu_console_required": True,
            "required_event": "im.message.receive_v1",
            "event_mode": "long_connection_websocket",
            "acceptance": ["SYSTEM_OK", "BOT_OK"],
        },
        "authorization_levels": {
            "L0": "diagnose_only",
            "L1": "initial_standard_structure_write",
            "L2": "customer_record_write",
            "L3": "im_send_or_group_send",
            "L4": "finance_or_complaint_compensation_write",
            "L5": "delete_batch_overwrite_privacy_export_closed_by_default",
        },
    }


def to_markdown(data):
    lines = [
        f"# {data['base']['name']} 安装清单",
        "",
        f"- 安装策略: `{data['install_strategy']}`",
        f"- 适配已有空间: `{data['adapt_existing_workspace']}`",
        f"- 真实写入需确认: `{data['real_write_requires_confirmation']}`",
        f"- 根目录: {data['root_folder']}",
        "",
        "## Base Tables",
        "",
    ]
    for table in data["base"]["tables"]:
        lines.append(f"### {table['name']}")
        lines.append("")
        lines.append(", ".join(table["fields"]))
        lines.append("")
    lines.extend(["## Docs", ""])
    lines.extend([f"- {name}" for name in data["docs"]])
    lines.extend(["", "## Digital Employees", ""])
    lines.extend([f"- {name}" for name in data["employees"]])
    lines.extend(["", "## Bot Reply Setup", ""])
    bot = data["bot_reply_setup"]
    lines.extend([
        f"- Runtime: `{bot['runtime']}`",
        f"- First bot: {bot['first_employee']} / `{bot['first_profile']}`",
        f"- Required event: `{bot['required_event']}`",
        f"- Event mode: `{bot['event_mode']}`",
        f"- Acceptance: {', '.join(bot['acceptance'])}",
    ])
    return "\n".join(lines) + "\n"


def main():
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


if __name__ == "__main__":
    main()
