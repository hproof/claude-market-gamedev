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

| 分析类型 | 说明 | 使用的 Skill |
|----------|------|-------------|
| `full-scan` | 宏观概览：快速扫描模块分布和层级关系，不深入依赖细节 | `full-scan` |
| `structure` | 深度结构：详细分析类关系、依赖关系、耦合度 | `structure-analyzer` |
| `flow` | 流程分析：追踪初始化、主循环、网络同步等关键流程 | `flow-analyzer` |

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
1. full-scan - 宏观概览：快速了解项目模块分布和层级关系
2. structure - 深度结构：详细分析类关系和模块依赖
3. flow - 流程分析：追踪关键执行流程（初始化、主循环等）
```

### 3. 计算文档名称

按以下命名规则标准化路径并拼接类型：

```
{normalized-scope}-{type}.md
```

**路径标准化：** 移除前导 `./` 或 `/`，将 `/` 替换为 `-`，`.` 转换为 `root`。

| 分析范围 | 分析类型 | 文档名 |
|----------|----------|--------|
| `.` | `full-scan` | `root-full-scan.md` |
| `./src` | `structure` | `src-structure.md` |
| `./src/render` | `flow` | `src-render-flow.md` |

### 4. 创建 Developer SubAgent 执行分析

调用 `developer` Agent 执行分析任务，传递以下参数：

| 参数 | 值 |
|------|-----|
| `scope` | {scope} |
| `type` | {type} |
| `skill_name` | {skill_name} |
| `doc_name` | {doc_name} |


### 5. 返回结果给用户

- 报告分析完成
- 输出文档路径
- 提示可查看 manifest.md 了解所有文档

## 容错处理

| 情况 | 处理方式 |
|------|----------|
| 目标路径不存在 | 提示用户路径无效，要求重新指定 |
| 代码库过大（>5万行） | 建议用户缩小 scope 到子目录，分批分析 |
| `.claudeignore` 不存在 | 正常执行，不忽略任何文件 |
| manifest.md 不存在 | 自动创建初始模板 |

## 使用示例

```
/code-analyzer                          # scope=., 询问 type
/code-analyzer ./src                    # scope=./src, 询问 type
/code-analyzer ./src full-scan          # 宏观概览
/code-analyzer ./src structure          # 深度结构分析
/code-analyzer ./src flow               # 流程分析
```
