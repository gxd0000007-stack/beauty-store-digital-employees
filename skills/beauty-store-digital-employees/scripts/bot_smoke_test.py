#!/usr/bin/env python3
"""Check lark-channel-bridge profile status and print bot reply smoke-test instructions."""
import argparse
import json
import shutil
import subprocess


TEST_MESSAGE = "状态自检：你是谁？请用一句话说明你负责什么。"


def bridge_status(profile):
    exe = shutil.which("lark-channel-bridge")
    if not exe:
        return {"ok": False, "exit_code": None, "stdout": "", "stderr": "lark-channel-bridge not found"}
    proc = subprocess.run([exe, "status", "--profile", profile], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
    return {
        "ok": proc.returncode == 0,
        "exit_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="store-ops-lead")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    status = bridge_status(args.profile)
    result = {
        "profile": args.profile,
        "local_status_ok": status["ok"],
        "status": status,
        "manual_feishu_test_message": TEST_MESSAGE,
        "acceptance": [
            "Feishu receives a reply from the correct bot.",
            "Reply identifies 运营总助.",
            "Reply does not promise high-risk automatic actions.",
        ],
        "writes_performed": False,
        "secrets_requested": False,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Profile:", args.profile)
        print("Local status:", "OK" if status["ok"] else "FAIL")
        if status["stdout"]:
            print(status["stdout"])
        if status["stderr"]:
            print(status["stderr"])
        print("")
        print("Send this message to the Feishu bot:")
        print(TEST_MESSAGE)
        print("")
        print("Acceptance:")
        for item in result["acceptance"]:
            print(" -", item)
        print("Writes performed: NO")
        print("Secrets requested: NO")
    return 0 if status["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
