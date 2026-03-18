# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个用于游戏开发的 Claude Code 插件市场 (claude-market-gamedev)，用于管理和分发 Claude Code 插件。

## 项目结构

```
.claude-plugin/marketplace.json    # 市场配置：定义可用的插件列表
plugins/                           # 插件目录
└── code-analyzer/                 # 代码分析器插件
    ├── .claude-plugin/plugin.json # 插件元数据配置
    └── agents/code-analyzer.md    # Agent 定义文件
```

## 插件配置规范

### 市场配置 (`.claude-plugin/marketplace.json`)

```json
{
  "name": "claude-market-gamedev",
  "owner": { "name": "hproof" },
  "plugins": [
    {
      "name": "插件名称",
      "source": "./plugins/插件目录",
      "description": "插件描述"
    }
  ]
}
```

### 插件配置 (`plugins/{name}/.claude-plugin/plugin.json`)

```json
{
    "name": "插件名称",
    "description": "插件描述",
    "version": "1.0.0",
    "author": { "name": "作者" },
    "agents": ["agent名称"]  // 需要显式声明agents
}
```

**注意**：
- `skills` 不需要在 `plugin.json` 中注册，放在 `skills/` 目录下自动发现
- `agents` 必须在 `plugin.json` 的 `agents` 数组中显式声明

### Agent 定义 (`plugins/{name}/agents/{agent-name}.md`)

Agent 文件使用 frontmatter 格式：

```yaml
---
name: agent名称
description: |
  使用说明，支持多行
model: inherit
color: orange
memory: project
---

Agent 指令内容...
```

## 开发工作流

此项目为纯配置项目，无需构建、测试或打包。

### 添加新插件

1. 在 `plugins/` 下创建新目录
2. 创建 `.claude-plugin/plugin.json` 配置文件
3. 创建 `agents/` 或 `skills/` 目录并添加定义文件
4. 更新 `.claude-plugin/marketplace.json` 注册新插件

### 验证配置

检查 JSON 文件格式：
```bash
node -e "JSON.parse(require('fs').readFileSync('.claude-plugin/marketplace.json'))" && echo "Valid JSON"
```

## Git 忽略规则

项目使用 `.gitignore` 忽略以下文件：
- OS 生成文件（`.DS_Store`、`Thumbs.db` 等）
- IDE 配置文件（`.idea/`、`.vscode/`、vim swap 文件等）
- 日志文件（`*.log`）
