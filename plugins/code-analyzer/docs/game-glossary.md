# 游戏领域术语表

分析 Skill 识别模块、分类第三方库时参考此表。

## 1. 常见中间件 / 第三方库

| 名称 | 类别 | 说明 |
|------|------|------|
| Wwise | 音频 | Audiokinetic 音频引擎 |
| FMOD | 音频 | FMOD 音频中间件 |
| criware | 音频/视频 | CRI 多媒体中间件（ADX2 音频、Sofdec 视频） |
| Spine | 2D 动画 | 2D 骨骼动画工具 |
| Live2D | 2D 动画 | 角色动态立绘 |
| DragonBones | 2D 动画 | 开源 2D 骨骼动画 |
| protobuf | 序列化 | Google Protocol Buffers |
| FlatBuffers | 序列化 | 高性能零拷贝序列化 |
| msgpack | 序列化 | 紧凑二进制序列化 |
| RakNet | 网络 | 游戏网络库 |
| KCP | 网络 | 可靠 UDP 传输协议 |
| ENet | 网络 | 可靠 UDP 网络库 |
| libcurl | 网络 | HTTP 客户端库 |
| Lua | 脚本 | Lua 脚本语言 |
| tolua | 脚本绑定 | Lua 绑定 C# 方案 |
| xLua | 脚本绑定 | 腾讯 Lua 绑定方案 |
| sLua | 脚本绑定 | Lua 绑定方案 |
| ILRuntime | 热更新 | C# 解释执行热更 |
| HybridCLR | 热更新 | Unity IL2CPP 原生热更 |
| InjectFix | 热更新 | 腾讯 C# 热修复 |
| Recast | AI/寻路 | 导航网格生成 |
| Detour | AI/寻路 | 导航网格寻路 |
| behavior3 | AI | 行为树框架 |
| TextMeshPro / TMP | UI/文本 | Unity 高质量文本渲染 |
| FairyGUI | UI | 跨引擎 UI 框架 |
| UGUI | UI | Unity 内置 UI 系统 |
| NGUI | UI | Unity 第三方 UI（旧） |
| DOTween | 动画/缓动 | Unity 补间动画库 |
| UniTask | 异步 | Unity 高性能异步库 |
| UniRx | 响应式 | Unity 响应式编程 |
| Addressables | 资源管理 | Unity 可寻址资源系统 |
| AssetBundle | 资源管理 | Unity 资源打包 |
| YooAsset | 资源管理 | Unity 资源管理框架 |
| LitJson | 数据 | 轻量 JSON 库 |
| Newtonsoft.Json | 数据 | .NET JSON 库 |
| SQLite | 数据 | 嵌入式数据库 |
| Odin | 编辑器 | Unity 编辑器扩展 |
| ECS / DOTS | 架构 | Unity 面向数据的技术栈 |
| Zenject / VContainer | 依赖注入 | Unity IoC 容器 |
| Mirror | 网络同步 | Unity 网络框架 |
| Photon | 网络同步 | 多人实时通信平台 |
| Nakama | 后端 | 开源游戏服务器 |

## 2. 常见目录 / 命名与功能映射

| 目录名 / 命名模式 | 通常对应功能 |
|-------------------|-------------|
| audio, sound, sfx, bgm, music | 音频模块 |
| net, network, proto, socket, rpc | 网络模块 |
| render, graphic, shader, material, vfx, fx | 渲染/特效模块 |
| ui, gui, hud, widget, panel, view | UI 模块 |
| ai, bt, fsm, npc, brain | AI 模块 |
| battle, combat, fight, skill, buff | 战斗模块 |
| scene, map, world, level, terrain | 场景/地图模块 |
| res, asset, bundle, loader, resource | 资源管理 |
| hotfix, patch, update | 热更新 |
| config, table, data, csv, excel | 配置/数据表 |
| anim, animation, animator, spine | 动画模块 |
| physics, collider, rigidbody | 物理模块 |
| input, control, joystick, touch | 输入模块 |
| camera, cinemachine | 摄像机模块 |
| event, message, signal, dispatch | 事件/消息系统 |
| pool, cache, recycle | 对象池 |
| timer, scheduler, coroutine | 定时/调度 |
| log, debug, console, profiler | 调试/日志 |
| localization, i18n, lang | 多语言 |
| save, archive, persist | 存档 |
| shop, store, pay, iap | 商城/支付 |
| social, friend, chat, guild | 社交模块 |
| quest, task, mission | 任务系统 |
| bag, inventory, item, equip | 背包/物品 |
| login, account, auth, sdk | 登录/账号 |
| guide, tutorial, newbie | 新手引导 |
| ad, advertisement | 广告模块 |
| analytics, tracking, report | 数据埋点/统计 |

