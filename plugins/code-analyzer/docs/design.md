# Code Analyzer 插件设计方案

## 1. 设计目标

提供一套游戏代码分析工作流，支持多种分析类型（整体扫描、结构分析、流程分析），通过 manifest 实现跨会话记忆，避免重复分析。

## 2. 架构概览

```
用户输入
  │
  ▼
┌─────────────────────────────┐
│  code-analyzer skill（入口） │  接收原始输入，启动 agent
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────────────────────────┐
│              developer agent（主控）              │
│                                                  │
│  1. 读取 manifest.md（记忆）                      │
│  2. 分析用户需求（scope / type / modules / notes）│
│  3. 检查历史，询问是否覆盖                        │
│  4. 决定输出路径                                  │
│  5. 调用分析 skill                                │
│  6. 调用 update-manifest skill                    │
│  7. 返回结果                                      │
└───────┬───────────────┬───────────────┬──────────┘
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  full-scan   │ │  structure-  │ │    flow-     │
│    skill     │ │  analyzer    │ │   analyzer   │
│              │ │    skill     │ │    skill     │
│ 宏观概览     │ │ 深度结构     │ │ 流程追踪     │
└──────────────┘ └──────────────┘ └──────────────┘
                                         │
                        ┌────────────────┘
                        ▼
               ┌─────────────────┐
               │ update-manifest │
               │     skill       │
               │                 │
               │ 维护文档清单     │
               └─────────────────┘
```

## 3. 组件职责

### 3.1 code-analyzer skill（主控入口）

**定位**：唯一的用户交互入口，职责极简。

| 职责 | 说明 |
|------|------|
| 接收输入 | 保留用户的完整原始查询，不做任何解析 |
| 启动 agent | 将原始查询传递给 `developer` agent |
| 返回结果 | 将 agent 的执行结果原样呈现给用户 |

**不做**：参数解析、文档命名、类型判断。

### 3.2 developer agent（主控 Agent）

**定位**：核心调度中心，负责需求分析和任务编排。

| 职责 | 说明 |
|------|------|
| 记忆加载 | 启动时读取 `manifest.md`，了解历史分析记录 |
| 需求分析 | 从用户原始输入中提取 scope、type、modules、key_paths、notes |
| 历史检查 | 发现重复分析时询问用户是否覆盖 |
| 路径决策 | 根据 scope 和 type 计算输出文档路径 |
| 调度执行 | 调用对应的分析 skill |
| 记忆更新 | 分析完成后调用 `update-manifest` skill |

**需求解析维度**：

| 维度 | 提取方式 | 默认值 |
|------|----------|--------|
| 分析范围 (`scope`) | 路径参数 | `.` |
| 分析类型 (`type`) | 关键词匹配 | 询问用户 |
| 目标模块 (`modules`) | "XX模块"等 | 无 |
| 重点路径 (`key_paths`) | "主要代码位于"等 | 无 |
| 注意事项 (`notes`) | "重点关注"等 | 无 |

### 3.3 分析 Skills

三个分析 skill 各自聚焦不同的分析类型，由 agent 调度，输出位置由 agent 决定。

| Skill | 分析类型 | 触发关键词 | 说明 |
|-------|----------|-----------|------|
| `full-scan` | 整体扫描 | 整体、概览、扫描、全局 | 宏观概览：模块分布和层级关系 |
| `structure-analyzer` | 结构分析 | 结构、类关系、依赖、耦合 | 深度结构：类关系、依赖、耦合度 |
| `flow-analyzer` | 流程分析 | 流程、初始化、主循环、执行 | 流程追踪：关键执行流程分析 |

**统一输入参数**：

| 参数 | 说明 |
|------|------|
| `scope` | 分析范围（目录路径），由 agent 传入 |
| `output_file` | 输出文件路径，由 agent 决定 |

### 3.4 update-manifest skill（记忆维护）

**定位**：专职维护 manifest.md，不由用户直接触发。

