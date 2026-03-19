---
name: code-analyzer
description: |
  分析游戏项目代码架构与实现，自动生成审查文档。
  当用户输入 /code-analyzer 或需要分析代码架构时触发。
  适用于：代码审查、架构评估、技术债务分析、重构建议。
---

分析游戏项目代码架构与实现，自动生成审查文档。

## 工作流程

1. **理解需求** - 分析用户提示，识别：
   - 目标代码路径
   - 需要审查的技术领域（自动判断）
   - 模块名称
   - 分析需求描述（用于目录命名）

2. **调用负责人** - 使用 `analysis-leader` agent 执行并行分析：
   - 传递目标路径、领域列表、模块名、描述
   - 总控器负责创建目录、调度专家、生成汇总

## 输出结构

```
./docs/
└── {日期}-{分析需求提要}/
    ├── summary.md          # 总概括文档（总控器生成）
    ├── architecture.md     # 各领域专家生成
    ├── rendering.md
    ├── network.md
    └── ...
```

**目录命名**：`{日期}-{分析需求提要}`
- 示例：`2026-03-19-渲染模块审查/`

## 领域判断规则

**路径关键词**：
| 关键词 | 领域 |
|--------|------|
| render, shader, graphics | rendering |
| ui, view, widget | ui |
| network, sync, server | network |
| scene, level, world | scene |
| entity, component, ecs | object |
| physics, collision | physics |
| core, framework | architecture |

**提示关键词**：根据技术术语匹配对应领域

## 专家领域

| 领域 | 标识 | 关注点 |
|------|------|--------|
| 架构 | architecture | 整体架构、模块划分、设计模式 |
| UI框架 | ui | UI架构、事件系统、布局动画 |
| 渲染管线 | rendering | 渲染架构、Shader、光照优化 |
| 网络同步 | network | 帧同步、状态同步、预测回滚 |
| 场景管理 | scene | 场景图、流式加载、大世界 |
| 对象管理 | object | ECS、对象池、序列化 |
| 物理引擎 | physics | 碰撞检测、刚体、角色控制 |

详细领域说明见 `analysis-leader` agent。
