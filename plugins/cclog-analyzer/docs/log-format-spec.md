# Claude Code 日志格式规范

本文档详细说明 Claude Code 执行日志的文件组织结构和 JSON 记录格式。

## 文件组织结构

```
~/.claude/projects/{encoded-path}/
├── {session-id}.jsonl              # 主会话日志（JSON Lines 格式）
├── {session-id}/                   # 子代理目录（如存在 Agent 调用）
│   └── subagents/
│       ├── agent-{agentId}.jsonl       # 子代理日志（JSON Lines 格式）
│       └── agent-{agentId}.meta.json   # 子代理元数据
└── ...
```

### 项目目录名编码规则

项目目录名 `{encoded-path}` 是对工作目录完整路径的编码，用于确保跨平台有效的目录名。

**编码转换规则：**

| 原始字符 | 编码后 | 说明 |
|----------|--------|------|
| `:` (盘符分隔符) | `--` | 例如 `D:` → `D--` |
| `\` 或 `/` (路径分隔符) | `-` | 所有层级分隔符统一为 `-` |
| 连续多个分隔符 | 单个 `-` | 合并重复的 `-` |

**编码示例：**

| 原始路径 | 编码后目录名 |
|----------|--------------|
| `D:\git_proj\bullet3` | `D--git-proj-bullet3` |
| `D:\git_proj\claude-market-gamedev` | `D--git-proj-claude-market-gamedev` |
| `C:\Users\hproof` | `C--Users-hproof` |

**如何定位当前项目的日志目录：**

1. 获取当前工作目录（CWD），例如 `D:\git_proj\bullet3`
2. 按上述规则编码：`D--git-proj-bullet3`
3. 构建完整路径：`~/.claude/projects/D--git-proj-bullet3/`

### 命名规则

| 元素 | 格式 | 示例 |
|------|------|------|
| 会话日志文件 | `{uuid}.jsonl` | `4676cf56-a6b2-4e98-a748-4e08e5260daa.jsonl` |
| 会话目录 | `{uuid}/` | `4676cf56-a6b2-4e98-a748-4e08e5260daa/` |
| 子代理日志 | `agent-{agentId}.jsonl` | `agent-a00463737d01a6eee.jsonl` |
| 子代理元数据 | `agent-{agentId}.meta.json` | `agent-a00463737d01a6eee.meta.json` |

## JSON Lines 记录格式

每行一个 JSON 对象，包含以下通用字段：

### 通用字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | string | 消息类型：见下文 |
| `uuid` | string | 消息唯一标识（UUID） |
| `parentUuid` | string | 父消息ID，形成对话树结构 |
| `sessionId` | string | 会话ID（UUID） |
| `timestamp` | string | ISO 8601 格式时间戳（UTC） |
| `cwd` | string | 当前工作目录 |
| `gitBranch` | string | Git 分支名 |
| `version` | string | Claude Code 版本 |
| `userType` | string | 用户类型：`external` / `internal` |
| `permissionMode` | string | 权限模式：`default` / `restricted` |

## 消息类型详解

### 1. `type: "file-history-snapshot"` - 文件历史快照

会话开始时的初始状态记录。

```json
{
  "type": "file-history-snapshot",
  "messageId": "uuid",
  "snapshot": {
    "messageId": "uuid",
    "trackedFileBackups": {},
    "timestamp": "2026-03-14T05:05:04.815Z"
  },
  "isSnapshotUpdate": false
}
```

### 2. `type: "user"` - 用户输入

```json
{
  "type": "user",
  "uuid": "449b2d95-c538-4b69-ae02-8eb23efcd174",
  "parentUuid": null,
  "isSidechain": false,
  "promptId": "uuid",
  "message": {
    "role": "user",
    "content": "用户输入文本"
  },
  "timestamp": "2026-03-14T05:05:04.815Z",
  "permissionMode": "default",
  "userType": "external",
  "cwd": "D:\\git_proj\\bullet3",
  "sessionId": "4676cf56-a6b2-4e98-a748-4e08e5260daa",
  "version": "2.1.76",
  "gitBranch": "my_build_test"
}
```

### 3. `type: "assistant"` - AI 回复

包含工具调用信息。

```json
{
  "type": "assistant",
  "uuid": "b9a930d2-b643-48c4-badb-c3cf03ed204a",
  "parentUuid": "449b2d95-c538-4b69-ae02-8eb23efcd174",
  "isSidechain": false,
  "message": {
    "id": "chatcmpl-xxx",
    "type": "message",
    "role": "assistant",
    "content": [
      {
        "type": "thinking",
        "thinking": "思考内容...",
        "signature": ""
      },
      {
        "type": "text",
        "text": "回复文本"
      },
      {
        "type": "tool_use",
        "id": "Bash_0",
        "name": "Bash",
        "input": {
          "command": "ls -la",
          "description": "List directory"
        }
      }
    ],
    "model": "kimi-k2.5",
    "stop_reason": null,
    "stop_sequence": null,
    "usage": {
      "input_tokens": 18136,
      "output_tokens": 0,
      "cache_creation_input_tokens": 0,
      "cache_read_input_tokens": 0,
      "service_tier": "standard",
      "inference_geo": "not_available",
      "prompt_tokens": 18136,
      "cached_tokens": 0
    }
  },
  "timestamp": "2026-03-14T05:05:11.078Z",
  "userType": "external",
  "cwd": "D:\\git_proj\\bullet3",
  "sessionId": "4676cf56-a6b2-4e98-a748-4e08e5260daa",
  "version": "2.1.76",
  "gitBranch": "my_build_test"
}
```

#### Usage 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `input_tokens` | number | 输入 token 数 |
| `output_tokens` | number | 输出 token 数 |
| `prompt_tokens` | number | Prompt token 数（同 input） |
| `cached_tokens` | number | 缓存命中 token 数 |
| `cache_read_input_tokens` | number | 从缓存读取的输入 token |
| `cache_creation_input_tokens` | number | 创建缓存的输入 token |
| `service_tier` | string | 服务层级 |
| `inference_geo` | string | 推理地理位置 |

### 4. `type: "progress"` - Agent 执行进度

记录子代理的执行状态。

```json
{
  "type": "progress",
  "uuid": "45d62b28-8678-48f7-8727-7b51720ef9a6",
  "parentUuid": "80a84930-d9cc-483d-b6a6-1eb81f48c725",
  "isSidechain": false,
  "data": {
    "type": "agent_progress",
    "prompt": "Agent 的任务描述...",
    "agentId": "af0c9fe6a1e515033",
    "message": {
      "type": "user",
      "message": {
        "role": "user",
        "content": [...]
      },
      "uuid": "536cbca2-8db8-4ec3-9050-36cf5831c339",
      "timestamp": "2026-03-14T05:05:23.091Z"
    }
  },
  "toolUseID": "agent_chatcmpl-xxx",
  "parentToolUseID": "Agent_0",
  "timestamp": "2026-03-14T05:05:23.093Z",
  "userType": "external",
  "cwd": "D:\\git_proj\\bullet3",
  "sessionId": "4676cf56-a6b2-4e98-a748-4e08e5260daa",
  "version": "2.1.76",
  "gitBranch": "my_build_test",
  "slug": "keen-zooming-yao"
}
```

#### Progress 类型子分类

| `data.type` | 说明 |
|-------------|------|
| `agent_progress` | 子代理执行进度 |

### 5. 工具结果（嵌入在消息流中）

```json
{
  "type": "tool_result",
  "tool_use_id": "Bash_0",
  "content": "命令输出内容"
}
```

## 子代理元数据格式

文件路径：`{session-id}/subagents/agent-{agentId}.meta.json`

```json
{
  "agentType": "Explore"
}
```

### Agent 类型枚举

| 类型 | 说明 |
|------|------|
| `Explore` | 探索型 Agent，用于代码库探索 |
| `Plan` | 规划型 Agent，用于任务规划 |
| `general-purpose` | 通用型 Agent |

## 工具调用结构

### 常见工具类型

| 工具名 | 用途 |
|--------|------|
| `Bash` | 执行 shell 命令 |
| `Read` | 读取文件 |
| `Write` | 写入文件 |
| `Edit` | 编辑文件 |
| `Glob` | 文件模式匹配 |
| `Grep` | 内容搜索 |
| `Agent` | 调用子代理 |
| `Skill` | 调用 Skill |

### 工具调用 ID 格式

| 工具 | ID 格式 | 示例 |
|------|---------|------|
| Bash | `Bash_{n}` | `Bash_0`, `Bash_1` |
| Read | `Read_{n}` | `Read_0` |
| Agent | `Agent_{n}` | `Agent_0` |
| 子代理内部 | `Glob_{n}`, `Bash_{n}` | `Glob_1` |

## 关联关系

### 消息树结构

```
user (uuid: A)
└── assistant (uuid: B, parentUuid: A)
    └── tool_result (parentUuid: B)
    └── assistant (uuid: C, parentUuid: B)
        └── tool_result
