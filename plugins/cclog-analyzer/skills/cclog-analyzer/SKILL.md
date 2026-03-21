---
name: cclog-analyzer
description: |
  分析当前 Claude Code 会话的执行日志，追溯用户提问的完整执行流程。
  在用户询问"分析这次执行"、"查看刚才的执行过程"、"这次 Claude 是怎么处理的"时触发。
allowed-tools: Read, Glob, Grep, Bash(find *), Bash(wc *), Bash(head *), Bash(tail *), Bash(jq *), AskUserQuestion
---

# Claude Code 执行日志分析器

你是一位 Claude Code 执行分析专家。你的任务是帮助用户追溯某次提问的完整执行过程，清晰展示 Claude 是如何思考、规划、调用工具和协调子代理的。

## 日志格式参考

详细日志格式规范请参阅：`${CLAUDE_PLUGIN_ROOT}/docs/log-format-spec.md`

## 执行流程

### 阶段 1：定位当前会话日志

**确定当前会话信息：**
- 当前工作目录（cwd）
- 当前会话 ID（从环境或上下文推断）

**查找日志文件：**
根据当前工作目录路径，按照编码规则转换为项目目录名。
详见 `${CLAUDE_PLUGIN_ROOT}/docs/log-format-spec.md` 中「项目目录名编码规则」章节。

示例：若当前目录为 `D:\git_proj\bullet3`，则日志目录为 `~/.claude/projects/D--git-proj-bullet3/`

**提取所有用户提问：**
从主会话日志中提取 `type: "user"` 的记录，获取：
- `uuid`：用户提问的 ID
- `timestamp`：提问时间
- `message.content`：提问内容（取前 100 字摘要）

```bash
# 使用 jq 提取用户提问
cat {session-id}.jsonl | jq -r 'select(.type=="user") | "\(.uuid)|\(.timestamp)|\(.message.content[0:100])"'
```

### 阶段 2：让用户选择要分析的提问

使用 `AskUserQuestion` 工具展示用户提问列表，让用户选择。

**选择列表格式：**
```
请选择要分析的执行记录：

1. [2026-03-14 13:05] 这是 bullet 物理引擎代码，我希望借助 claude code 来快速了解...
2. [2026-03-14 13:30] 请分析 LinearMath 模块的 btVector3 类实现...
3. [2026-03-14 14:00] 帮我找出碰撞检测相关的核心文件...
...
```

**获取选择结果：**
- 记录用户选择的索引
- 获取该提问的 `uuid` 作为分析的根节点

### 阶段 3：构建执行树并分析

**3.1 读取主会话日志中与该提问相关的所有记录**

从用户提问的 `uuid` 开始，追踪所有后代节点：
- 使用 `parentUuid` 关联查找
- 收集所有相关的 `assistant`、`progress`、`tool_result` 记录

**3.2 识别子代理调用**

从 `progress` 类型记录中提取：
- `agentId`：子代理 ID
- `prompt`：子代理的任务描述
- `toolUseID` / `parentToolUseID`：调用链关系

**3.3 读取子代理日志**

对于每个子代理：
```bash
# 子代理日志路径
{session-id}/subagents/agent-{agentId}.jsonl
```

提取子代理的执行记录，结构与主会话相同。

**3.4 构建执行流程图**

按时间顺序组织所有事件，形成执行树：
```
用户提问 (uuid: A)
├── 思考过程 (thinking)
├── 工具调用 1: Bash (id: Bash_0)
│   └── 工具结果
├── 工具调用 2: Agent (id: Agent_0)
│   └── 子代理 A (agentId: xxx)
│       ├── 思考过程
│       ├── 工具调用: Glob
│       └── 工具调用: Read
├── 工具调用 3: Agent (id: Agent_1)
│   └── 子代理 B (agentId: yyy)
│       └── ...
└── 最终回复
```

### 阶段 4：输出执行过程报告

以清晰的层级结构输出执行过程：

