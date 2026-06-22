#!/usr/bin/env python3
"""Check local readiness for Feishu bot replies without writing data or secrets."""
import argparse
import json
import shutil
import subprocess
import sys


def run(cmd, timeout=15):
    exe = shutil.which(cmd[0])
    if not exe:
        return {"ok": False, "path": None, "exit_code": None, "stdout": "", "stderr": "not found"}
    try:
        proc = subprocess.run([exe] + cmd[1:], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "path": exe,
            "exit_code": None,
            "stdout": (exc.stdout or "").strip() if isinstance(exc.stdout, str) else "",
            "stderr": "timed out after " + str(timeout) + "s",
        }
    return {
        "ok": proc.returncode == 0,
        "path": exe,
        "exit_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def node_version_ok(text):
    version = text.strip().lstrip("v")
    parts = version.split(".")
    try:
        major, minor = int(parts[0]), int(parts[1])
    except Exception:
        return False
    return major > 20 or (major == 20 and minor >= 12)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    node = run(["node", "--version"])
    npm = run(["npm", "--version"])
    codex = run(["codex", "--version"])
    bridge = run(["lark-channel-bridge", "--version"])
    result = {
        "ok": all([
            node["ok"] and node_version_ok(node["stdout"]),
            npm["ok"],
            codex["ok"],
            bridge["ok"],
        ]),
        "checks": {
            "node": {**node, "version_ok": node["ok"] and node_version_ok(node["stdout"])},
            "npm": npm,
            "codex": codex,
            "lark_channel_bridge": bridge,
        },
        "writes_performed": False,
        "secrets_requested": False,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Feishu bot doctor")
        for key, value in result["checks"].items():
            print(" -", key + ":", "OK" if value.get("ok") else "FAIL", value.get("stdout") or value.get("stderr"))
        print(" - writes performed: NO")
        print(" - secrets requested: NO")
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
