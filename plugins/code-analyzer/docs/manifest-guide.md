# Manifest 使用规则

本文档定义 manifest.md 的维护规则和使用方法。

## 1. Manifest 文件位置

**固定路径：** `./docs/code-analyzer/manifest.md`

## 2. Manifest 结构

```markdown
# Code Analyzer 文档清单

## 文档列表

| 文档 | 分析范围 | 分析类型 | 生成时间 | 简要说明 |
|------|----------|----------|----------|----------|
| [root-full-scan.md](./root-full-scan.md) | `.` | full-scan | 2025-03-20 14:30 | 项目整体结构扫描 |
| [src-structure.md](./src-structure.md) | `./src` | structure | 2025-03-20 15:00 | 源代码结构分析 |

## 快速导航

### 按分析类型
- **整体扫描**: [root-full-scan.md](./root-full-scan.md)
- **结构分析**: [src-structure.md](./src-structure.md)
- **流程分析**: (暂无)

### 按分析范围
- **root (.)**: [root-full-scan.md](./root-full-scan.md)
- **src**: [src-structure.md](./src-structure.md)

---
*最后更新: 2025-03-20 15:30*
```

## 3. 文档列表格式

### 表格列说明

| 列名 | 说明 | 格式 |
|------|------|------|
| 文档 | 文档链接 | `[{doc_name}](./{doc_name})` |
| 分析范围 | 分析的目标路径 | 原始路径，如 `./src` |
| 分析类型 | 分析类型 | `full-scan` / `structure` / `flow` |
| 生成时间 | 文档生成时间 | `YYYY-MM-DD HH:MM` |
| 简要说明 | 文档内容摘要 | 一句话描述，最长50字 |

### 添加新记录

当生成新文档时，在表格中添加新行：

```markdown
| [{doc_name}](./{doc_name}) | `{scope}` | {type} | {YYYY-MM-DD HH:MM} | {摘要} |
```

### 更新已有记录

当覆盖已有文档时，更新对应行的时间和摘要：

```markdown
<!-- 旧记录 -->
| [src-structure.md](./src-structure.md) | `./src` | structure | 2025-03-20 10:00 | 源代码结构分析 |

<!-- 更新后 -->
| [src-structure.md](./src-structure.md) | `./src` | structure | 2025-03-20 15:00 | 源代码结构分析（重新分析） |
```

## 4. 快速导航维护

### 按分析类型分组

列出每种类型的文档链接：

```markdown
### 按分析类型
- **整体扫描**: [root-full-scan.md](./root-full-scan.md), [src-full-scan.md](./src-full-scan.md)
- **结构分析**: [src-structure.md](./src-structure.md), [render-structure.md](./render-structure.md)
- **流程分析**: [src-render-flow.md](./src-render-flow.md)
```

### 按分析范围分组

列出每个范围的文档链接：

```markdown
### 按分析范围
- **root (.)**: [root-full-scan.md](./root-full-scan.md)
- **src**: [src-full-scan.md](./src-full-scan.md), [src-structure.md](./src-structure.md)
- **src/render**: [render-structure.md](./render-structure.md), [src-render-flow.md](./src-render-flow.md)
```

## 5. 使用场景

### 场景1：检查是否已有分析

在执行分析前，检查 manifest 中是否已有相同 scope 和 type 的分析：

```markdown
1. 读取 manifest.md
2. 在文档列表中查找 scope={scope} 且 type={type} 的记录
3. 如存在，可提示用户已存在分析，询问是否重新分析
4. 如不存在，执行新分析
```

### 场景2：查找相关分析

在执行模块分析前，查找该范围的其他分析：

```markdown
1. 读取 manifest.md
2. 在文档列表中查找 scope 包含或等于当前 scope 的记录
3. 读取相关分析文档，避免重复工作
4. 基于已有分析进行增量分析
```

### 场景3：生成分析计划

根据 manifest 生成下一步分析建议：

```markdown
1. 读取 manifest.md
2. 分析已有文档的分布
3. 识别未分析的范围或类型
4. 建议用户进行补充分析
```

## 6. 维护规则

### 初始化

如果 manifest.md 不存在，创建初始模板：

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
- **模块分析**: (暂无)

### 按分析范围
- **root (.)**: (暂无)

---
*最后更新: {YYYY-MM-DD HH:MM}*
```

### 更新时机

- **生成新文档后**：立即添加新记录
- **覆盖旧文档后**：更新时间和摘要
- **删除文档后**：删除对应记录

### 更新步骤

1. 读取 manifest.md
2. 定位到文档列表表格
3. 添加或更新行
4. 更新快速导航
5. 更新最后更新时间
6. 写回 manifest.md

## 7. 简要说明提取

从生成的文档中提取简要说明：

```markdown
1. 读取生成的文档内容
2. 提取第一行标题（去掉 #）
3. 或提取 "1. 项目概览" / "1. 目录结构" / "1. 初始化流程" 后的第一段文字
4. 限制长度在50字以内
5. 如有必要，添加 "(更新)" 标记
```

## 8. 示例

### 完整的 Manifest 示例

```markdown
# Code Analyzer 文档清单

## 文档清单

| 文档 | 分析范围 | 分析类型 | 生成时间 | 简要说明 |
|------|----------|----------|----------|----------|
| [root-full-scan.md](./root-full-scan.md) | `.` | full-scan | 2025-03-20 14:30 | 项目整体结构扫描，识别出5个核心模块 |
| [src-structure.md](./src-structure.md) | `./src` | structure | 2025-03-20 15:00 | 源代码结构分析，发现3处循环依赖 |
| [src-render-flow.md](./src-render-flow.md) | `./src/render` | flow | 2025-03-20 16:00 | 渲染流程分析，绘制管线流程图 |

## 快速导航

### 按分析类型
- **整体扫描**: [root-full-scan.md](./root-full-scan.md)
- **结构分析**: [src-structure.md](./src-structure.md)
- **流程分析**: [src-render-flow.md](./src-render-flow.md)

### 按分析范围
- **root (.)**: [root-full-scan.md](./root-full-scan.md)
- **src**: [src-structure.md](./src-structure.md)
- **src/render**: [src-render-flow.md](./src-render-flow.md)

---
*最后更新: 2025-03-20 17:00*
```
