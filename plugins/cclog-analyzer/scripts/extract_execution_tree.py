#!/usr/bin/env python3
"""
extract_execution_tree.py
提取某个提问的完整执行树

用法: python extract_execution_tree.py <session-log-file> <prompt-uuid>
输出: 完整 JSON 行（原样输出），子代理通过 AGENT:id 分隔

算法：顺序遍历，找到提问后收集所有相关记录
"""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print(f"用法: python {sys.argv[0]} <session-log-file> <prompt-uuid>", file=sys.stderr)
        sys.exit(1)

    log_file = Path(sys.argv[1])
    target_uuid = sys.argv[2]

    if not log_file.exists():
        print(f"错误: 文件不存在: {log_file}", file=sys.stderr)
        sys.exit(1)

    log_dir = log_file.parent
    session_name = log_file.stem

    # 1. 找到目标提问的行号
    target_line_num = -1
    with open(log_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if f'"uuid":"{target_uuid}"' in line and '"type":"user"' in line:
                target_line_num = i
                break

    if target_line_num == -1:
        print(f"错误: 找不到指定的提问 UUID: {target_uuid}", file=sys.stderr)
        sys.exit(1)

    # 2. 从目标行开始往下遍历，收集相关记录
    related_uuids = {target_uuid}  # 当前执行树中的所有 uuid
    agent_ids = set()  # 收集子代理 id

    with open(log_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < target_line_num:
                continue  # 跳过前面的记录

            line = line.rstrip('\n\r')
            if not line.strip():
                continue

            try:
                record = json.loads(line)
                uuid = record.get('uuid', '')
                parent_uuid = record.get('parentUuid', '')

                # 检查是否相关：uuid 已在集合中，或 parentUuid 在集合中
                is_related = (uuid in related_uuids) or (parent_uuid in related_uuids)

                if is_related:
                    print(line)
                    related_uuids.add(uuid)

                    # 提取子代理 id
                    if record.get('type') == 'progress':
                        agent_id = record.get('data', {}).get('agentId')
                        if agent_id:
                            agent_ids.add(agent_id)

            except json.JSONDecodeError:
                continue

    # 3. 输出子代理日志
    for agent_id in sorted(agent_ids):
        subagent_log = log_dir / session_name / 'subagents' / f'agent-{agent_id}.jsonl'
        if subagent_log.exists():
            print(f"AGENT:{agent_id}")
            with open(subagent_log, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.rstrip('\n\r')
                    if line.strip():
                        print(line)


if __name__ == '__main__':
    main()
