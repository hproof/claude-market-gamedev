#!/usr/bin/env python3
"""
extract_deep_execution.py
自动获取当前工作目录，深度遍历提取指定提问的执行树

用法: python extract_deep_execution.py <session-id> <prompt-uuid>
输出: JSON 数组，每条记录包含 _source 字段（MAIN 或 agent-{id}）
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
    # 将 [: \\ / _] 替换为 -
    encoded = re.sub(r'[:\\\\/_]', '-', cwd)
    return encoded


def get_log_dir(cwd):
    """根据当前目录获取日志目录"""
    encoded = encode_path(cwd)
    home = Path.home()
    log_dir = home / '.claude' / 'projects' / encoded
    return log_dir


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


# 要移除的冗余字段
FIELDS_TO_REMOVE = {
    'sessionId', 'parentUuid', 'uuid', 'usage', 'isSidechain',
    'userType', 'entrypoint', 'cwd', 'version', 'gitBranch', 'slug',
    'permissionMode', 'promptId', 'sourceToolAssistantUUID', 'toolUseResult',
    'isMeta', 'model', 'stop_reason', 'stop_sequence', 'id'
}

# message 中要移除的字段
MESSAGE_FIELDS_TO_REMOVE = {'usage', 'id', 'model', 'stop_reason', 'stop_sequence'}

# content 数组项中要移除的字段
CONTENT_FIELDS_TO_REMOVE = {'signature'}

# 内容截断长度
MAX_CONTENT_LENGTH = 300


def truncate_content(content, max_length=MAX_CONTENT_LENGTH):
    """截断过长的内容"""
    if not isinstance(content, str):
        return content
    if len(content) <= max_length:
        return content
    return content[:max_length] + f'...[截断，共{len(content)}字符]'


def simplify_content_item(item):
    """简化 content 数组中的单个项"""
    if not isinstance(item, dict):
        return item

    # 保留需要的字段
    simple_item = {k: v for k, v in item.items() if k not in CONTENT_FIELDS_TO_REMOVE}

    item_type = simple_item.get('type')

    # 根据类型处理内容
    if item_type == 'tool_result':
        # tool_result 的 content 往往很长，需要截断
        if 'content' in simple_item:
            simple_item['content'] = truncate_content(simple_item['content'])
    elif item_type == 'text':
        # text 类型的内容也可能很长
        if 'text' in simple_item:
            simple_item['text'] = truncate_content(simple_item['text'])
    elif item_type == 'thinking':
        # thinking 内容也截断
        if 'thinking' in simple_item:
            simple_item['thinking'] = truncate_content(simple_item['thinking'])

    return simple_item


def simplify_record(record):
    """简化记录，移除冗余字段"""
    simplified = {}
    for key, value in record.items():
        if key in FIELDS_TO_REMOVE:
            continue
        # 简化 message
        if key == 'message' and isinstance(value, dict):
            msg = {k: v for k, v in value.items() if k not in MESSAGE_FIELDS_TO_REMOVE}
            # 简化 content 数组
            if 'content' in msg and isinstance(msg['content'], list):
                msg['content'] = [simplify_content_item(item) for item in msg['content']]
            # user 类型的字符串 content 不截断，完整保留
            elif 'content' in msg and isinstance(msg['content'], str):
                pass  # 保留原始内容，不做截断
            simplified[key] = msg
        else:
            simplified[key] = value
    return simplified


def format_record(record, source):
    """格式化记录，简化并添加来源"""
    simplified = simplify_record(record)
    simplified['_source'] = source
    return simplified


def deep_traverse(main_lines, start_idx, log_dir, session_name):
    """
    深度遍历执行树
    遇到子代理立即读取并输出其日志，然后继续主会话
    在主agent中遇到新的用户提问时停止
    """
    i = start_idx
    in_subagent = False  # 标记是否在子agent执行中

    while i < len(main_lines):
        line_num, record, raw_line = main_lines[i]

        # 如果在主agent中（不在子agent内）且遇到新的用户提问，结束遍历
        # 从第二条记录开始判断，避免一开始就结束
        if not in_subagent and i > start_idx and record.get('type') == 'user':
            break

        # 输出当前主会话记录（简化版）
        formatted = format_record(record, 'MAIN')
        print(json.dumps(formatted, ensure_ascii=False))

        # 检查是否是子代理调用
        agent_id = extract_agent_id_from_progress(record)
        if agent_id:
            in_subagent = True  # 标记进入子agent
            subagent_log = log_dir / session_name / 'subagents' / f'agent-{agent_id}.jsonl'
            if subagent_log.exists():
                with open(subagent_log, 'r', encoding='utf-8') as f:
                    for sub_line in f:
                        sub_line = sub_line.rstrip('\n\r')
                        if sub_line.strip():
                            try:
                                sub_record = json.loads(sub_line)
                                formatted_sub = format_record(sub_record, f'agent-{agent_id}')
                                print(json.dumps(formatted_sub, ensure_ascii=False))
                            except json.JSONDecodeError:
                                continue
            in_subagent = False  # 标记退出子agent

        i += 1


def main():
    if len(sys.argv) < 3:
        print(f"用法: python {sys.argv[0]} <session-id> <prompt-uuid>", file=sys.stderr)
        print(f"示例: python {sys.argv[0]} xxx-xxx-xxxx-xxxx uuid", file=sys.stderr)
        sys.exit(1)

    session_id = sys.argv[1]
    target_uuid = sys.argv[2]

    # 1. 获取当前工作目录并找到日志目录
    cwd = get_cwd()
    log_dir = get_log_dir(cwd)

    if not log_dir.exists():
        print(f"错误: 日志目录不存在: {log_dir}", file=sys.stderr)
        sys.exit(1)

    # 直接使用 session_id 构建文件路径
    session_path = log_dir / f"{session_id}.jsonl"

    if not session_path.exists():
        print(f"错误: 会话文件不存在: {session_path}", file=sys.stderr)
        sys.exit(1)

    # 2. 加载主会话日志
    main_lines = load_session_log(session_path)

    # 3. 找到目标提问的行号
    start_idx = find_prompt_line_num(main_lines, target_uuid)
    if start_idx == -1:
        print(f"错误: 找不到指定的提问 UUID: {target_uuid}", file=sys.stderr)
        sys.exit(1)

    # 4. 深度遍历并输出
    deep_traverse(main_lines, start_idx, log_dir, session_path.stem)


if __name__ == '__main__':
    main()
