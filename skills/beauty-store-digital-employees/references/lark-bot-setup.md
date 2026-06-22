# Lark Bot Setup

Use this reference when the learner needs Feishu chat replies after installing the standard business system.

## Position

Bot reply is a separate acceptance stage from standard Base/doc/task creation.

- `SYSTEM_OK`: standard Feishu business system exists.
- `BOT_OK`: `运营总助 Agent` can receive a Feishu message and reply through local Codex via `lark-channel-bridge`.

Do not treat `SYSTEM_OK` as proof that bot reply works.

## First-Version Scope

Start with one bot:

- App name: `运营总助 Agent`
- Profile: `store-ops-lead`
- Agent: `codex`
- Workspace: the learner's local project folder

Do not default to 7 bots in the training first path. Add the other six bots only after `运营总助 Agent` is stable.

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
