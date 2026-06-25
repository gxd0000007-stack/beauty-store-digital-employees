# 门店表格管理系统｜一张表管公司

公开 GitHub 产品包，用于让学员在 Codex 对话框里初始化一套飞书上的美业门店表格管理系统，并按阶段接入数字员工 BOT。

## Codex 对话框安装

把下面这一句粘贴到 Codex 对话框：

```text
$skill-installer install https://github.com/gxd0000007-stack/beauty-store-digital-employees/tree/main/skills/beauty-store-digital-employees
```

安装后继续粘贴：

```text
使用 $beauty-store-digital-employees。
目标：在我的飞书里预览并初始化「门店表格管理系统｜一张表管公司」。
先检查环境和授权，只展示会创建什么，不要直接写飞书。
```

## 这个包会做什么

- 创建老板看的 Base：`门店表格管理系统｜一张表管公司`。
- 创建员工资料/备份文件夹：`美业门店数字员工资料与备份`。
- 保留数字员工控制层：客户主表、回访、复购、客诉、财务、经营分析、知识沉淀、写入日志等表。
- 先跑通 `运营总助 Agent`，拿到 `BOT_OK`。
- `BOT_OK` 后可一次性规划 7 个员工 BOT。
- 可生成 macOS `launchd` 长期在线配置预览。

## 不会做什么

- 不复制维护者真实多维表格 token。
- 不复制真实顾客、财务、测试记录或截图。
- 不把 App Secret 写进文件、文档、Base 或聊天记录。
- 不默认适配学员已有飞书结构。
- 不在未确认时写入真实飞书对象。

## 安装阶段

1. 环境授权：检查 `lark-cli`、飞书授权、Node.js、Codex CLI、`lark-channel-bridge`。
2. 老板 Base：预览并创建 `门店表格管理系统｜一张表管公司` 空结构。
3. 员工资料区：预览并创建 `美业门店数字员工资料与备份` 文件夹骨架。
4. `BOT_OK`：配置并验证 `运营总助 Agent`。
5. `7_BOTS_OK`：高级路径，一次性规划 7 个员工 BOT。
6. 长期在线：生成 launchd plist 预览，确认后再安装。

## 本地验证

```bash
python3 skills/beauty-store-digital-employees/scripts/validate_package.py skills/beauty-store-digital-employees
python3 skills/beauty-store-digital-employees/scripts/build_manifest.py --format json
python3 skills/beauty-store-digital-employees/scripts/setup_all_employee_bots.py --mode all-seven --format json
python3 skills/beauty-store-digital-employees/scripts/install_bot_daemons.py --mode all-seven --dry-run --format json
```

期望输出：

```text
PACKAGE OK
SYSTEM_OK
BOT_OK
7_BOTS_OK
```