```markdown
# Claude Code 执行过程分析

## 用户提问
**时间**: 2026-03-14 13:05:04
**内容**: 这是 bullet 物理引擎代码，我希望借助 claude code 来快速了解其 src 目录下的代码结构流程...

---

## 执行过程

### Step 1: 思考与规划
**Claude 的思考**:
用户想要快速了解 Bullet3 物理引擎的 src 目录下的代码结构和流程。这是一个较大的 C++ 项目...

**决策**: 使用 Agent 工具的 Explore 类型来并行分析各个核心模块。

---

### Step 2: 工具调用 - Agent (Agent_0)
**时间**: 13:05:15
**描述**: 探索 LinearMath 模块
**输入参数**:
- subagent_type: Explore
- prompt: "请探索 Bullet3 物理引擎的 src/LinearMath 目录..."

#### ↳ 子代理执行 (agentId: af0c9fe6a1e515033, 类型: Explore)

**Step 2.1**: 工具调用 - Bash (Bash_0)
- 命令: `ls -la D:/git_proj/bullet3/src/LinearMath`
- 结果: [成功] 列出 50+ 个文件

**Step 2.2**: 工具调用 - Glob (Glob_1)
- 模式: `src/LinearMath/**/*`
- 结果: 匹配到 57 个文件

**Step 2.3**: 工具调用 - Bash (Bash_2)
- 命令: `find ... -type d | head -50`
- 结果: [成功]

**子代理完成**: 返回结构化总结

---

### Step 3: 工具调用 - Agent (Agent_1)
**时间**: 13:05:18
**描述**: 探索 BulletCollision 模块
**输入参数**:
- subagent_type: Explore
- prompt: "请探索 Bullet3 物理引擎的 src/BulletCollision 目录..."

#### ↳ 子代理执行 (agentId: a00463737d01a6eee, 类型: Explore)

**Step 3.1**: 工具调用 - Bash (Bash_0)
- 命令: `find /d/git_proj/bullet3/src/BulletCollision -type d | head -50`
- 结果: [成功]

**Step 3.2**: 工具调用 - Glob (Glob_1)
- 模式: `src/BulletCollision/**/*.h`
- 结果: 匹配到 80+ 个头文件

**子代理完成**: 返回结构化总结

---

### Step 4-5: 并行 Agent 调用 (Agent_2, Agent_3)
[类似的详细记录...]

---

### Step 6: 最终回复
**时间**: 13:08:23
**Claude 向用户返回综合结果**，汇总四个子代理的探索结果。

---

## 执行统计

| 指标 | 数值 |
|------|------|
| 总执行时间 | 3分19秒 |
| 工具调用次数 | 12 |
| 子代理数量 | 4 |
| 子代理类型 | Explore x4 |
| Token 使用量 | 输入 18,136 / 输出 703 |

## 执行特点

1. **并行执行**: 4 个子代理同时运行，提高效率
2. **分治策略**: 将大任务拆分为模块级探索
3. **深度探索**: 每个子代理执行 3-5 个工具调用
```

## 关键技术细节

### 如何关联父子节点

使用 `parentUuid` 字段建立消息树：
```bash
# 查找某 uuid 的所有子节点
cat session.jsonl | jq 'select(.parentUuid=="目标uuid")'
```

### 如何追踪 Agent 调用链

使用 `toolUseID` 和 `parentToolUseID`：
```bash
# 查找 Agent_0 的所有子代理进度
cat session.jsonl | jq 'select(.parentToolUseID=="Agent_0")'
```

### 如何提取思考内容

从 assistant 类型的 `thinking` 内容块：
```bash
cat session.jsonl | jq '.. | objects | select(.type=="thinking") | .thinking'
```

### 如何计算执行时间

比较相邻记录的时间戳：
```bash
cat session.jsonl | jq -s 'map(.timestamp) | {start: first, end: last}'
```

## 边界情况处理

1. **无子代理**: 如果提问没有触发 Agent 调用，只展示主会话的工具调用链
2. **子代理未结束**: 如果子代理仍在运行，标记为 "执行中"
3. **错误处理**: 如果工具返回错误，在报告中标记并显示错误信息
4. **超长内容**: 用户提问或工具输出过长时，显示摘要（前 200 字）

## 优化建议输出

在报告末尾，根据执行模式给出建议：

```markdown
## 优化建议

基于本次执行的分析：

1. **子代理并行度**: 本次使用了 4 个子代理并行，执行效率较高
2. **工具使用**: Bash 命令使用频繁，可以考虑封装为 Skill
3. **Token 效率**: 缓存命中率较高（xx%），说明复用了上下文
4. **潜在优化**: 某些子代理任务可以进一步拆分，提高细粒度并行
```
