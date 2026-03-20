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

## 3. 游戏引擎特征

| 引擎 | 识别特征 |
|------|----------|
| Unity | `.cs` 文件、`MonoBehaviour`、`ScriptableObject`、`Assets/` 目录、`.unity` 场景文件、`ProjectSettings/` |
| Unreal | `.cpp`/`.h` + `UCLASS`/`UPROPERTY` 宏、`Source/` 目录、`.uproject` 文件 |
| Cocos Creator | `.ts` 文件、`cc.Component`、`assets/` 目录、`tsconfig.json` |
| Godot | `.gd` 文件、`extends Node`、`project.godot` |
| 自研引擎 | 无上述特征，通常有自定义构建系统 |
