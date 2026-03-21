# CLAUDE.md

游戏开发 Claude Code 插件市场。

## 项目结构

```
.claude-plugin/marketplace.json       # 市场配置（注册所有插件）
plugins/{plugin-name}/
├── .claude-plugin/plugin.json        # 插件元数据
├── agents/{agent-name}.md            # Agent 定义（自动发现）
├── skills/{skill-name}/SKILL.md      # Skill 定义（自动发现）
└── docs/                             # 插件文档（可选）
```

## 配置规范

### marketplace.json

```json
{
  "name": "市场名称",
  "owner": { "name": "作者" },
  "plugins": [
    { "name": "插件名", "source": "./plugins/目录", "description": "描述" }
  ]
}
```

### plugin.json

```json
{
  "name": "插件名",
  "description": "描述",
  "version": "1.0.0",
  "author": { "name": "作者" }
}
```

### Skill 定义

```yaml
---
name: skill-name
description: |
  做什么、何时触发、适用场景。
allowed-tools: Read, Write, Glob, Grep, Bash(find *)
---

Skill 指令内容...
```

| 字段 | 必需 | 说明 |
|------|------|------|
| `name` | 推荐 | 标识符，与目录名一致。省略则用目录名 |
| `description` | 推荐 | Claude 据此判断何时使用该 Skill |
| `allowed-tools` | 否 | Skill 激活时免审批的工具列表 |
| `disable-model-invocation` | 否 | `true` 则只能用户手动 `/name` 触发 |
| `user-invocable` | 否 | `false` 则不在 `/skills` 列表中显示（仅供 Agent 调用） |
| `context` | 否 | `fork` 在独立子上下文中执行 |
| `agent` | 否 | `context: fork` 时使用的 Agent 类型 |

### Agent 定义

```yaml
---
name: agent-name
description: 何时委派给此 Agent
model: inherit
tools: Read, Write, Glob, Grep, Skill(my-skill *)
---

Agent 系统提示...
```

| 字段 | 必需 | 说明 |
|------|------|------|
| `name` | 是 | 唯一标识符，小写字母和连字符 |
| `description` | 是 | Claude 据此决定何时委派 |
| `model` | 否 | `sonnet` / `opus` / `haiku` / `inherit` |
| `tools` | 否 | 可用工具白名单，省略则继承全部 |
| `disallowedTools` | 否 | 工具黑名单 |
| `memory` | 否 | `project` 启用跨会话记忆 |
| `skills` | 否 | 启动时预加载的 Skill 列表 |
| `maxTurns` | 否 | 最大执行轮数 |

**插件 Agent 限制：** 不支持 `hooks`、`mcpServers`、`permissionMode` 字段。

### 工具权限格式

```
Tool                    # 匹配该工具所有调用
Tool(specifier)         # 精确匹配
Tool(prefix *)          # 通配符匹配
```

常用示例：

| 格式 | 含义 |
|------|------|
| `Read` | 读取任意文件 |
| `Write` | 写入任意文件 |
| `Glob` | 文件名搜索 |
| `Grep` | 内容搜索 |
| `Bash(find *)` | 执行 find 命令 |
| `Bash(wc *)` | 执行 wc 命令 |
| `Agent(name)` | 调用指定 Agent |
| `Skill(name *)` | 调用指定 Skill |
