---
name: code-analyzer
description: |
  分析代码库架构并生成详细的架构文档。适用于以下场景：
  - 用户想要了解某个目录/模块的代码结构和设计
  - 新成员入职需要快速了解项目架构
  - 代码审查前需要评估架构设计
  - 技术债务分析和重构前的架构梳理
  - 准备技术分享文档
  - 用户询问"分析一下 X 模块的架构"、"X 目录的代码结构是怎样的"
  用户可以通过 /code-analyzer <目录路径> 直接调用。
disable-model-invocation: true
---

分析指定目录的代码库架构。

## 执行步骤

1. 获取用户要分析的目录路径（从参数 $ARGUMENTS 中解析）
2. 调用 code-analyzer agent，将目录路径作为任务传递给 agent
3. Agent 完成分析后，确认生成的架构文档路径

## Agent 调用方式

使用以下指令调用 code-analyzer agent：

```
使用 code-analyzer agent 分析目录：$ARGUMENTS

请按照 agent 的指令完成分析并生成架构文档。
```

## 输出说明

Agent 将生成包含以下内容的架构文档：
- 模块与目录结构分析
- 关键类与数据结构
- 核心流程梳理
- 接口与 API 层
- 架构评审（优点、缺点、风险点、可优化项）

文档保存路径：`doc/[目录名]-code-analyzer-[日期].md`
