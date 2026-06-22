#!/usr/bin/env python3
"""Generate safe lark-channel-bridge commands for the first bot profile."""
import argparse
import json
import os
import shlex


PROFILE_BY_EMPLOYEE = {
    "运营总助": "store-ops-lead",
    "回访专员": "store-follow-up-specialist",
    "复购顾问": "store-repurchase-advisor",
    "客诉专员": "store-complaint-specialist",
    "财务管家": "store-finance-steward",
    "经营分析预警官": "store-business-alert-analyst",
    "知识官": "store-knowledge-officer",
}


def q(value):
    return shlex.quote(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-id", required=True, help="Feishu app_id, for example cli_xxx. Do not pass App Secret.")
    parser.add_argument("--workspace", default=os.getcwd(), help="Local project workspace for Codex.")
    parser.add_argument("--employee", choices=sorted(PROFILE_BY_EMPLOYEE), default="运营总助")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    profile = PROFILE_BY_EMPLOYEE[args.employee]
    workspace = os.path.abspath(args.workspace)
    create_cmd = " ".join([
        "lark-channel-bridge", "profile", "create", q(profile),
        "--agent", "codex",
        "--workspace", q(workspace),
        "--app-id", q(args.app_id),
    ])
    start_cmd = " ".join(["lark-channel-bridge", "start", "--profile", q(profile)])
    status_cmd = " ".join(["lark-channel-bridge", "status", "--profile", q(profile)])
    run_cmd = " ".join([
        "lark-channel-bridge", "run",
        "--profile", q(profile),
        "--agent", "codex",
        "--workspace", q(workspace),
        "--app-id", q(args.app_id),
    ])
    result = {
        "employee": args.employee,
        "profile": profile,
        "workspace": workspace,
        "app_id": args.app_id,
        "commands": {
            "foreground_debug": run_cmd,
            "create_profile": create_cmd,
            "start_daemon": start_cmd,
            "status": status_cmd,
        },
        "secret_policy": "Do not pass App Secret to this script. Enter it only into the local lark-channel-bridge prompt.",
        "writes_performed": False,
        "secrets_requested": False,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Bridge profile plan")
        print("Employee:", args.employee)
        print("Profile:", profile)
        print("Workspace:", workspace)
        print("")
        print("Foreground debug command:")
        print(run_cmd)
        print("")
        print("Create profile command:")
        print(create_cmd)
        print("")
        print("Start daemon command:")
        print(start_cmd)
        print("")
        print("Status command:")
        print(status_cmd)
        print("")
        print("Secret policy:", result["secret_policy"])
        print("Writes performed: NO")
        print("Secrets requested: NO")


if __name__ == "__main__":
    main()
