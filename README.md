# claude-market-gamedev
用于游戏开发的 claude 插件市场


# 注意事项

## skill 中调用 agent
- 使用 `Agent` 工具调用 `plugin-name:agent-name` agent
- 告诉其 目标需求 而不是 执行命令
    - 否则， 无法发挥 agent 的自主性


## agent 中调用 skill
- 需写明 `skill-name` 是 claude code 的 skill 而不是命令

