---
name: cclog-analyzer
description: |
  分析当前 Claude Code 会话的执行日志，追溯用户提问的完整执行流程。
  在用户询问"分析这次执行"、"查看刚才的执行过程"、"这次 Claude 是怎么处理的"时触发。
allowed-tools: Read, Glob, Bash(python *), AskUserQuestion, Write
---

# Claude Code 执行日志分析器

## 执行步骤

### 步骤 0：接收可选参数

用户可能提供关键词参数，格式：
- `/cclog-analyzer` - 无参数，显示所有提问
- `/cclog-analyzer 简化` - 有参数，过滤包含"简化"的提问

### 步骤 1：输出当前会话ID

开始执行时，首先向用户显示当前会话ID：

```
当前会话 ID: ${CLAUDE_SESSION_ID}
```

### 步骤 2：获取用户提问列表

**调用方式（必须传入当前会话 ID）：**
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/find_and_list_prompts.py ${CLAUDE_SESSION_ID}
```

**输出格式：**
```
timestamp|content-preview|uuid
```

### 步骤 3：过滤与选择

**如果用户提供了参数（关键词）：**
1. 用关键词匹配所有提问的 `content-preview`
2. 匹配结果：
   - **1个匹配** → 直接使用，跳过选择
   - **多个匹配** → 只展示匹配项，让用户选择
   - **0个匹配** → 提示"未找到匹配，显示所有提问"，然后展示全部让用户选择

**如果用户未提供参数：**
- 展示所有提问，让用户选择

**⚠️ 重要：不要让 AI 去搜索日志文件**

如果过滤后没有匹配项，**展示所有候选让用户选择**，禁止 AI 自己用 grep 等工具去搜索日志文件。

### 步骤 4：生成执行流程 Markdown

**调用方式：**
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/extract_deep_execution.py ${CLAUDE_SESSION_ID} {prompt-uuid}
```

**输出格式：**
直接输出 Markdown 格式的执行流程表格：

```markdown
# Claude Code 执行日志分析

**会话**: xxx-xxx-xxxx
**用户提问**: 简化cclog-analyzer插件...
**分析时间**: 2026-03-23 10:30:00
**记录总数**: 45 (主会话: 25, 子代理: 20)

---

## 执行流程

| 序号 | 来源 | 类型 | 摘要 |
|------|------|------|------|
| 1 | MAIN | user | 用户提问: 简化cclog-analyzer插件，让它直接返回markdown... |
| 2 | MAIN | thinking | AI思考: 用户想要修改extract_deep_execution脚本... |
| 3 | MAIN | tool_use | Read: G:/git_proj/claude-market-gamedev/plugins/cclog-analyzer/... |
| 4 | MAIN | tool_result | 结果: #!/usr/bin/env python3... |
| 5 | agent-xxx | user | 用户提问: 请分析下protocol目录下的内容 |

---

## 统计信息

| 指标 | 数值 |
|------|------|
| 总记录数 | 45 |
| 主会话记录 | 25 |
| 子代理记录 | 20 |
| user | 10 |
| thinking | 15 |
| tool_use | 12 |
| tool_result | 8 |
```

**输出说明：**
- 脚本直接生成 Markdown 格式表格
- `摘要` 列保留最多 150 字符，确保路径完整显示
- 超过 500 条记录会自动截断并添加提示

### 步骤 5：分析并生成最终报告

**处理方式：**
1. 读取步骤 4 生成的 Markdown 表格
2. 分析执行流程：
   - 识别主要阶段（用户提问 → AI思考 → 工具调用 → 子代理 → 最终回复）
   - 统计各类型记录数量
   - 识别关键工具调用（Read/Bash/Agent 等）
3. 生成分析报告，写入文件：

```
./docs/cclog-{日期时间}-{用户提问摘要}.md
```

**文件名示例：**
- `cclog-20260322-150530-简化ccloganalyzer.md`

**最终报告格式：**

```markdown
# Claude Code 执行分析报告

**会话**: xxx-xxx-xxxx
**用户提问**: 简化cclog-analyzer插件...
**分析时间**: 2026-03-23 10:35:00

---

## 执行摘要

本次执行共 X 步，涉及主会话和 X 个子代理。主要流程为：
1. 用户请求...
2. AI 启动子代理分析...
3. 子代理执行了 X 次工具调用...
4. 最终返回结果...

---

## 详细执行流程

[这里直接包含步骤4生成的Markdown表格]

---

## 关键步骤分析

### 阶段1：理解与规划
AI 首先分析了用户请求，识别出需要...

### 阶段2：工具调用
主要调用了以下工具：
- Read: 读取了 X 个文件
- Bash: 执行了 X 个命令
- Agent: 启动了 X 个子代理

### 阶段3：子代理执行
子代理 agent-xxx 完成了...工作

---

## 统计汇总

| 指标 | 数值 |
|------|------|
| 总记录数 | X |
| 主会话记录 | X |
| 子代理记录 | X |
| 工具调用次数 | X |
```

**完成报告后：**
告知用户报告已保存到 `{文件路径}`

## 重要原则

1. **脚本直接生成 Markdown**：使用 `--markdown` 参数让 Python 脚本直接输出表格
2. **AI 负责分析总结**：读取 Markdown 表格后，分析执行流程并生成最终报告
3. **保留完整路径**：摘要列保留 150 字符，确保文件路径完整显示
4. **输出到文件**：将分析结果写入 Markdown 文件，不要直接输出到对话
