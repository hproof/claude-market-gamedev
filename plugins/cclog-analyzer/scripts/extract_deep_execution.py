#!/usr/bin/env python3
"""
extract_deep_execution.py
自动获取当前工作目录，深度遍历提取指定提问的执行树

用法: python extract_deep_execution.py <session-id> <prompt-uuid>
输出: Markdown 格式的执行流程表格
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime


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


# 最大输出记录数限制
MAX_RECORDS_LIMIT = 500

# 摘要长度限制（为了让路径完整显示，设为 150 字符）
MAX_SUMMARY_LENGTH = 150


def truncate_text(text, max_length=MAX_SUMMARY_LENGTH):
    """截断文本，保留关键信息"""
    if not isinstance(text, str):
        text = str(text) if text else ''
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'


def extract_summary(record):
    """
    从记录中提取摘要信息
    返回: (type_name, summary_text)
    """
    record_type = record.get('type', 'unknown')

    if record_type == 'user':
        content = record.get('message', {}).get('content', '')
        if isinstance(content, str):
            return 'user', f'用户提问: {truncate_text(content)}'
        # 处理非字符串类型（如 list、dict），尝试转换为字符串提取内容
        content_str = str(content) if content else ''
        return 'user', f'用户提问: {truncate_text(content_str)}'

    elif record_type == 'assistant':
        message = record.get('message', {})
        content = message.get('content', [])

        if isinstance(content, list) and len(content) > 0:
            first_item = content[0]
            item_type = first_item.get('type', '')

            if item_type == 'thinking':
                thinking_text = first_item.get('thinking', '')
                return 'thinking', f'AI思考: {truncate_text(thinking_text)}'

            elif item_type == 'tool_use':
                tool_name = first_item.get('name', 'Unknown')
                tool_input = first_item.get('input', {})
                # 对于 Read 工具，显示 file_path
                if tool_name == 'Read' and 'file_path' in tool_input:
                    return 'tool_use', f'{tool_name}: {tool_input["file_path"]}'
                # 对于 Bash 工具，显示 command
                elif tool_name == 'Bash' and 'command' in tool_input:
                    cmd = tool_input['command']
                    return 'tool_use', f'{tool_name}: {truncate_text(cmd, 100)}'
                # 对于 Agent 工具，显示 description
                elif tool_name == 'Agent' and 'description' in tool_input:
                    return 'tool_use', f'{tool_name}: {tool_input["description"]}'
                else:
                    input_summary = truncate_text(str(tool_input), 80)
                    return 'tool_use', f'{tool_name}: {input_summary}'

            elif item_type == 'text':
                text_content = first_item.get('text', '')
                return 'assistant', f'回复: {truncate_text(text_content)}'

        return 'assistant', '回复: [复杂内容]'

    elif record_type == 'tool_result':
        output = record.get('output', '')
        return 'tool_result', f'结果: {truncate_text(str(output))}'

    elif record_type == 'progress':
        data = record.get('data', {})
        agent_id = data.get('agentId')
        if agent_id:
            return 'progress', f'启动子代理: agent-{agent_id}'
        return 'progress', '进度更新'

    else:
        return record_type, f'[{record_type}]'


class MarkdownGenerator:
    """Markdown 报告生成器"""

    def __init__(self):
        self.records = []
        self.stats = {
            'total': 0,
            'main': 0,
            'subagent': 0,
            'by_type': {}
        }

    def add_record(self, seq, source, record_type, summary):
        """添加一条记录"""
        self.records.append({
            'seq': seq,
            'source': source,
            'type': record_type,
            'summary': summary
        })

        # 更新统计
        self.stats['total'] += 1
        if source == 'MAIN':
            self.stats['main'] += 1
        else:
            self.stats['subagent'] += 1

        self.stats['by_type'][record_type] = self.stats['by_type'].get(record_type, 0) + 1

    def generate(self, session_id, prompt_preview=''):
        """生成完整的 Markdown 报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        lines = []
        lines.append('# Claude Code 执行日志分析')
        lines.append('')
        lines.append(f'**会话**: {session_id}')
        if prompt_preview:
            lines.append(f'**用户提问**: {prompt_preview[:100]}')
        lines.append(f'**分析时间**: {timestamp}')
        lines.append(f'**记录总数**: {self.stats["total"]} (主会话: {self.stats["main"]}, 子代理: {self.stats["subagent"]})')
        lines.append('')
        lines.append('---')
        lines.append('')
        lines.append('## 执行流程')
        lines.append('')
        lines.append('| 序号 | 来源 | 类型 | 摘要 |')
        lines.append('|------|------|------|------|')

        for rec in self.records:
            # 转义摘要中的 |
            summary = rec['summary'].replace('|', '\\|').replace('\n', ' ')
            lines.append(f"| {rec['seq']} | {rec['source']} | {rec['type']} | {summary} |")

        lines.append('')
        lines.append('---')
        lines.append('')
        lines.append('## 统计信息')
        lines.append('')
        lines.append('| 指标 | 数值 |')
        lines.append('|------|------|')
        lines.append(f"| 总记录数 | {self.stats['total']} |")
        lines.append(f"| 主会话记录 | {self.stats['main']} |")
        lines.append(f"| 子代理记录 | {self.stats['subagent']} |")

        for type_name, count in sorted(self.stats['by_type'].items()):
            lines.append(f"| {type_name} | {count} |")

        return '\n'.join(lines)


