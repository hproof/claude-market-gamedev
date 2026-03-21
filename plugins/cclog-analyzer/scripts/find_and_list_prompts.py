#!/usr/bin/env python3
"""
find_and_list_prompts.py
自动获取当前工作目录，找到日志并列出所有用户提问

用法: python find_and_list_prompts.py
输出: 每行一个用户提问，格式: session-file|timestamp|content-preview|uuid
"""

import json
import os
import sys
from pathlib import Path


def get_cwd():
    """获取当前工作目录"""
    # 优先从环境变量获取，否则使用进程当前目录
    return os.environ.get('PWD', os.getcwd())


def encode_path(cwd):
    """将当前工作目录编码为日志目录名"""
    import re
    # 将 [: \\ / _] 替换为 -
    encoded = re.sub(r'[:\\\\/_]', '-', cwd)
    return encoded


def get_log_dir(cwd):
    """根据当前目录获取日志目录"""
    encoded = encode_path(cwd)
    home = Path.home()
    log_dir = home / '.claude' / 'projects' / encoded
    return log_dir


def find_latest_session_log(project_dir):
    """找到最新的 .jsonl 会话日志文件"""
    project_path = Path(project_dir)
    if not project_path.exists():
        return None

    jsonl_files = list(project_path.glob("*.jsonl"))
    if not jsonl_files:
        return None

    latest = max(jsonl_files, key=lambda f: f.stat().st_mtime)
    return latest


def is_real_user_input(record):
    """判断是否是真正的用户输入（排除系统消息和工具结果）"""
    message = record.get('message', {})
    content = message.get('content', '') if isinstance(message, dict) else ''

    # content 是数组的情况：检查是否包含 tool_result
    if isinstance(content, list):
        # 如果数组中包含 tool_result 类型，则不是真实用户输入
        for item in content:
            if isinstance(item, dict) and item.get('type') in ('tool_result', 'tool_use'):
                return False
        # 将数组转为字符串用于预览
        return True

    # content 是字符串的情况
    if not isinstance(content, str):
        return False

    content = content.strip()
    # 排除系统标签包裹的内容
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
        # 提取数组中的文本内容
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
                    # 过滤非真实用户输入
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
    # 1. 获取当前工作目录
    cwd = get_cwd()

    # 2. 根据当前目录找到日志目录
    log_dir = get_log_dir(cwd)
    if not log_dir.exists():
        print(f"错误: 日志目录不存在: {log_dir}", file=sys.stderr)
        sys.exit(1)

    # 3. 找到最新的会话日志
    latest_log = find_latest_session_log(log_dir)
    if not latest_log:
        print(f"错误: 在 {log_dir} 中找不到会话日志文件", file=sys.stderr)
        sys.exit(1)

    # 4. 提取所有用户提问
    prompts = extract_user_prompts(latest_log)

    # 5. 输出格式: session-file|timestamp|content-preview|uuid
    session_name = latest_log.name
    for prompt in prompts:
        print(f"{session_name}|{prompt['timestamp']}|{prompt['preview']}|{prompt['uuid']}")


if __name__ == '__main__':
    main()
