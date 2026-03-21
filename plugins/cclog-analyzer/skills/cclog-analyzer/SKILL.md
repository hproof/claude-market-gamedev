---
name: cclog-analyzer
description: |
  分析当前 Claude Code 会话的执行日志，追溯用户提问的完整执行流程。
  在用户询问"分析这次执行"、"查看刚才的执行过程"、"这次 Claude 是怎么处理的"时触发。
allowed-tools: Read, Glob, Bash(python *), AskUserQuestion
---

# Claude Code 执行日志分析器

## 日志格式规范

分析日志前，请先阅读 `${CLAUDE_PLUGIN_ROOT}/docs/log-format-spec.md` 了解：
- 日志文件组织结构
- JSON Lines 记录格式
- 消息类型（user/assistant/progress）
- 关键字段（uuid, parentUuid, timestamp, agentId 等）
- 子代理日志位置

## 执行步骤

### 步骤 1：获取用户提问列表

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/find_and_list_prompts.py
```

**注意：如果脚本执行失败（返回非0退出码或输出错误信息），则停止执行并告知用户。**

**输出格式：**
```
session-file.jsonl|timestamp|content-preview|uuid
```

### 步骤 2（⚠️ 关键）：强制用户选择

使用 `AskUserQuestion` 展示列表，必须等待用户明确选择：

```
请选择要分析的执行记录：

1. [2026-03-14 13:05:04] 这是 bullet 物理引擎代码，我希望借助 claude code...
2. [2026-03-14 13:30:12] 请分析 LinearMath 模块的 btVector3 类实现...
3. [2026-03-14 14:00:45] 帮我找出碰撞检测相关的核心文件...
```

**获取：** `session-file` 和 `uuid`

### 步骤 3：深度遍历提取执行树

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/extract_deep_execution.py {session-file} {prompt-uuid}
```

**注意：如果脚本执行失败（返回非0退出码或输出错误信息），则停止执行并告知用户。**

**输出格式：**
每行一条 JSON 记录，已简化（无 uuid、usage 等冗余字段）：

```json
{"type": "user", "message": {"role": "user", "content": "..."}, "timestamp": "...", "_source": "MAIN"}
{"type": "assistant", "message": {"role": "assistant", "content": [...]}, "timestamp": "...", "_source": "agent-xxx"}
```

- `"_source": "MAIN"` - 主会话记录
- `"_source": "agent-{id}"` - 子代理记录

### 步骤 4：输出执行过程

逐行解析步骤3的 JSON 输出，每条记录输出一行：

**输出格式：**

分割线前后字符数相同（至少10个字符），中间包含序号和角色：

```
━━━━━━━━━━ 001 [USER] ━━━━━━━━━━
用户输入内容（完整显示）

━━━━━━━━━━━━ 002 [ASSISTANT] ━━━━━━━━━━━━
AI 回复内容

━━━━━━━━━━━ 003 [THINKING] ━━━━━━━━━━━
AI 思考过程

━━━━━━━━━━ 004 [TOOL_USE: Bash] ━━━━━━━━━━
命令: python test.py
参数摘要...

━━━━━━━━━━━ 005 [TOOL_RESULT] ━━━━━━━━━━━
工具返回结果（过长则截断）

━━━━━━━━━━ 006 [SUB:agent-xxx] [USER] ━━━━━━━━━━
（子代理收到的问题）

━━━━━━━━━━ 007 [SUB:agent-xxx] [ASSIST] ━━━━━━━━━━
（子代理的回复）

━━━━━━━━━━━━ 010 [ASSISTANT] ━━━━━━━━━━━━
主会话收到子代理结果后的继续处理
```

**输出规则：**

| 元素 | 格式 | 说明 |
|------|------|------|
| **分隔线** | `━━━━ 001 [USER] ━━━━` | 前后各至少10个字符，中间包含序号和角色 |
| **主会话** | `001 [USER]` / `002 [ASSISTANT]` | 序号+大写角色 |
| **子会话** | `006 [SUB:agent-xxx] [USER]` | 子代理带 `[SUB:xxx]` 前缀 |

**内容处理规则：**
- `USER` 类型：显示完整 `message.content`
- `ASSISTANT` 类型：显示完整 `message.content`
- `THINKING` 类型：显示 `thinking` 字段内容（AI 的思考过程）
- `TOOL_USE` 类型：显示 `name` + `input` 摘要
- `TOOL_RESULT` 类型：显示 `output` 摘要（超过500字符则截断显示 `... [截断，共XXX字符]`）
- **子代理记录**：每条前面加 `[SUB:agent-id]` 前缀，与主会话区分

## 重要原则

1. **深度优先**：遇到子代理调用，立即处理完子代理全部记录，再返回主会话
2. **分割线格式**：每条记录以 `━━━━ 001 [USER] ━━━━` 格式开始（前后各至少10个字符），序号和角色一眼识别
3. **子代理标识**：子代理记录使用 `[SUB:agent-xxx]` 前缀，与主会话明确区分
4. **完整内容**：用户输入和 AI 输出必须完整显示，不要截断（tool_result 过长可截断）
