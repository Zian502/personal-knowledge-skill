#!/usr/bin/env python3
"""Export the active Agent conversation into a normalized, temporary source file.

The host Agent owns access to its live conversation. This adapter intentionally
does not scrape application databases or browser storage. Instead it calls a
user-configured host-native exporter, or normalizes an explicit JSON/text export.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def fail(message: str) -> "NoReturn":
    print(f"错误：{message}", file=sys.stderr)
    raise SystemExit(2)


def exporter_command(agent: str) -> str | None:
    names = ["PKS_CONVERSATION_EXPORT_CMD"]
    if agent in {"auto", "codex"}:
        names.extend(["PKS_CODEX_CONVERSATION_EXPORT_CMD", "CODEX_CONVERSATION_EXPORT_CMD"])
    if agent in {"auto", "cursor"}:
        names.extend(["PKS_CURSOR_CONVERSATION_EXPORT_CMD", "CURSOR_CONVERSATION_EXPORT_CMD"])
    for name in names:
        if command := os.environ.get(name, "").strip():
            return command
    return None


def text_content(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        pieces: list[str] = []
        for item in content:
            if isinstance(item, str):
                pieces.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                pieces.append(item["text"])
        return "\n".join(piece.strip() for piece in pieces if piece.strip())
    return ""


def normalize(raw: str, agent: str) -> str:
    """Keep only user and assistant messages from a JSON or plain-text export."""
    try:
        document = json.loads(raw)
    except json.JSONDecodeError:
        return raw.strip()

    messages = document.get("messages") if isinstance(document, dict) else document
    if not isinstance(messages, list):
        fail("导出内容必须是纯文本，或包含 messages 数组的 JSON")

    sections = [f"# 当前会话导出（{agent}）", ""]
    count = 0
    for message in messages:
        if not isinstance(message, dict):
            continue
        role = str(message.get("role", "")).lower()
        if role not in {"user", "assistant"}:
            continue
        content = text_content(message.get("content", message.get("text", "")))
        if not content:
            continue
        label = "用户" if role == "user" else "助手"
        sections.extend([f"## {label}", "", content, ""])
        count += 1
    if not count:
        fail("导出中没有可用的 user 或 assistant 消息")
    return "\n".join(sections).strip()


def read_source(args: argparse.Namespace) -> str:
    if args.input:
        return Path(args.input).expanduser().read_text(encoding="utf-8")
    command = args.command or exporter_command(args.agent)
    if not command:
        fail(
            "当前 Agent 未提供会话导出器。请让 Agent 使用其原生会话读取能力，"
            "或设置 PKS_CONVERSATION_EXPORT_CMD 后重试。"
        )
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode:
        fail(f"会话导出器执行失败（退出码 {result.returncode}）：{result.stderr.strip()}")
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser(description="导出当前 Agent 会话为 PKS 临时知识源")
    parser.add_argument("--agent", choices=("auto", "codex", "cursor"), default="auto")
    parser.add_argument("--input", help="显式传入的纯文本或 JSON 会话导出文件")
    parser.add_argument("--command", help="可信的当前会话导出命令；其 stdout 为文本或 JSON")
    parser.add_argument("--output", required=True, help="临时规范化会话文件")
    args = parser.parse_args()

    content = normalize(read_source(args), args.agent)
    if not content:
        fail("会话导出为空")
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
