# All Seven Bots

This package supports a staged path:

1. Default: configure and verify one bot, `运营总助 Agent`.
2. Advanced: generate the full setup checklist for all seven bots.

## Employees

| Employee | App name | Profile | Wrapper directory | Daemon label |
| --- | --- | --- | --- | --- |
| 运营总助 | 运营总助 Agent | store-ops-lead | wrappers/运营总助 | ai.lark-channel-bridge.bot.store-ops-lead |
| 回访专员 | 回访专员 Agent | store-follow-up-specialist | wrappers/回访专员 | ai.lark-channel-bridge.bot.store-follow-up-specialist |
| 复购顾问 | 复购顾问 Agent | store-repurchase-advisor | wrappers/复购顾问 | ai.lark-channel-bridge.bot.store-repurchase-advisor |
| 客诉专员 | 客诉专员 Agent | store-complaint-specialist | wrappers/客诉专员 | ai.lark-channel-bridge.bot.store-complaint-specialist |
| 财务管家 | 财务管家 Agent | store-finance-steward | wrappers/财务管家 | ai.lark-channel-bridge.bot.store-finance-steward |
| 经营分析预警官 | 经营分析预警官 Agent | store-business-alert-analyst | wrappers/经营分析预警官 | ai.lark-channel-bridge.bot.store-business-alert-analyst |
| 知识官 | 知识官 Agent | store-knowledge-officer | wrappers/知识官 | ai.lark-channel-bridge.bot.store-knowledge-officer |

## Manual Feishu Requirements Per Bot

Each bot needs:

- self-built Feishu app
- bot ability enabled
- IM message permission
- event subscription: `im.message.receive_v1`
- long connection mode
- published app version
- App ID recorded locally
- App Secret entered locally when `lark-channel-bridge` prompts

## Why One Bot First

One bot first reduces setup noise. It proves:

- Feishu app setup works
- bridge runtime works
- Codex CLI can be invoked
- role wrapper works
- local logs are readable

Only after `BOT_OK` should the learner expand to seven bots.

## Advanced Expansion

Use:

```bash
python3 <skill-dir>/scripts/setup_all_employee_bots.py --mode all-seven --format markdown
```

This script does not create Feishu apps. It creates a human-readable setup map, command checklist, wrapper targets, profile names, daemon labels, and smoke-test sequence.

Then preview long-running plists:

```bash
python3 <skill-dir>/scripts/install_bot_daemons.py --mode all-seven --dry-run --format markdown
```

Do not install all seven launchd services until each profile has been created locally and the user confirms the all-seven path.
