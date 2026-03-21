#!/usr/bin/env python3
"""
list_user_prompts.py
列出会话中的所有用户提问

用法: python list_user_prompts.py <session-log-file>
示例: python list_user_prompts.py ~/.claude/projects/D--git-proj-bullet3/4676cf56-a6b2-4e98-a748-4e08e5260daa.jsonl

输出格式: index|uuid|timestamp|content-preview
"""

import json
import sys
from pathlib import Path


def extract_user_prompts(log_file):
    """提取所有用户提问"""
    prompts = []

    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            if record.get('type') != 'user':
                continue

            uuid = record.get('uuid', '')
            timestamp = record.get('timestamp', '')

            # 提取 content
            message = record.get('message', {})
            content = message.get('content', '') if isinstance(message, dict) else ''

            # 取前 200 字符作为预览
            preview = content[:200].replace('\n', ' ') if content else ''
            if len(content) > 200:
                preview += '...'

            prompts.append({
                'uuid': uuid,
                'timestamp': timestamp,
                'preview': preview
            })

    return prompts


def main():
    if len(sys.argv) < 2:
        print(f"用法: python {sys.argv[0]} <session-log-file>")
        print(f"示例: python {sys.argv[0]} ~/.claude/projects/D--git-proj-bullet3/4676cf56-a6b2-4e98-a748-4e08e5260daa.jsonl")
        sys.exit(1)

    log_file = sys.argv[1]

    if not Path(log_file).exists():
        print(f"错误: 文件不存在: {log_file}")
        sys.exit(1)

    prompts = extract_user_prompts(log_file)

    for idx, prompt in enumerate(prompts):
        print(f"{idx}|{prompt['uuid']}|{prompt['timestamp']}|{prompt['preview']}")


if __name__ == '__main__':
    main()
