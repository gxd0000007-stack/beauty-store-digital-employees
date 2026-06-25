# Long Running Daemons

Codex chat windows should not be responsible for staying online. Long-running Feishu bot connections should be handled by local daemon services.

## Runtime Shape

```text
Feishu bot
  -> lark-channel-bridge WebSocket
  -> employee wrapper
  -> Codex CLI
  -> employee role.md
```

## Mac Default

Use `launchd`:

- `RunAtLoad=true`
- `KeepAlive=true`
- logs under `~/Library/Logs/beauty-store-digital-employees/`
- one plist per bot profile
- first-bot mode before all-seven mode

## Script Responsibilities

`install_bot_daemons.py` should:

- generate launchd plist previews
- support `--mode first-bot`
- support `--mode all-seven`
- preview by default when no `--output-dir` or `--install` is provided
- never write App Secret
- never run `launchctl` automatically
- optionally install plist files only after explicit user confirmation

`bot_status.py` should:

- check expected profiles
- call `lark-channel-bridge status --profile <profile>`
- print `BOT_OK` for first-bot status
- print `7_BOTS_OK` only when all seven are healthy

## Safety

Do not store credentials in plist files. Profiles should be created by `lark-channel-bridge` and should prompt locally for secrets when needed.