## 3. 功能/系统命名模式（用于 feature 分析）

feature-analyzer 识别功能边界时参考此表。

### 3.1 功能命名关键词

| 命名模式 | 典型功能类型 | 分析重点 |
|----------|-------------|----------|
| `*System`, `*Mgr`, `*Manager` | 核心系统/管理器 | 生命周期、初始化顺序、模块间协调 |
| `*Service` | 服务层 | 接口设计、依赖注入、可替换性 |
| `*Controller`, `*Ctrl` | 控制器 | 输入处理、状态流转、业务编排 |
| `*Handler`, `*Processor` | 处理器 | 消息处理、事件响应、数据转换 |
| `*Module`, `*Unit` | 功能模块 | 内聚性、接口稳定性、复用性 |
| `*Driver`, `*Adapter` | 驱动/适配层 | 抽象层次、平台兼容性 |
| `*Factory`, `*Pool` | 工厂/对象池 | 对象生命周期、内存管理 |
| `*Context`, `*Environment` | 上下文/环境 | 状态管理、作用域、资源持有 |

### 3.2 典型功能系统识别

| 功能名称关键词 | 涉及模块 | 分析重点 |
|---------------|----------|----------|
| 子弹系统/弹道系统 | bullet, weapon, effect, physics | 发射流程、碰撞检测、对象池、特效触发 |
| 战斗系统 | battle, skill, buff, ai, camera | 回合/实时逻辑、技能释放、状态同步、镜头控制 |
| 背包系统 | bag, inventory, item, equip | 物品操作、数据持久化、UI刷新、容量管理 |
| 任务系统 | quest, task, mission, guide | 任务状态机、奖励发放、条件检查、引导触发 |
| 存档系统 | save, archive, persist, storage | 序列化、加密、版本兼容、云端同步 |
| 网络同步 | sync, replicate, state, rpc | 状态同步、可靠传输、断线重连、预测回滚 |
| 资源加载 | loader, asset, bundle, resource | 加载策略、依赖解析、缓存管理、内存释放 |
| UI 框架 | ui, view, panel, window | 层级管理、打开/关闭流程、数据绑定、动画过渡 |

### 3.3 功能边界识别规则

分析 feature 时，通过以下线索识别功能涉及的范围：

1. **命名一致性**：查找包含相同前缀/后缀的类和文件
2. **调用链追踪**：从入口函数追踪跨模块调用
3. **数据关联**：识别共享的数据结构（配置、状态、事件）
4. **生命周期关联**：查找在同一生命周期阶段初始化的模块

## 4. 游戏引擎特征

| 引擎 | 识别特征 |
|------|----------|
| Unity | `.cs` 文件、`MonoBehaviour`、`ScriptableObject`、`Assets/` 目录、`.unity` 场景文件、`ProjectSettings/` |
| Unreal | `.cpp`/`.h` + `UCLASS`/`UPROPERTY` 宏、`Source/` 目录、`.uproject` 文件 |
| Cocos Creator | `.ts` 文件、`cc.Component`、`assets/` 目录、`tsconfig.json` |
| Godot | `.gd` 文件、`extends Node`、`project.godot` |
| 自研引擎 | 无上述特征，通常有自定义构建系统 |
