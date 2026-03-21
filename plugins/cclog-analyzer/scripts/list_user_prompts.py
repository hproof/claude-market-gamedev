#!/usr/bin/env python3
"""
list_user_prompts.py
列出会话中的所有用户提问

用法: python list_user_prompts.py <session-log-file>
输出: 完整的 user 类型 JSON 行（原样输出，不做修改）
"""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print(f"用法: python {sys.argv[0]} <session-log-file>", file=sys.stderr)
        sys.exit(1)

    log_file = Path(sys.argv[1])
    if not log_file.exists():
        print(f"错误: 文件不存在: {log_file}", file=sys.stderr)
        sys.exit(1)

    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if record.get('type') == 'user':
                    # 原样输出完整 JSON 行，不做任何修改
                    print(line)
            except json.JSONDecodeError:
                continue


if __name__ == '__main__':
    main()
