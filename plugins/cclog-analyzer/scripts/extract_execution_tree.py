#!/usr/bin/env python3
"""
extract_execution_tree.py
提取某个提问的完整执行树（包括所有后代节点）

用法: python extract_execution_tree.py <session-log-file> <prompt-uuid>
示例: python extract_execution_tree.py session.jsonl 449b2d95-c538-4b69-ae02-8eb23efcd174

输出: 按时间戳排序的 JSONL 格式记录
"""

import json
import sys
from pathlib import Path
from collections import defaultdict


def load_all_records(log_file):
    """加载所有日志记录"""
    records = []
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError:
                continue
    return records


def build_uuid_index(records):
    """构建 UUID 到记录的索引"""
    uuid_to_record = {}
    uuid_to_children = defaultdict(list)

    for record in records:
        uuid = record.get('uuid')
        if uuid:
            uuid_to_record[uuid] = record

        parent_uuid = record.get('parentUuid')
        if parent_uuid and uuid:
            uuid_to_children[parent_uuid].append(uuid)

    return uuid_to_record, uuid_to_children


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


def extract_agent_ids(records):
    """从 progress 记录中提取所有 agentId"""
    agent_ids = set()
    for record in records:
        if record.get('type') == 'progress':
            data = record.get('data', {})
            agent_id = data.get('agentId')
            if agent_id:
                agent_ids.add(agent_id)
    return agent_ids


def load_subagent_logs(log_dir, session_name, agent_ids):
    """加载子代理日志"""
    subagent_logs = {}
    subagents_dir = log_dir / session_name / 'subagents'

    if not subagents_dir.exists():
        return subagent_logs

    for agent_id in agent_ids:
        log_file = subagents_dir / f'agent-{agent_id}.jsonl'
        if log_file.exists():
            records = load_all_records(str(log_file))
            subagent_logs[agent_id] = records

    return subagent_logs


def main():
    if len(sys.argv) < 3:
        print(f"用法: python {sys.argv[0]} <session-log-file> <prompt-uuid>")
        print(f"示例: python {sys.argv[0]} session.jsonl 449b2d95-c538-4b69-ae02-8eb23efcd174")
        sys.exit(1)

    log_file = Path(sys.argv[1])
    prompt_uuid = sys.argv[2]

    if not log_file.exists():
        print(f"错误: 文件不存在: {log_file}")
        sys.exit(1)

    log_dir = log_file.parent
    session_name = log_file.stem  # 去掉 .jsonl 后缀

    # 1. 加载主会话日志
    records = load_all_records(str(log_file))

    # 2. 构建索引
    uuid_to_record, uuid_to_children = build_uuid_index(records)

    # 3. 检查目标 UUID 是否存在
    if prompt_uuid not in uuid_to_record:
        print(f"错误: 找不到指定的提问 UUID: {prompt_uuid}")
        sys.exit(1)

    # 4. 收集所有后代节点
    all_uuids = collect_all_descendants(prompt_uuid, uuid_to_children)

    # 5. 提取相关记录并排序
    related_records = [uuid_to_record[uuid] for uuid in all_uuids if uuid in uuid_to_record]
    related_records.sort(key=lambda x: x.get('timestamp', ''))

    # 6. 输出主会话记录
    for record in related_records:
        print(json.dumps(record, ensure_ascii=False))

    # 7. 提取并加载子代理日志
    agent_ids = extract_agent_ids(related_records)
    if agent_ids:
        subagent_logs = load_subagent_logs(log_dir, session_name, agent_ids)

        # 8. 输出子代理日志分隔标记
        print("")
        print("=== SUBAGENT_LOGS ===")

        for agent_id, agent_records in subagent_logs.items():
            print(f"AGENT:{agent_id}")
            for record in agent_records:
                print(json.dumps(record, ensure_ascii=False))


if __name__ == '__main__':
    main()
