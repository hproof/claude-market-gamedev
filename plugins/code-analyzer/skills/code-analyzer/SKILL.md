---
name: code-analyzer
description: |
  启动代码审计工作流。
  当用户输入 /code-analyzer 或说"分析代码"、"审计项目"、"分析 XX 模块"、"分析 XX 流程"等时触发。
  将用户的原始查询转交给 analyst agent 进行智能分析。
allowed-tools: Agent(analyst), Read
---

启动代码审计工作流的入口 Skill。

## 职责

本 Skill 仅作为入口层，职责极简：

1. 接收用户的原始输入
2. 启动 `analyst` agent，将原始查询完整传递
3. 返回 agent 的执行结果给用户

**不做**参数解析、文档命名、类型判断 — 这些全部由 `analyst` agent 负责。

## 工作流程

### 1. 接收用户输入

原样保留用户的完整查询文本，不做任何解析。

### 2. 启动 Analyst Agent

调用 `analyst` agent，传递：

| 参数 | 值 |
|------|-----|
| `user_query` | 用户的完整原始输入 |

### 3. 返回结果

将 agent 返回的分析结果原样呈现给用户，包括：
- 分析完成状态
- 输出文档路径
- 简要摘要
- 提示可查看 `./docs/code-analyzer/manifest.md` 了解所有文档

## 使用示例

```
/code-analyzer                                    # agent 自行判断范围和类型
/code-analyzer ./src                              # agent 识别范围为 ./src
/code-analyzer ./src full-scan                    # agent 识别范围和类型
/code-analyzer 分析战斗模块的流程，重点关注初始化    # agent 解析自然语言
```
