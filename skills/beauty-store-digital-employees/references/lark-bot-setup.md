# Lark Bot Setup

Use this reference when the learner needs Feishu chat replies after installing the standard business system.

## Position

Bot reply is a separate acceptance stage from standard Base/doc/task creation.

- `SYSTEM_OK`: standard Feishu business system exists.
- `BOT_OK`: `运营总助 Agent` can receive a Feishu message and reply through local Codex via `lark-channel-bridge`.
- `7_BOTS_OK`: all seven digital employee bot profiles are configured and reachable after `BOT_OK`.

Do not treat `SYSTEM_OK` as proof that bot reply works.

## First-Version Scope

Start with one bot:

- App name: `运营总助 Agent`
- Profile: `store-ops-lead`
- Agent: `codex`
- Workspace: the learner's local project folder

Do not default to 7 bots in the training first path. Add the other six bots only after `运营总助 Agent` is stable.

Advanced all-seven app names:

| Employee | App name | Profile |
| --- | --- | --- |
| 运营总助 | 运营总助 Agent | store-ops-lead |
| 回访专员 | 回访专员 Agent | store-follow-up-specialist |
| 复购顾问 | 复购顾问 Agent | store-repurchase-advisor |
| 客诉专员 | 客诉专员 Agent | store-complaint-specialist |
| 财务管家 | 财务管家 Agent | store-finance-steward |
| 经营分析预警官 | 经营分析预警官 Agent | store-business-alert-analyst |
| 知识官 | 知识官 Agent | store-knowledge-officer |

## Manual Feishu Open Platform Steps

The package can open the relevant pages and show instructions, but the learner must manually complete the Feishu console steps.

1. Open Feishu Open Platform: `https://open.feishu.cn/app`
2. Create or select an enterprise self-built app.
3. Name it `运营总助 Agent`.
4. Enable bot ability.
5. Open permissions and add minimum IM scopes for receiving and sending messages.
6. Open events and callbacks.
7. Choose long connection / WebSocket receiving mode.
8. Subscribe to `im.message.receive_v1`.
9. Publish a new app version and wait until the changes are effective.
10. Add the bot to a direct chat or a training test group.
11. Copy the `App ID`. Keep `App Secret` private and enter it only into the local bridge prompt.

For the all-seven path, repeat these steps for each employee app. The package can generate commands, but each app still needs manual Feishu console setup and publish.

## Required Manual Confirmation

Before starting the bridge, ask the learner to confirm:

- Bot ability is enabled.
- `im.message.receive_v1` is subscribed.
- The app version has been published.
- The bot is available in Feishu chat.
- App Secret will not be pasted into repository files, docs, Base records, or chat logs.

## Troubleshooting Signals

If the WebSocket connection starts but no message arrives:

- Confirm the app version was published after adding event subscriptions.
- Confirm `im.message.receive_v1` is present in events.
- Confirm bot ability is enabled.
- Confirm the learner is messaging the correct bot.
- Confirm group chats mention the bot if the bridge requires mention-triggered group messages.
- Confirm the bridge daemon is running for the expected profile.

## Long-Running Setup

After a profile works, use:

```bash
python3 <skill-dir>/scripts/install_bot_daemons.py --mode first-bot --dry-run --format markdown
```

Only install launchd plists after the learner has reviewed the preview. The script writes plist files only when `--output-dir` or `--install` is used, and it does not run `launchctl` automatically.
