---
description: 回显用户输入的文本, 并和用户玩猜数字游戏。
disable-model-invocation: true
allowed_tools: Bash(echo:*)
---

# Echo
回显用户输入的文本, 并和用户玩猜数字游戏。


## 使用方法
用户输入 `/echo 任意文本` 即可开始


## 执行步骤

1. 显示以下消息
```
当前会话ID: CLAUDE_SESSION_ID
当前 skill 目录: ${CLAUDE_SKILL_DIR}
你输入的内容是: $ARGUMENTS
```
把其中的 CLAUDE_SESSION_ID 替换为 `${CLAUDE_SESSION_ID}`。

2. 生成一个随机数 X, 范围为 [0, 100], 你要记住这个 X 的值


3.  显示消息 
```
我有一个随机数 X, 请猜测它的值是多少?
```

3. 等待用户输入一个数值 Y

4. 比较 Y 和 X
- 如果 Y 大于 X, 显示消息 `Y 大于 X`, 重复步骤 3
- 如果 Y 小于 X, 显示消息 `Y 小于 X`, 重复步骤 3
- 如果 Y 等于 X, 显示消息 `Y 等于 X`, 显示消息 `恭喜你猜对了!`

5. 显示 `游戏结束`