| 职责 | 说明 |
|------|------|
| 创建清单 | manifest 不存在时按模板初始化 |
| 新增记录 | 分析完成后添加文档记录 |
| 更新记录 | 覆盖分析时更新时间和摘要 |
| 删除记录 | 文档被删除时移除对应记录 |
| 导航维护 | 自动更新"按类型"和"按范围"的快速导航 |

## 4. 核心流程

### 4.1 完整执行流程

```
用户: /code-analyzer ./src structure
         │
         ▼
    code-analyzer skill
         │ 传递原始查询
         ▼
    developer agent 启动
         │
         ├─ 1. 读取 manifest.md → 获取历史记录
         ├─ 2. 读取 spec.md → 了解规范
         ├─ 3. 解析需求 → scope=./src, type=structure
         ├─ 4. 检查历史 → 如有重复，询问用户
         ├─ 5. 决定路径 → src-structure.md
         ├─ 6. 调用 structure-analyzer skill
         ├─ 7. 调用 update-manifest skill
         └─ 8. 返回结果给用户
```

### 4.2 历史检查流程

```
发现已有 src-structure.md（2026-03-15）
         │
         ├─ 用户确认覆盖 → 重新分析，覆盖文档
         └─ 用户拒绝    → 终止分析，提示已有文档路径
```

### 4.3 文档命名规则

路径标准化：移除前导 `./` 或 `/`，将 `/` 替换为 `-`，`.` 转换为 `root`。

| 分析范围 | 分析类型 | 文档名 |
|----------|----------|--------|
| `.` | `full-scan` | `root-full-scan.md` |
| `./src` | `structure` | `src-structure.md` |
| `./src/render` | `flow` | `src-render-flow.md` |

## 5. 记忆机制

### 5.1 Manifest 结构

`./docs/code-analyzer/manifest.md` 作为插件的持久化记忆：

```markdown
# Code Analyzer 文档清单

## 文档列表

| 文档 | 分析范围 | 分析类型 | 生成时间 | 简要说明 |
|------|----------|----------|----------|----------|
| [src-structure.md](./src-structure.md) | ./src | structure | 2026-03-20 17:00 | ... |

## 快速导航

### 按分析类型
- **整体扫描**: ...
- **结构分析**: [src-structure.md](./src-structure.md)
- **流程分析**: (暂无)

### 按分析范围
- **src**: [src-structure.md](./src-structure.md)
```

### 5.2 记忆生命周期

| 时机 | 操作 |
|------|------|
| agent 启动 | 读取 manifest，加载历史记录 |
| 分析完成 | 调用 `update-manifest` 新增/更新记录 |
| 重复检查 | 基于 manifest 判断是否已有相同分析 |

## 6. 文件结构

```
plugins/code-analyzer/
├── .claude-plugin/
│   └── plugin.json              # 插件元数据
├── agents/
│   └── developer.md             # 主控 Agent
├── skills/
│   ├── code-analyzer/SKILL.md   # 主控入口 Skill
│   ├── full-scan/SKILL.md       # 整体扫描 Skill
│   ├── structure-analyzer/SKILL.md  # 结构分析 Skill
│   ├── flow-analyzer/SKILL.md   # 流程分析 Skill
│   └── update-manifest/SKILL.md # Manifest 维护 Skill
└── docs/
    ├── spec.md                  # 共用规范（文档格式、评分标准等）
    └── design.md                # 本设计文档
```

输出文档统一存放在项目根目录的 `./docs/code-analyzer/` 下。

## 7. 使用示例

```bash
/code-analyzer                                      # agent 自行判断范围和类型
/code-analyzer ./src                                # agent 识别范围为 ./src，询问类型
/code-analyzer ./src full-scan                      # 对 ./src 做整体扫描
/code-analyzer ./src structure                      # 对 ./src 做结构分析
/code-analyzer 分析战斗模块的流程，重点关注初始化      # agent 解析自然语言需求
```
