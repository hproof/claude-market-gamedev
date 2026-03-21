---
name: cclog-analyzer
description: |
  分析当前 Claude Code 会话的执行日志，追溯用户提问的完整执行流程。
  在用户询问"分析这次执行"、"查看刚才的执行过程"、"这次 Claude 是怎么处理的"时触发。
allowed-tools: Read, Glob, Bash(python *), AskUserQuestion
---

# Claude Code 执行日志分析器

## 执行步骤

### 步骤 1：获取用户提问列表

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/find_and_list_prompts.py
```

**注意：如果脚本执行失败（返回非0退出码或输出错误信息），则停止执行并告知用户。**

**输出格式：**
```
session-file.jsonl|line-num|uuid|timestamp|content-preview
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
python ${CLAUDE_PLUGIN_ROOT}/scripts/extract_deep_execution.py {session-file} {uuid}
```

**注意：如果脚本执行失败（返回非0退出码或输出错误信息），则停止执行并告知用户。**

**输出格式：**
```
SOURCE|{完整的 JSON 行}
```

- `MAIN` - 主会话记录
- `agent-{id}` - 子代理记录

### 步骤 4：深度遍历输出分析报告

逐行解析步骤3的输出，**一条日志对应一个分析条目**。

**输出格式：**

```markdown
# Claude Code 执行过程分析

## 用户提问
**会话**: {session-file}
**UUID**: {uuid}

---

## 执行过程（深度优先遍历）

### 记录 1 [MAIN]
```json
{完整的 user 类型 JSON}
```
**解析**: 用户输入问题

### 记录 2 [MAIN]
```json
{完整的 assistant thinking JSON}
```
**解析**: Claude 进行思考规划

### 记录 3 [MAIN]
```json
{完整的 tool_use (Agent) JSON}
```
**解析**: 调用子代理

### 记录 4 [agent-xxx]
```json
{子代理的第 1 条记录}
```
**解析**: 子代理开始执行

### 记录 5 [agent-xxx]
```json
{子代理的第 2 条记录}
```
**解析**: 子代理执行工具

### 记录 6 [agent-xxx]
```json
{子代理的第 3 条记录}
```
**解析**: 子代理收到结果

### 记录 7 [MAIN]
```json
{主会话收到子代理结果}
```
**解析**: 收到子代理返回结果，继续执行

...（继续深度遍历）

---

## 执行统计
| 指标 | 数值 |
|------|------|
| 总记录数 | X |
| 主会话记录数 | X |
| 子代理数量 | X |
| 各子代理记录数 | agent-xxx: X |
| 总执行时间 | 首条到最后一条的时间差 |
```

## 重要原则

1. **深度优先**：遇到子代理调用，立即处理完子代理全部记录，再返回主会话
2. **一条日志一个分析**：不合并、不跳过任何记录
3. **完整输出**：所有 JSON 和 content/prompt 都完整展示
