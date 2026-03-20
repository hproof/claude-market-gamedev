---
name: update-manifest
description: |
  维护 Code Analyzer 的文档清单（manifest.md）。
  在分析任务完成后由 developer agent 调用，负责新增/更新/删除文档记录。
  不应由用户直接触发。
allowed-tools: Read, Write
disable-model-invocation: true
---

维护 `./docs/code-analyzer/manifest.md` 文档清单。

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `doc_name` | string | 是 | 文档文件名（如 `src-structure.md`） |
| `scope` | string | 是 | 分析范围（如 `./src`） |
| `type` | string | 是 | 分析类型（`full-scan` / `structure` / `flow`） |
| `summary` | string | 是 | 简要说明，限 50 字以内 |
| `action` | string | 否 | 操作类型：`add`（默认）/ `update` / `delete` |

## 工作流程

### 1. 读取或创建 Manifest

- 如 `./docs/code-analyzer/manifest.md` 存在：读取并解析
- 如不存在：按初始化模板创建

### 2. 执行操作

根据 `action` 参数：

| action | 操作 |
|--------|------|
| `add` | 在文档列表中新增一行，更新快速导航 |
| `update` | 找到相同 `doc_name` 的行，更新时间和摘要 |
| `delete` | 删除对应 `doc_name` 的行，更新快速导航 |

### 3. 更新快速导航

根据文档列表中的所有记录，重新生成"按分析类型"和"按分析范围"的导航索引。

### 4. 更新时间戳

更新底部的 `*最后更新: {YYYY-MM-DD HH:MM}*` 时间戳。

## Manifest 模板

```markdown
# Code Analyzer 文档清单

## 文档列表

| 文档 | 分析范围 | 分析类型 | 生成时间 | 简要说明 |
|------|----------|----------|----------|----------|

## 快速导航

### 按分析类型
- **整体扫描**: (暂无)
- **结构分析**: (暂无)
- **流程分析**: (暂无)

### 按分析范围
- **root (.)**: (暂无)

---
*最后更新: {YYYY-MM-DD HH:MM}*
```

## 维护规则

### 文档列表行格式

```markdown
| [{doc_name}](./{doc_name}) | {scope} | {type} | {YYYY-MM-DD HH:MM} | {summary} |
```

### 快速导航格式

**按分析类型**：将同类型的文档链接归类到对应条目下。

```markdown
- **整体扫描**: [root-full-scan.md](./root-full-scan.md)
- **结构分析**: [src-structure.md](./src-structure.md), [core-structure.md](./core-structure.md)
- **流程分析**: (暂无)
```

**按分析范围**：将相同范围的文档链接归类。

```markdown
- **root (.)**: [root-full-scan.md](./root-full-scan.md)
- **src**: [src-structure.md](./src-structure.md)
```

### 类型显示名映射

| type | 显示名 |
|------|--------|
| `full-scan` | 整体扫描 |
| `structure` | 结构分析 |
| `flow` | 流程分析 |
