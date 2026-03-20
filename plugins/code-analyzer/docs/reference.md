# code-analyzer 参考文档

本文档包含 code-analyzer 的概述信息，详细规范见本文档所在目录下的其他规范文档。

## 规范文档索引

| 文档 | 路径 | 内容 |
|------|------|------|
| 文档生成规范 | `document-spec.md` | 文档命名、结构、导航规范 |
| 评分标准指南 | `scoring-guide.md` | 评分维度、标准、等级定义 |
| Manifest 使用规则 | `manifest-guide.md` | manifest 维护和使用规则 |
| 代码链接规范 | `code-link-guide.md` | 代码引用链接格式规范 |

## Skill 列表

| Skill | 描述 | 触发方式 |
|-------|------|----------|
| `code-analyzer` | 启动器，解析参数并调用 developer agent | `/code-analyzer [scope] [type]` |
| `full-scan` | 宏观概览：扫描模块分布和层级关系 | `type=full-scan` |
| `structure-analyzer` | 深度结构：分析类关系、文件依赖、耦合度 | `type=structure` |
| `flow-analyzer` | 流程分析：追踪初始化、主循环、网络同步等关键流程 | `type=flow` |

## Agent 列表

| Agent | 描述 | 用途 |
|-------|------|------|
| `developer` | 游戏开发工程师 | 执行分析任务，管理 manifest，遵守规范文档 |

## 参数解析规则

```
/code-analyzer [scope] [type]
```

**参数识别逻辑：**
1. 第一个参数如果以 `/`、`./` 开头或是相对路径 → `scope`（分析范围）
2. 第二个参数如果匹配分析类型 → `type`（分析类型）
3. 如果未指定 `type` → **询问用户**

**分析类型关键词映射：**
| 关键词 | 说明 | 调用的 Skill |
|--------|------|-------------|
| `full-scan`, `scan`, `整体扫描` | 宏观概览：识别模块边界和层级 | `full-scan` |
| `structure`, `struct`, `结构分析` | 深度结构：类关系、依赖、耦合度 | `structure-analyzer` |
| `flow`, `流程分析` | 流程追踪：初始化、主循环、网络同步 | `flow-analyzer` |

## 文档清单机制

### 固定输出目录

所有分析文档保存到：**`./docs/code-analyzer/`**

### 文档命名规则

文档名由 **分析范围 + 分析类型** 组成：

```
{normalized-scope}-{type}.md
```

详见 `document-spec.md` 的"文档命名规范"章节。

### Manifest 文件

**路径：** `./docs/code-analyzer/manifest.md`

详见 `manifest-guide.md`

## 模块划分标准

### 第三方库
- **位置**：`third_party/`, `external/`, `libs/`, `vendor/`
- **特征**：开源许可证、版本文件
- **处理方式**：在 full-scan 中识别列出

### 底层模块
- **特征**：被业务依赖、提供通用能力、目录内语言一致
- **处理方式**：通过 `structure-analyzer` 或 `flow-analyzer` 分析

### 业务模块
- **场景内业务**：战斗、探索等（与场景绑定、实时性高）
- **场景无关业务**：背包、强化等（UI交互、数据驱动）
- **处理方式**：在 full-scan 中识别分类

## 业务类型定义

### 场景内业务
玩家处于游戏场景中时进行的玩法：
- 战斗系统（技能、Buff、AI）
- 关卡探索（触发器、事件）
- 场景交互（采集、对话）
- 移动控制（寻路、跳跃）

### 场景无关业务
不依赖于特定游戏场景的功能：
- 包裹/背包系统
- 道具强化/合成
- 任务/成就系统
- 社交系统（好友、聊天）
- 商店/交易系统
