#!/usr/bin/env python3
"""
find_and_list_prompts.py
列出指定会话日志中的所有用户提问

用法: python find_and_list_prompts.py <session-id>
输出: 每行一个用户提问，格式: timestamp|content-preview|uuid
"""

import json
import os
import sys
from pathlib import Path


def get_cwd():
    """获取当前工作目录"""
    return os.environ.get('PWD', os.getcwd())


def encode_path(cwd):
    """将当前工作目录编码为日志目录名"""
    import re
    encoded = re.sub(r'[:\\/_]', '-', cwd)
    return encoded


def get_log_dir(cwd):
    """根据当前目录获取日志目录"""
    encoded = encode_path(cwd)
    home = Path.home()
    log_dir = home / '.claude' / 'projects' / encoded
    return log_dir


def is_real_user_input(record):
    """判断是否是真正的用户输入（排除系统消息和工具结果）"""
    message = record.get('message', {})
    content = message.get('content', '') if isinstance(message, dict) else ''

    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get('type') in ('tool_result', 'tool_use'):
                return False
        return True

    if not isinstance(content, str):
        return False

    content = content.strip()
    if content.startswith('<local-command-caveat>'):
        return False
    if content.startswith('<command-name>'):
        return False
    if content.startswith('<local-command-'):
        return False
    if content.startswith('<'):
        return False
    return True


def get_content_preview(record):
    """获取内容预览"""
    message = record.get('message', {})
    content = message.get('content', '') if isinstance(message, dict) else ''

    if isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict):
                if 'text' in item:
                    texts.append(item['text'])
                elif 'content' in item and isinstance(item['content'], str):
                    texts.append(item['content'])
            elif isinstance(item, str):
                texts.append(item)
        content = ' '.join(texts)

    return str(content) if content else ''


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
                    if not is_real_user_input(record):
                        continue

                    content = get_content_preview(record)
                    uuid = record.get('uuid', '')
                    timestamp = record.get('timestamp', '')
                    preview = content[:100].replace('\n', ' ')
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
        print(f"用法: python {sys.argv[0]} <session-id>", file=sys.stderr)
        print(f"示例: python {sys.argv[0]} xxx-xxx-xxxx-xxxx", file=sys.stderr)
        sys.exit(1)

    session_id = sys.argv[1]

    # 1. 获取当前工作目录
    cwd = get_cwd()

    # 2. 根据当前目录找到日志目录
    log_dir = get_log_dir(cwd)
    if not log_dir.exists():
        print(f"错误: 日志目录不存在: {log_dir}", file=sys.stderr)
        sys.exit(1)

    # 3. 构建会话日志文件路径
    log_file = log_dir / f"{session_id}.jsonl"
    if not log_file.exists():
        print(f"错误: 会话文件不存在: {log_file}", file=sys.stderr)
        sys.exit(1)

    # 4. 提取所有用户提问
    prompts = extract_user_prompts(log_file)

    # 5. 输出格式: timestamp|content-preview|uuid
    for prompt in prompts:
        print(f"{prompt['timestamp']}|{prompt['preview']}|{prompt['uuid']}")


if __name__ == '__main__':
    main()
