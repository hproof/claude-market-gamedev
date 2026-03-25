# Claude Code Marketplace 规范

## 目录结构

```
<marketplace-name>/
├── .claude-plugin/
│   └── marketplace.json      # 市场清单
├── plugins/                   # 插件目录
│   ├── plugin-a/
│   └── plugin-b/
└── docs/                      # 市场文档
```

## Marketplace 清单

`marketplace.json` 定义市场的元数据和插件列表：

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Owner Name"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "插件描述"
    }
  ]
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| name | 是 | Marketplace 标识符 |
| owner | 是 | 所有者信息 |
| plugins | 是 | 插件列表 |

### 插件条目

| 字段 | 必填 | 说明 |
|------|------|------|
| name | 是 | 插件名称 |
| source | 是 | 相对于 marketplace 根目录的路径 |
| description | 否 | 插件描述 |

## 相关文档

- [插件开发规范](plugins-reference.md)
- [Skill 系统](skills.md)
- [子 Agent 配置](sub-agents.md)
