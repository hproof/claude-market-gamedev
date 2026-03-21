# Claude Code 日志格式规范

本文档说明 cclog-analyzer skill 所需的日志格式信息。

## 文件组织结构

```
~/.claude/projects/{encoded-path}/
├── {session-id}.jsonl              # 主会话日志
└── {session-id}/
    └── subagents/
        └── agent-{agentId}.jsonl   # 子代理日志
```

### 项目目录名编码

将当前工作目录中的 `:` `\` `/` `_` 替换为 `-`。

**示例：**
- `D:\git_proj\bullet3` → `D--git-proj-bullet3`

## 关键字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | string | 消息类型：user/assistant/progress |
| `uuid` | string | 消息唯一标识 |
| `parentUuid` | string | 父消息ID，用于构建执行链 |
| `timestamp` | string | ISO 8601 格式时间戳 |
| `data.agentId` | string | 子代理标识（progress类型） |

## 消息类型

### user - 用户输入
```json
{
  "type": "user",
  "uuid": "...",
  "message": {"content": "..."},
  "timestamp": "..."
}
```

### assistant - AI回复
包含 thinking 和 tool_use：
```json
{
  "type": "assistant",
  "uuid": "...",
  "parentUuid": "...",
  "message": {
    "content": [
      {"type": "thinking", "thinking": "..."},
      {"type": "tool_use", "name": "Agent", "input": {...}}
    ]
  }
}
```

### progress - Agent执行进度
标识子代理调用：
```json
{
  "type": "progress",
  "parentUuid": "...",
  "data": {
    "agentId": "xxx",
    "type": "agent_progress"
  }
}
```

## 子代理日志路径

```
{session-id}/subagents/agent-{agentId}.jsonl
```

子代理日志格式与主会话相同。

## 脚本输出格式

`find_and_list_prompts.py` 和 `extract_deep_execution.py` 会简化原始日志，输出精简后的 JSON：

### find_and_list_prompts 输出

```
session-file.jsonl|timestamp|content-preview|uuid
```

### extract_deep_execution 输出

```json
{"type": "user", "message": {"role": "user", "content": "..."}, "timestamp": "...", "_source": "MAIN"}
{"type": "assistant", "message": {"role": "assistant", "content": [{"type": "thinking", "thinking": "..."}]}, "timestamp": "...", "_source": "MAIN"}
{"type": "assistant", "message": {"role": "assistant", "content": [{"type": "tool_use", "id": "...", "name": "...", "input": {...}}]}, "timestamp": "...", "_source": "MAIN"}
```

### 简化规则

脚本会移除以下冗余字段：
- `uuid`, `parentUuid`, `sessionId` - ID 类字段
- `usage`, `model`, `stop_reason`, `stop_sequence` - 元数据
- `isSidechain`, `userType`, `entrypoint`, `cwd` - 执行环境
- `version`, `gitBranch`, `slug` - 版本信息
- `permissionMode`, `promptId`, `sourceToolAssistantUUID` - 内部标识

只保留核心字段：
- `type` - 记录类型
- `message.role` / `message.content` - 角色和内容
- `timestamp` - 时间戳
- `_source` - 来源标识（"MAIN" 或 "agent-{id}"）
