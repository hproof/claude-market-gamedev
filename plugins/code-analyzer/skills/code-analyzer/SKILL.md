---
name: code-analyzer
description: |
  分析游戏项目代码架构与实现，自动生成审查文档。
  当用户输入 /code-analyzer 或需要分析代码架构时触发。
  适用于：代码审查、架构评估、技术债务分析、重构建议。
---

分析游戏项目代码架构与实现，自动生成审查文档。

## 工作流程

1. **理解需求** - 分析用户的提示内容，自动识别：
   - 目标代码路径
   - 需要审查的技术领域
   - 分析范围和关注点
   - 模块名称（从路径或提示中提取）

2. **并行分析** - 为每个识别出的领域创建 SubAgent，并行执行：
   - 每个领域专家独立分析代码
   - 使用对应领域的 agent 定义文件
   - **向 SubAgent 传递以下信息**：
     - 目标代码路径
     - 输出目录：`./docs/`
     - 输出文件名：`{日期}-{领域}-{模块}.md`
     - 领域标识和模块名称

3. **独立输出** - 每个 SubAgent 各自保存文档到指定路径：
   - 在 `./docs/` 目录下创建独立文档
   - 文件名遵循 `{日期}-{领域}-{模块}.md` 格式
   - 多领域分析时生成多个独立文档

## 输出文档规则

**输出目录**：`./docs/`（相对于当前工作目录，自动创建）

**文件命名**：`{日期}-{领域}-{模块}.md`

| 部分 | 说明 | 示例 |
|------|------|------|
| 日期 | 生成日期，格式 `YYYY-MM-DD` | 2026-03-19 |
| 领域 | 专家领域标识（见下表） | architecture, rendering |
| 模块 | 分析的模块名称 | core, shader, network |

**示例文件名**：
- `2026-03-19-architecture-core.md`
- `2026-03-19-rendering-shader.md`
- `2026-03-19-network-sync.md`

**注意**：每个领域独立输出文档，不合并为单个文件。

## 专家领域

### architecture（架构专家）
**关注点**：整体架构设计、模块划分、依赖关系、设计模式、可扩展性、可维护性

**适用场景**：
- 项目整体架构评审
- 模块边界和依赖分析
- 设计模式应用评估
- 技术债务识别
- 重构建议

**关键词**：架构、模块、依赖、设计模式、耦合、分层、接口、抽象

---

### ui（UI框架专家）
**关注点**：UI架构、事件系统、布局系统、动画系统、资源管理

**适用场景**：
- UI系统代码审查
- MVC/MVP/MVVM 架构评估
- 事件冒泡/委托机制分析
- 布局计算性能优化
- UI动画性能

**关键词**：UI、界面、视图、布局、事件、动画、控件、Widget、Canvas

---

### rendering（渲染管线专家）
**关注点**：渲染架构、材质/Shader系统、光照、后处理、渲染优化

**适用场景**：
- 渲染管线架构评审
- Forward/Deferred/Clustered 渲染评估
- Shader 变体管理
- 光照和阴影实现
- 后处理效果
- 渲染性能优化（DrawCall、合批、剔除）

**关键词**：渲染、Render、Shader、材质、光照、阴影、后处理、Camera、DrawCall

---

### network（网络同步专家）
**关注点**：帧同步、状态同步、预测回滚、网络优化、安全性

**适用场景**：
- 网络同步方案评审
- 帧同步确定性分析
- 客户端预测与服务器回滚
- 延迟处理和补偿
- 网络流量优化
- 反作弊机制

**关键词**：网络、同步、帧同步、状态同步、预测、回滚、延迟、连接、Server、Client

---

### scene（场景管理专家）
**关注点**：场景图、空间分区、流式加载、场景切换、大世界支持

**适用场景**：
- 场景图架构评审
- 空间分区数据结构（四叉树/八叉树/BVH）
- 流式加载和Chunk管理
- 场景切换机制
- 大世界和坐标精度处理
- 可见性剔除

**关键词**：场景、Scene、Level、World、Map、Chunk、加载、流送、四叉树、八叉树

---

### object（对象管理专家）
**关注点**：ECS架构、对象生命周期、对象池、序列化、引用管理

**适用场景**：
- ECS 架构评审
- 对象生命周期管理
- 对象池和内存池实现
- 序列化和反序列化
- 引用管理（智能指针/句柄/ID）
- 反射系统

**关键词**：对象、Object、Entity、Component、System、ECS、对象池、序列化、生命周期

---

### physics（物理引擎专家）
**关注点**：碰撞检测、刚体动力学、约束求解、角色控制、物理优化

**适用场景**：
- 物理引擎架构评审
- 碰撞检测算法（Broad/Narrow Phase）
- 刚体动力学和积分器
- 约束求解和关节系统
- 角色控制器实现
- 物理优化（睡眠机制、LOD）

**关键词**：物理、Physics、碰撞、Collision、刚体、RigidBody、约束、角色、Character

## 领域自动判断规则

**路径关键词匹配**：
| 关键词 | 触发领域 |
|--------|----------|
| render, shader, graphics, camera, material | rendering |
| ui, view, widget, hud, canvas | ui |
| network, sync, connection, server, client, multiplayer | network |
| scene, level, world, map, chunk, spatial | scene |
| entity, component, object, pool, serialize | object |
| physics, collision, rigidbody, character, constraint | physics |
| core, framework, arch, manager, system | architecture |

**用户提示关键词匹配**：
- 根据提示中的技术术语匹配对应领域
- 多个领域关键词出现时，启用多个专家
- 未明确指定时，分析所有相关领域
