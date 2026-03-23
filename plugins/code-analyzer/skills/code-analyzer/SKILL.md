---
name: code-analyzer
description: |
  启动代码分析工作流。支持两种模式：
  - 分析模式：当用户说"分析代码"、"审计项目"、"分析 XX 模块"等时触发，生成分析文档。
  - 询问模式：当用户提问"XX流程是怎样的？"、"XX模块依赖了什么？"等时触发，基于已有分析回答。
  将用户的原始查询转交给 analyst agent 进行智能处理。
allowed-tools: Agent(code-analyzer:analyst), Read
---

启动代码分析工作流的入口 Skill。

## 职责

本 Skill 仅作为入口层，职责极简：

1. 接收用户的原始输入
2. 启动 `analyst` agent，将原始查询完整传递
3. 返回 agent 的执行结果给用户

**不做**意图判断、参数解析、文档命名 — 这些全部由 `analyst` agent 负责。

## 工作流程

### 1. 接收用户输入

原样保留用户的完整查询文本，不做任何解析。

### 2. 启动 Analyst Agent

使用 `Agent` 工具调用 `analyst` agent：

```
Agent(code-analyzer:analyst)
  user_query: {用户的完整原始输入}
```

**注意**：
- 工具名是 `Agent`（不是 Bash 或其他）
- agent 名是 `analyst`
- 只传递 `user_query` 一个参数

### 3. 返回结果

将 agent 返回的结果原样呈现给用户。

## 使用示例

**分析模式：**

```
/code-analyzer                                    # agent 自行判断范围和类型
/code-analyzer ./src full-scan                    # 对 ./src 做整体扫描
/code-analyzer ./src/battle module                 # 对战斗模块做深度分析
/code-analyzer 分析战斗模块，重点关注初始化          # agent 解析自然语言
```

**询问模式：**

```
/code-analyzer 战斗流程是怎么样的？                  # 基于已有分析文档回答
/code-analyzer 渲染模块依赖了哪些底层模块？          # 查找 structure 文档回答
/code-analyzer 项目有哪些业务模块？                  # 查找 full-scan 文档回答
```
