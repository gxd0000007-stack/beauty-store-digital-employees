# Write Policy

Use this reference before any real write to a learner's Feishu workspace.

## Authorization Levels

| Level | Scope | Default |
| --- | --- | --- |
| L0 | Diagnose auth and environment only | Always allowed |
| L1 | Create standard docs, folders, empty Base tables, tasks, calendar review events | Allowed after initial confirmation |
| L2 | Create or modify real customer records and customer tasks | Confirm each batch |
| L3 | Send IM messages or group messages | Preview and confirm every send |
| L4 | Finance records, card/session balances, refunds, complaint compensation records | Confirm exact data and owner approval |
| L5 | Delete, batch overwrite, privacy export, production automation | Closed by default |

## Confirmation Rules

For L1 initial creation, require a sentence equivalent to:

`我确认在我的飞书里创建门店表格管理系统｜一张表管公司。`

For L2-L4, require a preview containing:

- Target object: doc, Base, table, record, task, calendar, or chat.
- Exact affected rows, customers, dates, amounts, or recipients.
- Risk level.
- Whether the action can be undone manually.
- Local log destination.

If the user has not confirmed the specific action, reply:

`BLOCKED: waiting for write confirmation`

## Hard Stops

Do not proceed silently when the action includes:

- Group send or customer-facing message.
- Real customer privacy export.
- Real money, refund, card balance, session count, or compensation.
- Base field/schema change after initial standard creation.
- Delete, batch overwrite, or irreversible update.
- App secret, token, cookie, private key, or credential storage.

## Logging

After any confirmed write, write a local record with:

- timestamp
- Feishu tenant/profile if visible
- action type
- risk level
- confirmation text summary
- created or updated object IDs/URLs
- success or failure

Do not log secrets or raw customer exports.
