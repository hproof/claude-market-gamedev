---
name: cclog-analyzer
description: |
  分析当前 Claude Code 会话的执行日志，追溯用户提问的完整执行流程。
  在用户询问"分析这次执行"、"查看刚才的执行过程"、"这次 Claude 是怎么处理的"时触发。
allowed-tools: Read, Glob, Bash(python *), Bash(cat *), Bash(ls *), Bash(dir *), AskUserQuestion
---

# Claude Code 执行日志分析器

你是一位 Claude Code 执行分析专家。通过专用脚本高效提取日志，清晰展示执行过程。

## 日志格式参考

详细日志格式规范请参阅：`${CLAUDE_PLUGIN_ROOT}/docs/log-format-spec.md`

## 执行流程（全部通过脚本完成）

### 阶段 1：定位并获取所有用户提问

**步骤：**
1. 获取当前工作目录，编码为项目目录名
2. 找到最新的会话日志文件（按修改时间）
3. 使用脚本提取所有用户提问

```bash
# 列出所有用户提问（输出完整 JSON 行）
python ${CLAUDE_PLUGIN_ROOT}/scripts/list_user_prompts.py {session-log-file}
```

**脚本输出：** 每行是一个完整的 `type: "user"` JSON 记录

### 阶段 2：强制用户选择提问

解析脚本输出的 JSON，提取 `timestamp` 和 `message.content` 展示给用户：

```
请选择要分析的执行记录：

1. [2026-03-14 13:05] 这是 bullet 物理引擎代码，我希望借助 claude code 来快速了解...
2. [2026-03-14 13:30] 请分析 LinearMath 模块的 btVector3 类实现...
3. [2026-03-14 14:00] 帮我找出碰撞检测相关的核心文件...
```

**必须等待用户明确选择后，获取该提问的 `uuid`。**

### 阶段 3：提取完整执行树

使用脚本提取该提问的所有相关记录：

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/extract_execution_tree.py {session-log-file} {selected-uuid}
```

**脚本输出格式：**
```
{主会话相关记录（完整 JSON 行）}
...
AGENT:agent-id-1
{子代理 1 的记录（完整 JSON 行）}
...
AGENT:agent-id-2
{子代理 2 的记录（完整 JSON 行）}
...
```

### 阶段 4：解析并输出执行报告

**解析脚本的输出行：**
1. 按行读取，每行是一个完整 JSON 记录
2. 遇到 `AGENT:xxx` 行表示切换到该子代理的记录
3. 按 `timestamp` 字段排序后输出

**输出格式：**

```markdown
# Claude Code 执行过程分析

## 用户提问
**时间**: {timestamp}
**内容**: {message.content}

---

## 执行过程

### Step 1: 用户输入
{完整的 user 类型记录}

### Step 2: 思考与规划
{thinking 内容块}

### Step 3: 工具调用 - {工具名}
**时间**: {timestamp}
**输入参数**: {完整的 input 对象}

#### ↳ 子代理执行 (agentId: xxx)
**任务描述**: {完整的 prompt 内容}

### Step 4: 最终回复
{assistant 的 content}

---

## 执行统计
| 指标 | 数值 |
|------|------|
| 总执行时间 | X |
| 主会话记录数 | X |
| 子代理数量 | X |
| 各子代理记录数 | X |
```

## 关键技术细节

### 项目目录名编码

当前目录 `D:\git_proj\bullet3` → `D--git-proj-bullet3`
- `:` → `--`
- `\` 或 `/` → `-`

### 日志文件路径

```
~/.claude/projects/{encoded-path}/
├── {session-id}.jsonl
└── {session-id}/
    └── subagents/
        ├── agent-{id}.jsonl
        └── agent-{id}.meta.json
```

### 关键字段说明

| 字段 | 用途 |
|------|------|
| `type` | 消息类型: user/assistant/progress |
| `uuid` | 唯一标识 |
| `parentUuid` | 父节点，用于构建执行树 |
| `timestamp` | 时间戳，用于排序 |
| `data.agentId` | 子代理标识 |

## 边界处理

1. **无子代理**: 脚本输出不含 `AGENT:` 行
2. **子代理运行中**: 正常输出已完成的记录
3. **超长内容**: 完整输出，不截断
