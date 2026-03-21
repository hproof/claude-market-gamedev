#!/usr/bin/env python3
"""
find_and_list_prompts.py
自动找到最新的会话日志，并列出所有用户提问

用法: python find_and_list_prompts.py <project-log-dir>
输出: 每行一个用户提问，格式: session-file|line-num|uuid|timestamp|content-preview
"""

import json
import sys
from pathlib import Path


def find_latest_session_log(project_dir):
    """找到最新的 .jsonl 会话日志文件"""
    project_path = Path(project_dir)
    if not project_path.exists():
        return None

    jsonl_files = list(project_path.glob("*.jsonl"))
    if not jsonl_files:
        return None

    # 按修改时间排序，取最新的
    latest = max(jsonl_files, key=lambda f: f.stat().st_mtime)
    return latest


def extract_user_prompts(log_file):
    """提取所有用户提问"""
    prompts = []
    with open(log_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if record.get('type') == 'user':
                    uuid = record.get('uuid', '')
                    timestamp = record.get('timestamp', '')
                    message = record.get('message', {})
                    content = message.get('content', '') if isinstance(message, dict) else ''
                    # 取前 100 字作为预览
                    preview = content[:100].replace('\n', ' ') if content else ''
                    if len(content) > 100:
                        preview += '...'
                    prompts.append({
                        'line_num': line_num,
                        'uuid': uuid,
                        'timestamp': timestamp,
                        'preview': preview
                    })
            except json.JSONDecodeError:
                continue
    return prompts


def main():
    if len(sys.argv) < 2:
        print(f"用法: python {sys.argv[0]} <project-log-dir>", file=sys.stderr)
        print(f"示例: python {sys.argv[0]} ~/.claude/projects/D--git-proj-bullet3", file=sys.stderr)
        sys.exit(1)

    project_dir = Path(sys.argv[1])

    # 1. 找到最新的会话日志
    latest_log = find_latest_session_log(project_dir)
    if not latest_log:
        print(f"错误: 在 {project_dir} 中找不到会话日志文件", file=sys.stderr)
        sys.exit(1)

    # 2. 提取所有用户提问
    prompts = extract_user_prompts(latest_log)

    # 3. 输出格式: session-file|line-num|uuid|timestamp|preview
    session_name = latest_log.name
    for prompt in prompts:
        print(f"{session_name}|{prompt['line_num']}|{prompt['uuid']}|{prompt['timestamp']}|{prompt['preview']}")


if __name__ == '__main__':
    main()
