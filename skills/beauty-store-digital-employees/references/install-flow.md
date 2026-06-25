# Install Flow

This package installs a Feishu-based beauty store operating system in four stages.

## Stage 0: Environment Authorization

Goal: prove the learner's machine and Feishu account can support the install.

Run:

```bash
python3 <skill-dir>/scripts/doctor.py --json
python3 <skill-dir>/scripts/bot_doctor.py --json
python3 <skill-dir>/scripts/build_manifest.py --format markdown
```

Check:

- `lark-cli` exists.
- Feishu user identity is ready.
- Base, Drive, Docs, IM scopes are present or the user is told what authorization is missing.
- Node.js and `lark-channel-bridge` are ready for BOT OK.

Do not write any Feishu object in this stage.

## Stage 1: Create Boss System

Goal: create a new empty owner-facing Base named:

`门店表格管理系统｜一张表管公司`

Use:

```bash
python3 <skill-dir>/scripts/build_boss_base_manifest.py --format markdown
```

Before writing, show a preview and ask the user to confirm:

`我确认创建门店表格管理系统｜一张表管公司。`

Create only the structure:

- native folders
- tables
- fields
- dashboards
- homepage blocks
- quick entries

Do not import real records.

## Stage 2: Create Employee Assets Folder

Goal: create the backstage folder skeleton:

`美业门店数字员工资料与备份`

Use:

```bash
python3 <skill-dir>/scripts/build_employee_folder_manifest.py --format markdown
```

Before writing, show the folder list and ask for confirmation.

## Stage 3: BOT OK

Goal: make at least one bot reply in Feishu.

Default path:

1. Configure `运营总助 Agent`.
2. Run `bot_smoke_test.py`.
3. User sends a Feishu message to the bot.
4. The bot replies and identifies its role.

Acceptance token: `BOT_OK`.

## Stage 4: 7_BOTS_OK

Advanced path after `BOT_OK`:

```bash
python3 <skill-dir>/scripts/setup_all_employee_bots.py --format markdown
python3 <skill-dir>/scripts/install_bot_daemons.py --mode all-seven --dry-run
python3 <skill-dir>/scripts/bot_status.py --mode all-seven --json
```

Acceptance token: `7_BOTS_OK`.

Do not enable all seven bots silently. Each Feishu app still requires manual App ID, local App Secret input, bot ability, event subscription, and version publish.