def deep_traverse(main_lines, start_idx, log_dir, session_name, session_id):
    """深度遍历，输出 Markdown"""
    i = start_idx
    in_subagent = False
    record_count = 0
    generator = MarkdownGenerator()

    # 获取用户提问预览
    prompt_preview = ''
    if start_idx < len(main_lines):
        first_record = main_lines[start_idx][1]
        if first_record.get('type') == 'user':
            content = first_record.get('message', {}).get('content', '')
            if isinstance(content, str):
                prompt_preview = content[:100]

    while i < len(main_lines):
        if record_count >= MAX_RECORDS_LIMIT:
            generator.add_record(record_count + 1, 'SYSTEM', 'truncated', f'输出记录数超过限制 ({MAX_RECORDS_LIMIT})，已截断')
            break

        line_num, record, raw_line = main_lines[i]

        if not in_subagent and i > start_idx and record.get('type') == 'user':
            break

        source = 'MAIN'
        rec_type, summary = extract_summary(record)
        generator.add_record(record_count + 1, source, rec_type, summary)
        record_count += 1

        agent_id = extract_agent_id_from_progress(record)
        if agent_id:
            in_subagent = True
            subagent_log = log_dir / session_name / 'subagents' / f'agent-{agent_id}.jsonl'
            if subagent_log.exists():
                with open(subagent_log, 'r', encoding='utf-8') as f:
                    for sub_line in f:
                        if record_count >= MAX_RECORDS_LIMIT:
                            break
                        sub_line = sub_line.rstrip('\n\r')
                        if sub_line.strip():
                            try:
                                sub_record = json.loads(sub_line)
                                sub_source = f'agent-{agent_id}'
                                sub_type, sub_summary = extract_summary(sub_record)
                                generator.add_record(record_count + 1, sub_source, sub_type, sub_summary)
                                record_count += 1
                            except json.JSONDecodeError:
                                continue
            in_subagent = False

        i += 1

    print(generator.generate(session_id, prompt_preview))


def main():
    if len(sys.argv) < 3:
        print(f"用法: python {sys.argv[0]} <session-id> <prompt-uuid>", file=sys.stderr)
        print(f"示例: python {sys.argv[0]} xxx-xxx-xxxx-xxxx uuid", file=sys.stderr)
        sys.exit(1)

    session_id = sys.argv[1]
    target_uuid = sys.argv[2]

    cwd = get_cwd()
    log_dir = get_log_dir(cwd)

    if not log_dir.exists():
        print(f"错误: 日志目录不存在: {log_dir}", file=sys.stderr)
        sys.exit(1)

    session_path = log_dir / f"{session_id}.jsonl"

    if not session_path.exists():
        print(f"错误: 会话文件不存在: {session_path}", file=sys.stderr)
        sys.exit(1)

    main_lines = load_session_log(session_path)
    start_idx = find_prompt_line_num(main_lines, target_uuid)

    if start_idx == -1:
        print(f"错误: 找不到指定的提问 UUID: {target_uuid}", file=sys.stderr)
        sys.exit(1)

    deep_traverse(main_lines, start_idx, log_dir, session_path.stem, session_id)


if __name__ == '__main__':
    main()
