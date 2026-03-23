---
name: update-manifest
description: |
  扫描 `./docs/code-analyzer/` 目录，从所有 `.md` 文件的 frontmatter 提取元信息，
  自动生成并更新 `manifest.md` 文档清单。
  仅由 analyst agent 调用，不应由用户直接触发。
allowed-tools: Bash(*)
disable-model-invocation: true
user-invocable: false
---

调用脚本扫描文档目录，生成 manifest。

## 执行命令

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/update-manifest.js
```

脚本会自动：
1. 扫描 `./docs/code-analyzer/*.md`（排除 manifest.md）
2. 解析每个文件的 frontmatter，提取 name、description、type、scope、date
3. 生成 `./docs/code-analyzer/manifest.md`

## 输出

脚本输出扫描结果：`完成：发现 N 个文档，跳过 M 个`