```

### Agent 调用链

```
assistant (type: assistant, tool_use: Agent_0)
└── progress (type: agent_progress, parentToolUseID: Agent_0, toolUseID: agent_xxx)
    └── progress (agent internal tool call)
        └── tool_result
```

## 时间戳格式

- 格式：ISO 8601 UTC
- 示例：`2026-03-14T05:05:04.815Z`
- 精度：毫秒级

## 分析查询技巧

### 使用 jq 解析

```bash
# 统计记录总数
cat session.jsonl | jq -s 'length'

# 提取所有工具调用
cat session.jsonl | jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use") | .name' | sort | uniq -c

# 提取会话时间范围
cat session.jsonl | jq -s 'map(.timestamp) | {start: first, end: last}'

# 提取 Agent 调用
cat session.jsonl | jq -r 'select(.type=="progress") | .data.agentId' | sort | uniq -c

# 统计 Token 使用
cat session.jsonl | jq -s '[.[].message.usage? | select(. != null)] | reduce .[] as $u ({input: 0, output: 0}; {input: (.input + $u.input_tokens), output: (.output + $u.output_tokens)})'
```

### 使用 grep 快速搜索

```bash
# 统计某工具使用次数
grep '"name":"Bash"' session.jsonl | wc -l

# 查找特定 Agent 的所有记录
grep '"agentId":"af0c9fe6a1e515033"' session.jsonl

# 查找错误关键词
grep -i 'error\|failed\|exit code' session.jsonl
```

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-03 | 初始文档，基于 Claude Code 2.1.76 日志格式 |
