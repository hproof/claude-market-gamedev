---
description: 和用户玩猜数字游戏
disable-model-invocation: true
allowed-tools: Bash, Read, Write
---

# Guess Number
和用户玩猜数字游戏。

## 使用方法
用户输入 `/guess-number` 即可开始


## 执行步骤

1. **显示欢迎信息与环境信息**
首先向发送以下欢迎信息:
```
欢迎来到猜数字游戏!
---
当前会话: `${CLAUDE_SESSION_ID}`
当前 目录: `${PWD}`
skill 目录: `${CLAUDE_SKILL_DIR}`
plugin 目录: `${CLAUDE_PLUGIN_ROOT}`
---
```

2. **启动游戏逻辑**

2.1 **初始化**
* 使用 PS1 脚本 `scripts/generate-number.ps1` 获取一个随机数

2.2 **交互循环**
  * 提示用户输入数字
  * 比较用户输入的数字和随机数, 回答 “太大了” “太小了” 或 “恭喜你猜对了”