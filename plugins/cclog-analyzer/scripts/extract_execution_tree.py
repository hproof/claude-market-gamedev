#!/usr/bin/env python3
"""
extract_execution_tree.py
提取某个提问的完整执行树（包括所有后代节点）

用法: python extract_execution_tree.py <session-log-file> <prompt-uuid>
输出: 完整的 JSON 行（原样输出，不做修改）

子代理日志通过 AGENT:agent-id 分隔行输出
"""

import json
import sys
from pathlib import Path
from collections import defaultdict


def build_uuid_index(log_file):
    """构建 UUID 到文件位置的索引"""
    uuid_to_line = {}
    uuid_to_children = defaultdict(list)
    all_lines = []

    with open(log_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            line = line.rstrip('\n\r')
            if not line.strip():
                continue
            all_lines.append(line)
            try:
                record = json.loads(line)
                uuid = record.get('uuid')
                parent_uuid = record.get('parentUuid')

                if uuid:
                    uuid_to_line[uuid] = line_num
                if parent_uuid and uuid:
                    uuid_to_children[parent_uuid].append(uuid)
            except json.JSONDecodeError:
                continue

    return all_lines, uuid_to_line, uuid_to_children


def collect_all_descendants(root_uuid, uuid_to_children, max_depth=100):
    """收集所有后代节点的 UUID"""
    all_uuids = {root_uuid}
    current_level = {root_uuid}
    depth = 0

    while current_level and depth < max_depth:
        next_level = set()
        for uuid in current_level:
            children = uuid_to_children.get(uuid, [])
            for child in children:
                if child not in all_uuids:
                    all_uuids.add(child)
                    next_level.add(child)
        current_level = next_level
        depth += 1

    return all_uuids


def extract_agent_ids(lines, uuid_set):
    """从相关记录中提取所有 agentId"""
    agent_ids = set()
    for line in lines:
        try:
            record = json.loads(line)
            if record.get('uuid') in uuid_set and record.get('type') == 'progress':
                data = record.get('data', {})
                agent_id = data.get('agentId')
                if agent_id:
                    agent_ids.add(agent_id)
        except json.JSONDecodeError:
            continue
    return agent_ids


def main():
    if len(sys.argv) < 3:
        print(f"用法: python {sys.argv[0]} <session-log-file> <prompt-uuid>", file=sys.stderr)
        sys.exit(1)

    log_file = Path(sys.argv[1])
    prompt_uuid = sys.argv[2]

    if not log_file.exists():
        print(f"错误: 文件不存在: {log_file}", file=sys.stderr)
        sys.exit(1)

    log_dir = log_file.parent
    session_name = log_file.stem

    # 1. 构建索引
    all_lines, uuid_to_line, uuid_to_children = build_uuid_index(str(log_file))

    # 2. 检查目标 UUID 是否存在
    if prompt_uuid not in {line.split('"uuid":"')[1].split('"')[0] if '"uuid":"' in line else '' for line in all_lines}:
        # 更可靠的检查
        found = False
        for line in all_lines:
            try:
                r = json.loads(line)
                if r.get('uuid') == prompt_uuid:
                    found = True
                    break
            except:
                continue
        if not found:
            print(f"错误: 找不到指定的提问 UUID: {prompt_uuid}", file=sys.stderr)
            sys.exit(1)

    # 3. 收集所有后代节点 UUID
    all_uuids = collect_all_descendants(prompt_uuid, uuid_to_children)

    # 4. 获取相关行号并排序（保持原始顺序）
    line_indices = []
    for uuid in all_uuids:
        if uuid in uuid_to_line:
            line_indices.append(uuid_to_line[uuid])
    line_indices.sort()

    # 5. 输出主会话记录（完整 JSON 行）
    for idx in line_indices:
        print(all_lines[idx])

    # 6. 提取 agentId 并输出子代理日志
    related_lines = [all_lines[i] for i in line_indices]
    agent_ids = extract_agent_ids(related_lines, all_uuids)

    if agent_ids:
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
