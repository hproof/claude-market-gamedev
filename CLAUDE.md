# CLAUDE.md

游戏开发 Claude Code 插件市场配置指南。

## 项目结构

```
.claude-plugin/marketplace.json    # 市场配置
plugins/                           # 插件目录
└── {plugin-name}/                 # 单个插件
    ├── .claude-plugin/plugin.json # 插件配置
    ├── agents/                    # Agent 定义目录（自动发现）
    └── skills/                    # Skill 定义目录（自动发现）
```

## 配置规范

### 1. 市场配置 `.claude-plugin/marketplace.json`

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

### 2. 插件配置 `plugins/{name}/.claude-plugin/plugin.json`

```json
{
  "name": "插件名称",
  "description": "插件描述",
  "version": "1.0.0",
  "author": { "name": "作者" }
}
```

### 3. Agent 定义 `agents/{agent-name}.md`

```yaml
---
name: agent名称
description: 使用说明
model: inherit
color: orange
memory: project
---

Agent 指令内容...
```

## 开发工作流

1. 在 `plugins/` 下创建新目录
2. 创建 `.claude-plugin/plugin.json` 配置文件
3. 创建 `agents/` 或 `skills/` 目录并添加定义文件
4. 更新 `.claude-plugin/marketplace.json` 注册新插件

## 验证配置

```bash
node -e "JSON.parse(require('fs').readFileSync('.claude-plugin/marketplace.json'))" && echo "Valid JSON"
```
