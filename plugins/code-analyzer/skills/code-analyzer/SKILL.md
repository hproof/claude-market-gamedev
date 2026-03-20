---
name: code-analyzer
description: |
  启动代码审计工作流。
  当用户输入 /code-analyzer 或说"分析代码"、"审计项目"时触发。
  适用于：启动代码审查、架构评估、技术债务分析。
---

启动代码审计工作流，解析分析范围和分析类型，调用 developer subagent 执行分析。

## 参数提取

从用户输入中提取以下参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `scope` | 分析范围（目标代码路径） | `.`（当前目录） |
| `type` | 分析类型 | 未指定时询问用户 |

### 参数解析规则

1. **分析范围 (`scope`)**
   - 第一个参数如果以 `/`、`.` 开头或是相对路径 → 作为 `scope`
   - 如果没有路径参数 → 默认为 `.`

2. **分析类型 (`type`)**
   - 第二个参数匹配分析类型关键词 → 作为 `type`
   - 如果未指定或无法识别 → **询问用户**

## 分析类型

| 分析类型 | 说明 | 使用的 Skill | 输出文档 |
|----------|------|-------------|----------|
| `full-scan` | 整体扫描 | `full-scan` | `{scope}-full-scan.md` |
| `structure` | 结构分析 | `structure-analyzer` | `{scope}-structure.md` |
| `flow` | 流程分析 | `flow-analyzer` | `{scope}-flow.md` |

**说明：**
- `full-scan`：快速扫描项目整体结构，识别模块边界和层级关系
- `structure`：分析代码结构、类关系、依赖关系
- `flow`：分析关键流程（初始化、主循环、网络同步等）

## 输出目录和文档规范

### 固定输出目录

所有分析文档保存到：`./docs/code-analyzer/`

### 文档命名规则

详见 `plugins/code-analyzer/docs/document-spec.md`

### Manifest 文件

详见 `plugins/code-analyzer/docs/manifest-guide.md`

## 工作流程

### 1. 解析参数

```
/code-analyzer ./src full-scan
        ↑           ↑
      scope        type
```

### 2. 确认分析类型（如未指定）

```
请选择分析类型：
1. full-scan - 整体扫描：快速了解项目结构和模块分布
2. structure - 结构分析：深入分析代码结构和依赖关系
3. flow - 流程分析：分析关键执行流程（初始化、主循环等）
```

### 3. 计算文档名称

```python
# 伪代码
doc_name = normalize(scope) + "-" + type + ".md"
# ./src + full-scan → src-full-scan.md
```

### 4. 创建 Developer SubAgent 执行分析

调用 `developer` Agent 执行分析任务，传递以下参数：

| 参数 | 值 |
|------|-----|
| `scope` | {scope} |
| `type` | {type} |
| `skill_name` | {skill_name} |
| `doc_name` | {doc_name} |
| `manifest_path` | `./docs/code-analyzer/manifest.md` |

执行流程详见 `agents/developer.md`。

### 5. 返回结果给用户

- 报告分析完成
- 输出文档路径
- 提示可查看 manifest.md 了解所有文档

## 使用示例

```
/code-analyzer                          # scope=., 询问 type
/code-analyzer ./src                    # scope=./src, 询问 type
/code-analyzer ./src full-scan          # 整体扫描
/code-analyzer ./src structure          # 结构分析
/code-analyzer ./src flow               # 流程分析
```

## 输出示例

执行 `/code-analyzer ./src full-scan` 后：

```
./docs/code-analyzer/
├── manifest.md           # 文档清单
└── src-full-scan.md      # 本次分析结果
```

执行 `/code-analyzer ./src structure` 后：

```
./docs/code-analyzer/
├── manifest.md
├── src-full-scan.md
└── src-structure.md      # 新增
```
