#!/usr/bin/env python3
"""Check local readiness for Feishu-backed installation without writing data."""
import argparse
import json
import os
import shutil
import subprocess
import sys


DEFAULT_LARK_CLI = "/Users/gouxiaodong/.local/bin/lark-cli"


def find_lark_cli(explicit=None):
    if explicit:
        return explicit
    if os.environ.get("LARK_CLI"):
        return os.environ["LARK_CLI"]
    if os.path.isfile(DEFAULT_LARK_CLI):
        return DEFAULT_LARK_CLI
    return shutil.which("lark-cli")


def run_auth_status(lark_cli):
    if not lark_cli or not os.path.exists(lark_cli):
        return {
            "ok": False,
            "exit_code": None,
            "stdout": "",
            "stderr": "lark-cli not found",
        }
    proc = subprocess.run(
        [lark_cli, "auth", "status"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
    )
    return {
        "ok": proc.returncode == 0,
        "exit_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lark-cli", help="Path to lark-cli. Defaults to LARK_CLI, known local path, or PATH lookup.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    lark_cli = find_lark_cli(args.lark_cli)
    auth = run_auth_status(lark_cli)
    result = {
        "ok": bool(lark_cli and os.path.exists(lark_cli) and auth["ok"]),
        "checks": {
            "python": {
                "ok": sys.version_info >= (3, 9),
                "version": sys.version.split()[0],
            },
            "lark_cli": {
                "ok": bool(lark_cli and os.path.exists(lark_cli)),
                "path": lark_cli,
            },
            "lark_auth": auth,
        },
        "writes_performed": False,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Feishu install doctor")
        print(" - python:", "OK" if result["checks"]["python"]["ok"] else "FAIL", result["checks"]["python"]["version"])
        print(" - lark-cli:", "OK" if result["checks"]["lark_cli"]["ok"] else "FAIL", result["checks"]["lark_cli"]["path"])
        print(" - auth status:", "OK" if result["checks"]["lark_auth"]["ok"] else "FAIL")
        if auth["stdout"]:
            print(auth["stdout"])
        if auth["stderr"]:
            print(auth["stderr"])
        print(" - writes performed: NO")

    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
