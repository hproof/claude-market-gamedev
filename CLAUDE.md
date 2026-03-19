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

### 4. Skill 定义 `skills/{skill-name}/SKILL.md`

**必须以 YAML 前置元数据开头**，包含 name 和 description：

```yaml
---
name: skill名称
description: |
  Skill 的简要描述。
  触发条件说明（当用户输入 /xxx 或说"xxx"时触发）。
  适用场景说明。
---

Skill 使用说明和执行逻辑...
```

**YAML 字段说明：**
- `name` - Skill 标识符（必需），与目录名保持一致
- `description` - Skill 描述（必需），支持多行，包含触发条件和适用场景

**注意：** YAML 前置元数据以 `---` 开始和结束，这是解析 Skill 的关键标记。

## 开发工作流

1. 在 `plugins/` 下创建新目录
2. 创建 `.claude-plugin/plugin.json` 配置文件
3. 创建 `agents/` 或 `skills/` 目录并添加定义文件
4. 更新 `.claude-plugin/marketplace.json` 注册新插件

## 验证配置

```bash
node -e "JSON.parse(require('fs').readFileSync('.claude-plugin/marketplace.json'))" && echo "Valid JSON"
```
