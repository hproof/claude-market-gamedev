#!/usr/bin/env python3
"""
extract_deep_execution.py
深度遍历提取执行树，遇到子代理立即输出其日志

用法: python extract_deep_execution.py <project-log-dir> <session-file> <prompt-uuid>
输出: 深度遍历的所有记录，子代理记录直接穿插在主记录中
      格式: [SOURCE]|{json-line}
      SOURCE: MAIN 或 agent-{id}
"""

import json
import sys
from pathlib import Path


def load_session_log(log_path):
    """加载会话日志，返回 (行号, json行) 列表"""
    lines = []
    with open(log_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            line = line.rstrip('\n\r')
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                lines.append((line_num, record, line))
            except json.JSONDecodeError:
                continue
    return lines


def find_prompt_line_num(lines, target_uuid):
    """找到目标提问的行号"""
    for line_num, record, raw_line in lines:
        if record.get('uuid') == target_uuid and record.get('type') == 'user':
            return line_num
    return -1


def extract_agent_id_from_progress(record):
    """从 progress 记录中提取 agentId"""
    if record.get('type') == 'progress':
        data = record.get('data', {})
        return data.get('agentId')
    return None


def deep_traverse(main_lines, start_idx, project_dir, session_name, related_uuids=None):
    """
    深度遍历执行树
    遇到子代理立即读取并输出其日志，然后继续主会话
    """
    if related_uuids is None:
        related_uuids = set()

    i = start_idx
    while i < len(main_lines):
        line_num, record, raw_line = main_lines[i]

        uuid = record.get('uuid', '')
        parent_uuid = record.get('parentUuid', '')

        # 检查是否相关：uuid 已在集合中，或 parentUuid 在集合中，或是起始行
        is_related = (uuid in related_uuids) or (parent_uuid in related_uuids) or (i == start_idx)

        if not is_related:
            i += 1
            continue

        # 输出当前主会话记录
        print(f"MAIN|{raw_line}")
        related_uuids.add(uuid)

        # 检查是否是子代理调用（progress 类型且有 agentId）
        agent_id = extract_agent_id_from_progress(record)
        if agent_id:
            # 深度优先：立即读取并输出子代理日志
            subagent_log = project_dir / session_name / 'subagents' / f'agent-{agent_id}.jsonl'
            if subagent_log.exists():
                # 输出子代理所有记录
                with open(subagent_log, 'r', encoding='utf-8') as f:
                    for sub_line in f:
                        sub_line = sub_line.rstrip('\n\r')
                        if sub_line.strip():
                            print(f"agent-{agent_id}|{sub_line}")

        i += 1


def main():
    if len(sys.argv) < 4:
        print(f"用法: python {sys.argv[0]} <project-log-dir> <session-file> <prompt-uuid>", file=sys.stderr)
        print(f"示例: python {sys.argv[0]} ~/.claude/projects/D--git-proj-bullet3 session.jsonl uuid", file=sys.stderr)
        sys.exit(1)

    project_dir = Path(sys.argv[1])
    session_file = sys.argv[2]
    target_uuid = sys.argv[3]

    session_path = project_dir / session_file

    if not session_path.exists():
        print(f"错误: 会话文件不存在: {session_path}", file=sys.stderr)
        sys.exit(1)

    # 1. 加载主会话日志
    main_lines = load_session_log(session_path)

    # 2. 找到目标提问的行号
    start_idx = find_prompt_line_num(main_lines, target_uuid)
    if start_idx == -1:
        print(f"错误: 找不到指定的提问 UUID: {target_uuid}", file=sys.stderr)
        sys.exit(1)

    # 3. 深度遍历并输出
    related_uuids = {target_uuid}
    deep_traverse(main_lines, start_idx, project_dir, session_path.stem, related_uuids)


if __name__ == '__main__':
    main()
