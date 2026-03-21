---
name: cclog-analyzer
description: |
  分析当前 Claude Code 会话的执行日志，追溯用户提问的完整执行流程。
  在用户询问"分析这次执行"、"查看刚才的执行过程"、"这次 Claude 是怎么处理的"时触发。
allowed-tools: Read, Glob, Bash(python *), AskUserQuestion
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

### 步骤 2：调用脚本获取用户提问列表

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/find_and_list_prompts.py ~/.claude/projects/{encoded-path}
```

**脚本功能：**
- 自动找到最新的 `.jsonl` 会话日志文件
- 提取其中所有 `type: "user"` 的记录

**脚本输出格式：**
```
session-file.jsonl|line-num|uuid|timestamp|content-preview
```

### 步骤 3（⚠️ 关键）：强制用户选择提问

解析步骤2的输出，使用 `AskUserQuestion` 展示列表：

```
请选择要分析的执行记录：

1. [2026-03-14 13:05:04] 这是 bullet 物理引擎代码，我希望借助 claude code...
2. [2026-03-14 13:30:12] 请分析 LinearMath 模块的 btVector3 类实现...
3. [2026-03-14 14:00:45] 帮我找出碰撞检测相关的核心文件...
```

**要求：**
- 必须等待用户明确选择后才能继续
- 不允许自动选择
- 获取用户选择项的 `uuid` 和 `session-file`

### 步骤 4：深度遍历提取完整执行树

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/extract_deep_execution.py \
  ~/.claude/projects/{encoded-path} \
  {session-file} \
  {selected-uuid}
```

**脚本功能（深度优先遍历）：**
1. 从目标提问开始顺序遍历主会话日志
2. 遇到子代理调用时，**立即**读取并输出子代理日志
3. 子代理日志输出完成后，**返回**主会话继续遍历
4. 保持完整的执行时序

**脚本输出格式：**
```
SOURCE|{完整的 JSON 行}
```

其中 SOURCE 为：
- `MAIN` - 主会话记录
- `agent-{id}` - 子代理记录

### 步骤 5：深度遍历输出分析报告

按步骤4的输出顺序，逐行解析并生成报告。**一条日志对应一个分析条目。**

**输出格式：**

```markdown
# Claude Code 执行过程分析

## 用户提问
**会话**: {session-file}
**UUID**: {selected-uuid}

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
{子代理的第 2 条记录 (tool_use Bash)}
```
**解析**: 子代理执行 Bash 命令

### 记录 6 [agent-xxx]
```json
{子代理的第 3 条记录 (tool_result)}
```
**解析**: Bash 命令返回结果

### 记录 7 [agent-xxx]
```json
{子代理的最后一条记录}
```
**解析**: 子代理完成，返回结果

### 记录 8 [MAIN]
```json
{主会话的 tool_result JSON}
```
**解析**: 收到子代理返回结果

### 记录 9 [MAIN]
```json
{主会话的下一个 tool_use}
```
**解析**: 主会话继续执行下一个工具

...（继续深度遍历）

### 记录 N [MAIN]
```json
{最终的 assistant 回复}
```
**解析**: Claude 向用户返回最终结果

---

## 执行统计
| 指标 | 数值 |
|------|------|
| 总记录数 | X |
| 主会话记录数 | X |
| 子代理数量 | X |
| 各子代理记录数 | agent-xxx: X, agent-yyy: Y |
| 总执行时间 | 首条到最后一条的时间差 |
```

## 日志格式参考

详细规范请参阅：`${CLAUDE_PLUGIN_ROOT}/docs/log-format-spec.md`

关键字段：
- `type`: user/assistant/progress
- `uuid`: 唯一标识
- `parentUuid`: 父节点
- `timestamp`: 时间戳
- `data.agentId`: 子代理标识

## 重要原则

1. **深度优先**：遇到子代理调用，立即处理完子代理全部记录，再返回主会话
2. **一条日志一个分析**：不合并、不跳过任何记录
3. **完整输出**：所有 JSON 和 content/prompt 都完整展示
