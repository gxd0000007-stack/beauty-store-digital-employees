# 美业门店数字员工系统

公开 GitHub 产品包，用于让学员在 Codex 对话框里安装一套标准美业门店数字员工系统，并接入自己的飞书。

## Codex 对话框安装

把下面这一句粘贴到 Codex 对话框：

```text
$skill-installer install https://github.com/gxd0000007-stack/beauty-store-digital-employees/tree/main/skills/beauty-store-digital-employees
```

安装后继续粘贴：

```text
使用 $beauty-store-digital-employees，先检查环境，不要直接写飞书。我要在自己的飞书里新建标准美业门店数字员工系统，并配置运营总助 Agent 能回消息。
```

## 第一版会做什么

- 在学员自己的飞书里新建标准业务系统。
- 默认不适配已有飞书结构。
- 创建客户主表、回访、复购、客诉、财务、经营分析、知识库和写入日志等标准表。
- 支持文档、Base、任务、日历、IM 写入。
- 真实写入前必须预览和确认。
- 机器人回消息阶段先只配置 `运营总助 Agent`。

## 飞书机器人回消息

机器人回消息使用 `lark-channel-bridge`。

流程：

1. Codex 检查 Node.js、Codex CLI、`lark-channel-bridge`。
2. Codex 打开飞书开放平台页面。
3. 学员手动创建或配置 `运营总助 Agent`。
4. 学员启用机器人能力、添加 IM 权限、订阅 `im.message.receive_v1`、选择长连接、发布版本。
5. Codex 生成 bridge profile 命令。
6. 学员只把 App Secret 输入到本地 bridge 提示，不写入任何文件或聊天。
7. 飞书里给机器人发消息，确认能收到回复。

## 安全边界

以下动作必须预览和确认：

- 群发消息
- 修改真实客户资料
- 写财务记录
- 处理客诉赔付
- 修改 Base 字段结构
- 批量更新

以下动作第一版默认关闭：

- 删除数据
- 批量覆盖
- 隐私导出
- 自动生产发布

## 验收

本地包验证：

```bash
python3 skills/beauty-store-digital-employees/scripts/validate_package.py skills/beauty-store-digital-employees
```

标准系统验收：

```text
SYSTEM_OK
```

机器人回消息验收：

```text
BOT_OK
```
