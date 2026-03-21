---
name: cclog-analyzer
description: |
  分析当前 Claude Code 会话的执行日志，追溯用户提问的完整执行流程。
  在用户询问"分析这次执行"、"查看刚才的执行过程"、"这次 Claude 是怎么处理的"时触发。
allowed-tools: Read, Glob, Bash(python *), Bash(cat *), Bash(ls *), Bash(dir *), AskUserQuestion
---

# Claude Code 执行日志分析器

## 核心任务

帮助用户追溯某次提问的完整执行过程，展示 Claude 如何思考、调用工具和协调子代理。

## 执行步骤（严格按顺序执行）

### 步骤 1：获取当前项目目录名

根据当前工作目录（cwd），按编码规则转换：
- 盘符 `:` → `--`
- 路径分隔符 `\` 或 `/` → `-`

**示例：** `D:\git_proj\bullet3` → `D--git-proj-bullet3`

日志目录路径：`~/.claude/projects/{encoded-path}/`

### 步骤 2：找到最新的会话日志文件

```bash
# 列出目录下的 .jsonl 文件，按修改时间排序取最新的
ls -t ~/.claude/projects/{encoded-path}/*.jsonl | head -1
```

### 步骤 3：列出所有用户提问

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/list_user_prompts.py {session-log-file}
```

**脚本输出：** 每行是一个完整的 `type: "user"` JSON 记录

### 步骤 4（⚠️ 关键）：强制用户选择提问

**必须执行此步骤！** 解析步骤3输出的 JSON 记录，提取 `timestamp` 和 `message.content` 的前100字，使用 `AskUserQuestion` 工具展示列表：

```
请选择要分析的执行记录：

1. [2026-03-14 13:05] 这是 bullet 物理引擎代码，我希望借助 claude code 来快速了解...
2. [2026-03-14 13:30] 请分析 LinearMath 模块的 btVector3 类实现...
3. [2026-03-14 14:00] 帮我找出碰撞检测相关的核心文件...
```

**要求：**
- 必须等待用户明确选择后才能继续
- 不允许自动选择（如选最新的、最长的等）
- 获取用户选择项的 `uuid`

### 步骤 5：提取完整执行树

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
```

### 步骤 6：解析并生成执行报告

解析步骤5的输出，按以下结构生成最终报告：

```markdown
# Claude Code 执行过程分析

## 用户提问
**时间**: {timestamp}
**内容**: {message.content}

---

## 执行过程

### 记录 1: 用户输入
{完整的 user 类型 JSON}

### 记录 2: 思考与规划
{thinking 内容块}

### 记录 3: 工具调用 - {工具名}
**时间**: {timestamp}
**输入参数**: {完整的 input 对象}

#### ↳ 子代理执行 (agentId: xxx)
**任务描述**: {完整的 prompt 内容}

### 记录 4: 工具调用结果
{tool_result 内容}

### 记录 5: 最终回复
{assistant 的 content}

---

## 执行统计
| 指标 | 数值 |
|------|------|
| 总执行时间 | 首条到最后一条记录的时间差 |
| 主会话记录数 | X |
| 子代理数量 | X |
| 各子代理记录数 | X |
```

## 日志格式参考

详细规范请参阅：`${CLAUDE_PLUGIN_ROOT}/docs/log-format-spec.md`

关键字段：
- `type`: user/assistant/progress
- `uuid`: 唯一标识
- `parentUuid`: 父节点
- `timestamp`: 时间戳
- `data.agentId`: 子代理标识

## 边界处理

1. **无子代理**: 脚本输出不含 `AGENT:` 行，正常处理即可
2. **子代理运行中**: 脚本只输出已完成的记录
3. **超长内容**: 完整输出，不截断
