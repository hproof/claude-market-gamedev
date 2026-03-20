---
name: update-manifest
description: |
  维护 Code Analyzer 的文档清单（manifest.md）。
  在分析任务完成后由 analyst agent 调用，负责新增/更新/删除文档记录。
  不应由用户直接触发。
allowed-tools: Read, Write, Glob
disable-model-invocation: true
---

维护 `./docs/code-analyzer/manifest.md` 文档清单。

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | string | 否 | 操作类型：`add`（默认）/ `update` / `delete` / `rebuild` |
| `doc_name` | string | 条件 | 文档文件名（如 `src-structure.md`），`rebuild` 时不需要 |
| `scope` | string | 条件 | 分析范围（如 `./src`），`rebuild` 时不需要 |
| `type` | string | 条件 | 分析类型（`full-scan` / `structure` / `flow`），`rebuild` 时不需要 |
| `summary` | string | 条件 | 简要说明（限 50 字），`rebuild` 时不需要 |

`rebuild` 操作不需要以上条件参数，它会自动从文件中提取所有信息。

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
| `rebuild` | 扫描目录，从文件中提取信息，重建整个清单（见下方详细流程） |

### 3. 更新快速导航

根据文档列表中的所有记录，重新生成"按分析类型"和"按分析范围"的导航索引。

### 4. 更新时间戳

更新底部的 `*最后更新: {YYYY-MM-DD HH:MM}*` 时间戳。

## Rebuild 流程

当 `action` 为 `rebuild` 时，执行以下步骤：

### R1. 扫描文档目录

使用 `Glob` 扫描 `./docs/code-analyzer/*.md`，排除 `manifest.md` 本身。

### R2. 解析每个文档

对每个扫描到的 `.md` 文件：

**从文件名反向提取 scope 和 type：**

文件命名格式为 `{normalized-scope}-{type}.md`，其中 type 是最后一段已知类型标识。

解析规则：
1. 去掉 `.md` 后缀
2. 从末尾匹配已知类型标识：`full-scan`、`structure`、`flow`
3. 剩余部分为 normalized-scope，将 `root` 还原为 `.`，将 `-` 还原为 `/`，加前导 `./`

| 文件名 | type | scope |
|--------|------|-------|
| `root-full-scan.md` | `full-scan` | `.` |
| `src-structure.md` | `structure` | `./src` |
| `src-render-flow.md` | `flow` | `./src/render` |

如文件名无法匹配已知类型，跳过该文件并在结果中报告。

**从文件内容提取信息：**

- **生成时间**：读取文件末尾，匹配 `*生成时间: {YYYY-MM-DD HH:MM}*`
- **摘要**：读取文件标题（第一个 `#` 行），结合 scope 生成简要说明（限 50 字）

### R3. 重建 Manifest

丢弃旧的文档列表，用扫描结果重新生成完整的 manifest（模板 + 文档列表 + 快速导航 + 时间戳）。

### R4. 报告结果

返回重建摘要：发现 N 个文档，跳过 M 个无法识别的文件（如有）。

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
