# 代码链接规范

本文档定义分析文档中代码引用的链接格式。

## 1. 基本格式

### 标准格式

```markdown
[显示文本](file_path:line_number)
```

### 示例

```markdown
[GameManager::Init](src/core/manager.cpp:45)
[RenderSystem::Draw](src/render/renderer.cpp:128)
[ConfigMgr::Load](src/utils/config.cpp:23)
```

## 2. 路径规则

### 相对路径

- 使用相对于项目根目录的相对路径
- 不包含前导 `./`
- 示例：`src/core/manager.cpp`（正确）vs `./src/core/manager.cpp`（不推荐）

### 路径格式

| 平台 | 路径格式 | 示例 |
|------|----------|------|
| Unix/Linux/macOS | 正斜杠 `/` | `src/core/manager.cpp` |
| Windows | 正斜杠 `/`（统一） | `src/core/manager.cpp` |

**注意：** 统一使用正斜杠 `/`，即使在 Windows 平台上。

## 3. 行号规则

### 精确到行

```markdown
[函数定义](src/core/game.cpp:45)
[类声明](src/core/game.h:12)
```

### 行号范围（可选）

```markdown
[函数实现](src/core/game.cpp:45-78)
[代码块](src/utils/helper.cpp:23-45)
```

### 行号获取

- 使用 IDE 或编辑器的行号显示
- 行号从 1 开始计数
- 确保行号在代码变更后仍然准确

## 4. 显示文本规范

### 函数/方法

```markdown
[ClassName::MethodName](path:line)
[FunctionName](path:line)
```

示例：
```markdown
[GameManager::Initialize](src/manager.cpp:45)
[LoadConfig](src/config.cpp:23)
```

### 类/结构体

```markdown
[ClassName](path:line)
[struct StructName](path:line)
```

示例：
```markdown
[GameObject](src/object.h:15)
[struct Vector3](src/math.h:45)
```

### 变量/成员

```markdown
[memberName](path:line)
[ClassName::memberName](path:line)
```

示例：
```markdown
[m_instance](src/manager.cpp:12)
[GameManager::m_renderSystem](src/manager.h:34)
```

### 代码位置描述

```markdown
[初始化代码](path:line)
[循环逻辑](path:line)
[错误处理](path:line)
```

## 5. 使用场景

### 问题定位

在问题列表中使用代码链接：

```markdown
| 严重程度 | 问题 | 位置 | 建议 |
|---------|------|------|------|
| 高 | 内存泄漏，未释放资源 | `[RenderTarget::Init](src/render/target.cpp:45)` | 添加析构函数释放资源 |
| 中 | 魔法数字 | `[GameLogic::Update](src/game/logic.cpp:78)` | 使用具名常量 |
```

### 接口引用

在接口说明中使用代码链接：

```markdown
### 主要接口

| 接口 | 说明 | 代码链接 |
|------|------|----------|
| `Initialize()` | 初始化渲染系统 | `[声明](src/render.h:45)` `[实现](src/render.cpp:23)` |
| `Render()` | 执行渲染 | `[声明](src/render.h:56)` `[实现](src/render.cpp:78)` |
```

### 流程说明

在流程分析中使用代码链接：

```markdown
### 初始化流程

1. **[主入口](src/main.cpp:12)** - 程序入口
2. **[系统初始化](src/core/init.cpp:45)** - 初始化核心系统
3. **[模块加载](src/core/module.cpp:23)** - 加载各模块
```

## 6. 批量链接

### 同类代码分组

将同类代码链接分组展示：

```markdown
### 渲染相关代码

- 初始化: `[RenderSystem::Init](src/render.cpp:45)`
- 绘制: `[RenderSystem::Draw](src/render.cpp:128)`
- 清理: `[RenderSystem::Cleanup](src/render.cpp:256)`

### 网络相关代码

- 连接: `[NetManager::Connect](src/net/manager.cpp:34)`
- 发送: `[NetManager::Send](src/net/manager.cpp:67)`
- 接收: `[NetManager::Receive](src/net/manager.cpp:89)`
```

## 7. 链接验证

### 生成前检查

- 确保文件路径存在
- 确保行号在有效范围内
- 确保路径格式统一

### 生成后验证

- 在 VS Code 中测试链接可点击
- 确认跳转位置正确
- 确认行号与代码匹配

## 8. 特殊情况

### 多行代码

对于跨多行的代码，使用范围或指向起始行：

```markdown
[函数实现 - 45-78行](src/core/game.cpp:45)
<!-- 或 -->
[函数开始](src/core/game.cpp:45)
```

### 外部代码

对于第三方库代码，标明库名：

```markdown
[std::vector::push_back](stl_vector:456) (STL)
[glCreateShader](GL/glew.h:1234) (OpenGL)
```

### 生成的代码

对于生成的代码，特别标注：

```markdown
[自动生成的序列化代码](gen/serializer.cpp:23) (generated)
```

## 9. 工具支持

### VS Code

VS Code 支持 `file:line` 格式的链接自动识别：
- 按住 `Ctrl` 点击链接跳转
- 支持行号和行号范围

### 其他编辑器

大多数现代 IDE 和编辑器都支持类似的链接格式：
- Vim/Neovim: 使用 `gF` 跳转
- Emacs: 使用 `find-file-at-point`
- JetBrains IDE: 自动识别并支持点击跳转
