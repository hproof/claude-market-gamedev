---
name: cclog-analyzer
description: |
  分析当前 Claude Code 会话的执行日志，追溯用户提问的完整执行流程。
  在用户询问"分析这次执行"、"查看刚才的执行过程"、"这次 Claude 是怎么处理的"时触发。
allowed-tools: Read, Glob, Grep, Bash(*), AskUserQuestion
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

**推荐使用脚本（性能更好）：**
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/list_user_prompts.py {session-id}.jsonl
```

或手动使用 jq：
```bash
cat {session-id}.jsonl | jq -r 'select(.type=="user") | "\(.uuid)|\(.timestamp)|\(.message.content[0:100])"'
```

### 阶段 2：强制用户选择要分析的提问

**重要：必须等待用户选择后才能继续！**

使用 `AskUserQuestion` 工具展示用户提问列表。如果用户没有明确指定要分析哪个提问，必须弹出选择列表让用户选择，绝不能自动选择。

**强制选择要求：**
- 如果用户空参数调用此 skill，必须使用 AskUserQuestion 弹出选择框
- 必须等待用户做出明确选择后才能进入阶段 3
- 不允许基于任何启发式规则自动选择（如选择最新的、选择最长的等）

**选择列表格式：**
```
请选择要分析的执行记录：

1. [2026-03-14 13:05] 这是 bullet 物理引擎代码，我希望借助 claude code 来快速了解...
2. [2026-03-14 13:30] 请分析 LinearMath 模块的 btVector3 类实现...
3. [2026-03-14 14:00] 帮我找出碰撞检测相关的核心文件...
...
```

**获取选择结果：**
- 使用 AskUserQuestion 获取用户明确选择的索引
- 只有用户确认选择后，才能获取该提问的 `uuid` 进入下一阶段
- **禁止**：在没有用户选择的情况下自动进入阶段 3

### 阶段 3：构建执行树并分析

**3.1 提取完整执行树**

**推荐使用脚本（性能更好）：**
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/extract_execution_tree.py {session-id}.jsonl {prompt-uuid}
```

该脚本会：
- 找到目标提问及其所有后代节点
- 按时间戳排序输出所有相关记录
- 自动加载并附加子代理日志

**手动实现方式（如不使用脚本）：**

从用户提问的 `uuid` 开始，追踪所有后代节点：
- 使用 `parentUuid` 关联查找
- 收集所有相关的 `assistant`、`progress`、`tool_result` 记录
- 递归查找子节点的子节点（最多 100 层）

**3.2 识别子代理调用**

从 `progress` 类型记录中提取：
- `agentId`：子代理 ID
- `prompt`：子代理的任务描述
- `toolUseID` / `parentToolUseID`：调用链关系

**3.3 读取子代理日志**

对于每个子代理：
```
子代理日志路径: {session-id}/subagents/agent-{agentId}.jsonl
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

**输出原则：**
1. **每条日志记录对应一个独立步骤** - 不要将多条日志合并为一步输出
2. **所有传递的 prompt/content 完整输出** - 包括：
   - 调用 Agent 时的 `prompt` 参数
   - 调用 Skill 时的完整输入
   - 传递给子代理的所有 `content`
   - 不要摘要，保留完整原始内容
3. **按时间顺序严格输出** - 保持日志的时间先后顺序

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

**子代理任务描述**（完整内容）：
```
请探索 Bullet3 物理引擎的 src/LinearMath 目录，了解其代码结构和主要功能。这个模块是数学工具库，包含向量、矩阵等基础数学类。

请分析：
1. 目录结构和主要头文件/源文件
2. 核心类及其职责（如 btVector3, btMatrix3x3, btTransform 等）
3. 关键数学工具和数据结构
4. 文件间的依赖关系

请提供结构化的总结。
```

**Step 2.1**: 工具调用 - Bash (Bash_0)
- 命令: `ls -la D:/git_proj/bullet3/src/LinearMath`
- 结果: [成功] 列出 50+ 个文件

**Step 2.2**: 工具调用 - Glob (Glob_1)
- 模式: `src/LinearMath/**/*`
- 结果: 匹配到 57 个文件

**Step 2.3**: 工具调用 - Bash (Bash_2)
- 命令: `find ... -type d | head -50`
- 结果: [成功]

**Step 2.4**: 工具调用 - Read (Read_0)
- 文件: `src/LinearMath/btVector3.h`
- 结果: [成功] 读取文件内容

**Step 2.5**: 工具调用 - Read (Read_1)
- 文件: `src/LinearMath/btMatrix3x3.h`
- 结果: [成功] 读取文件内容

**子代理完成**: 返回结构化总结（完整内容输出）

---

### Step 3: 工具调用 - Agent (Agent_1)
**时间**: 13:05:18
**描述**: 探索 BulletCollision 模块
**输入参数**:
- subagent_type: Explore
- prompt: "请探索 Bullet3 物理引擎的 src/BulletCollision 目录..."

#### ↳ 子代理执行 (agentId: a00463737d01a6eee, 类型: Explore)

**子代理任务描述**（完整内容）：
```
请探索 Bullet3 物理引擎的 src/BulletCollision 目录，了解其碰撞检测系统的代码结构。

请分析：
1. 目录结构（BroadphaseCollision, NarrowPhaseCollision, CollisionShapes, CollisionDispatch 等子目录）
2. 核心类及其职责
3. 碰撞检测的主要流程
4. 各种碰撞形状（box, sphere, mesh 等）的组织方式

请提供结构化的总结。
```

**Step 3.1**: 工具调用 - Bash (Bash_0)
- 命令: `find /d/git_proj/bullet3/src/BulletCollision -type d | head -50`
- 结果: [成功]

**Step 3.2**: 工具调用 - Glob (Glob_1)
- 模式: `src/BulletCollision/**/*.h`
- 结果: 匹配到 80+ 个头文件

**Step 3.3**: 工具调用 - Read (Read_0)
- 文件: `src/BulletCollision/BroadphaseCollision/btBroadphaseInterface.h`
- 结果: [成功]

**子代理完成**: 返回结构化总结（完整内容输出）

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
