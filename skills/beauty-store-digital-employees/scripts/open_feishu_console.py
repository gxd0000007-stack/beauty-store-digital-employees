#!/usr/bin/env python3
"""Open Feishu Open Platform pages and print the manual bot setup checklist."""
import argparse
import json
import webbrowser


PAGES = {
    "app-home": "https://open.feishu.cn/app",
    "bot-setup": "https://open.feishu.cn/app",
    "event-doc": "https://open.feishu.cn/document/server-docs/event-subscription-guide/event-subscription-configure-/request-url-configuration-case?lang=zh-CN",
    "receive-message-doc": "https://open.larksuite.com/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/receive",
}


CHECKLIST = [
    "创建或选择企业自建应用：运营总助 Agent",
    "启用机器人能力",
    "开通 IM 接收消息和发送消息权限",
    "事件订阅选择长连接 / WebSocket",
    "订阅 im.message.receive_v1",
    "创建并发布新版本，等待生效",
    "把机器人加入单聊或测试群",
    "复制 App ID；App Secret 只输入到本地 bridge 提示，不写入文件或聊天",
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", choices=sorted(PAGES), default="bot-setup")
    parser.add_argument("--no-open", action="store_true", help="Only print URL and checklist.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    url = PAGES[args.page]
    opened = False
    if not args.no_open:
        opened = webbrowser.open(url)

    result = {
        "page": args.page,
        "url": url,
        "opened": opened,
        "manual_checklist": CHECKLIST,
        "writes_performed": False,
        "secrets_requested": False,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Feishu Open Platform:", url)
        print("Opened:", opened)
        print("Manual checklist:")
        for i, item in enumerate(CHECKLIST, 1):
            print(f"{i}. {item}")
        print("Writes performed: NO")
        print("Secrets requested: NO")


if __name__ == "__main__":
    main()
