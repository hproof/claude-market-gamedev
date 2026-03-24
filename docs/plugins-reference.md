## ​Plugin components reference

### ​Skills

```
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (optional)
│   └── scripts/ (optional)
└── code-reviewer/
    └── SKILL.md

```

- Skills and commands are automatically discovered when the plugin is installed

- Claude can invoke them automatically based on task context

- Skills can include supporting files alongside SKILL.md

### ​Agents

```
---
name: agent-name
description: What this agent specializes in and when Claude should invoke it
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

Detailed system prompt for the agent describing its role, expertise, and behavior.

```

- Agents appear in the `/agents` interface

- Claude can invoke agents automatically based on task context

- Agents can be invoked manually by users

- Plugin agents work alongside built-in Claude agents

### ​Hooks

```
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}

```

| Event | When it fires |

| --- | --- |

| SessionStart | When a session begins or resumes |

| UserPromptSubmit | When you submit a prompt, before Claude processes it |

| PreToolUse | Before a tool call executes. Can block it |

| PermissionRequest | When a permission dialog appears |

| PostToolUse | After a tool call succeeds |

| PostToolUseFailure | After a tool call fails |

| Notification | When Claude Code sends a notification |

| SubagentStart | When a subagent is spawned |

| SubagentStop | When a subagent finishes |

| Stop | When Claude finishes responding |

| StopFailure | When the turn ends due to an API error. Output and exit code are ignored |

| TeammateIdle | When an agent team teammate is about to go idle |

| TaskCompleted | When a task is being marked as completed |

| InstructionsLoaded | When a CLAUDE.md or .claude/rules/*.md file is loaded into context. Fires at session start and when files are lazily loaded during a session |

| ConfigChange | When a configuration file changes during a session |

| WorktreeCreate | When a worktree is being created via --worktree or isolation: "worktree". Replaces default git behavior |

| WorktreeRemove | When a worktree is being removed, either at session exit or when a subagent finishes |

| PreCompact | Before context compaction |

| PostCompact | After context compaction completes |

| Elicitation | When an MCP server requests user input during a tool call |

| ElicitationResult | After a user responds to an MCP elicitation, before the response is sent back to the server |

| SessionEnd | When a session terminates |

- `command`: execute shell commands or scripts

- `http`: send the event JSON as a POST request to a URL

- `prompt`: evaluate a prompt with an LLM (uses `$ARGUMENTS` placeholder for context)

- `agent`: run an agentic verifier with tools for complex verification tasks

### ​MCP servers

```
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}

```

- Plugin MCP servers start automatically when the plugin is enabled

- Servers appear as standard MCP tools in Claude’s toolkit

- Server capabilities integrate seamlessly with Claude’s existing tools

- Plugin servers can be configured independently of user MCP servers

### ​LSP servers

- Instant diagnostics: Claude sees errors and warnings immediately after each edit

- Code navigation: go to definition, find references, and hover information

- Language awareness: type information and documentation for code symbols

```
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}

```

```
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}

```

| Field | Description |

| --- | --- |

| command | The LSP binary to execute (must be in PATH) |

| extensionToLanguage | Maps file extensions to language identifiers |

| Field | Description |

| --- | --- |

| args | Command-line arguments for the LSP server |

| transport | Communication transport: stdio (default) or socket |

| env | Environment variables to set when starting the server |

| initializationOptions | Options passed to the server during initialization |

| settings | Settings passed via workspace/didChangeConfiguration |

| workspaceFolder | Workspace folder path for the server |

| startupTimeout | Max time to wait for server startup (milliseconds) |

| shutdownTimeout | Max time to wait for graceful shutdown (milliseconds) |

| restartOnCrash | Whether to automatically restart the server if it crashes |

| maxRestarts | Maximum number of restart attempts before giving up |

| Plugin | Language server | Install command |

| --- | --- | --- |

| pyright-lsp | Pyright (Python) | pip install pyright or npm install -g pyright |

| typescript-lsp | TypeScript Language Server | npm install -g typescript-language-server typescript |

| rust-lsp | rust-analyzer | See rust-analyzer installation |

## ​Plugin installation scopes

| Scope | Settings file | Use case |

| --- | --- | --- |

| user | ~/.claude/settings.json | Personal plugins available across all projects (default) |

| project | .claude/settings.json | Team plugins shared via version control |

| local | .claude/settings.local.json | Project-specific plugins, gitignored |

| managed | Managed settings | Managed plugins (read-only, update only) |

## ​Plugin manifest schema

### ​Complete schema

```
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "[email protected]",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}

```

### ​Required fields

| Field | Type | Description | Example |

| --- | --- | --- | --- |

| name | string | Unique identifier (kebab-case, no spaces) | "deployment-tools" |

### ​Metadata fields

| Field | Type | Description | Example |

| --- | --- | --- | --- |

| version | string | Semantic version. If also set in the marketplace entry, plugin.json takes priority. You only need to set it in one place. | "2.1.0" |

| description | string | Brief explanation of plugin purpose | "Deployment automation tools" |

| author | object | Author information | {"name": "Dev Team", "email": "[email protected]"} |

| homepage | string | Documentation URL | "https://docs.example.com" |

| repository | string | Source code URL | "https://github.com/user/plugin" |

| license | string | License identifier | "MIT", "Apache-2.0" |

| keywords | array | Discovery tags | ["deployment", "ci-cd"] |

### ​Component path fields

| Field | Type | Description | Example |

| --- | --- | --- | --- |

| commands | string|array | Additional command files/directories | "./custom/cmd.md" or ["./cmd1.md"] |

| agents | string|array | Additional agent files | "./custom/agents/reviewer.md" |

| skills | string|array | Additional skill directories | "./custom/skills/" |

| hooks | string|array|object | Hook config paths or inline config | "./my-extra-hooks.json" |

| mcpServers | string|array|object | MCP config paths or inline config | "./my-extra-mcp-config.json" |

| outputStyles | string|array | Additional output style files/directories | "./styles/" |

| lspServers | string|array|object | Language Server Protocol configs for code intelligence (go to definition, find references, etc.) | "./.lsp.json" |

### ​Path behavior rules

- If `commands/` exists, it’s loaded in addition to custom command paths

- All paths must be relative to plugin root and start with `./`

- Commands from custom paths use the same naming and namespacing rules

- Multiple paths can be specified as arrays for flexibility

```
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}

```

### ​Environment variables

```
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}

```

#### ​Persistent data directory

```
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}

```

```
{
  "mcpServers": {
    "routines": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}

```

## ​Plugin caching and file resolution

- Through `claude --plugin-dir`, for the duration of a session.

- Through a marketplace, installed for future sessions.

### ​Path traversal limitations

### ​Working with external dependencies

```
# Inside your plugin directory
ln -s /path/to/shared-utils ./shared-utils

```

## ​Plugin directory structure

### ​Standard plugin layout

```
enterprise-plugin/
├── .claude-plugin/           # Metadata directory (optional)
│   └── plugin.json             # plugin manifest
├── commands/                 # Default command location
│   ├── status.md
│   └── logs.md
├── agents/                   # Default agent location
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Agent Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Hook configurations
│   ├── hooks.json           # Main hook config
│   └── security-hooks.json  # Additional hooks
├── settings.json            # Default settings for the plugin
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations
├── scripts/                 # Hook and utility scripts
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # License file
└── CHANGELOG.md             # Version history

```

### ​File locations reference

| Component | Default Location | Purpose |

| --- | --- | --- |

| Manifest | .claude-plugin/plugin.json | Plugin metadata and configuration (optional) |

| Commands | commands/ | Skill Markdown files (legacy; use skills/ for new skills) |

| Agents | agents/ | Subagent Markdown files |

| Skills | skills/ | Skills with <name>/SKILL.md structure |

| Hooks | hooks/hooks.json | Hook configuration |

| MCP servers | .mcp.json | MCP server definitions |

| LSP servers | .lsp.json | Language server configurations |

| Settings | settings.json | Default configuration applied when the plugin is enabled. Only agent settings are currently supported |

## ​CLI commands reference

### ​plugin install

```
claude plugin install <plugin> [options]

```

- `<plugin>`: Plugin name or `plugin-name@marketplace-name` for a specific marketplace

| Option | Description | Default |

| --- | --- | --- |

| -s, --scope <scope> | Installation scope: user, project, or local | user |

| -h, --help | Display help for command |  |

```
# Install to user scope (default)
claude plugin install formatter@my-marketplace

# Install to project scope (shared with team)
claude plugin install formatter@my-marketplace --scope project

# Install to local scope (gitignored)
claude plugin install formatter@my-marketplace --scope local

```

### ​plugin uninstall

```
claude plugin uninstall <plugin> [options]

```

- `<plugin>`: Plugin name or `plugin-name@marketplace-name`

| Option | Description | Default |

| --- | --- | --- |

| -s, --scope <scope> | Uninstall from scope: user, project, or local | user |

| --keep-data | Preserve the plugin’s persistent data directory |  |

| -h, --help | Display help for command |  |

### ​plugin enable

```
claude plugin enable <plugin> [options]

```

- `<plugin>`: Plugin name or `plugin-name@marketplace-name`

| Option | Description | Default |

| --- | --- | --- |

| -s, --scope <scope> | Scope to enable: user, project, or local | user |

| -h, --help | Display help for command |  |

### ​plugin disable

```
claude plugin disable <plugin> [options]

```

- `<plugin>`: Plugin name or `plugin-name@marketplace-name`

| Option | Description | Default |

| --- | --- | --- |

| -s, --scope <scope> | Scope to disable: user, project, or local | user |

| -h, --help | Display help for command |  |

### ​plugin update

```
claude plugin update <plugin> [options]

```

- `<plugin>`: Plugin name or `plugin-name@marketplace-name`

| Option | Description | Default |

| --- | --- | --- |

| -s, --scope <scope> | Scope to update: user, project, local, or managed | user |

| -h, --help | Display help for command |  |

## ​Debugging and development tools

### ​Debugging commands

- Which plugins are being loaded

- Any errors in plugin manifests

- Command, agent, and hook registration

- MCP server initialization

### ​Common issues

| Issue | Cause | Solution |

| --- | --- | --- |

| Plugin not loading | Invalid plugin.json | Run claude plugin validate or /plugin validate to check plugin.json, skill/agent/command frontmatter, and hooks/hooks.json for syntax and schema errors |

| Commands not appearing | Wrong directory structure | Ensure commands/ at root, not in .claude-plugin/ |

| Hooks not firing | Script not executable | Run chmod +x script.sh |

| MCP server fails | Missing ${CLAUDE_PLUGIN_ROOT} | Use variable for all plugin paths |

| Path errors | Absolute paths used | All paths must be relative and start with ./ |

| LSP Executable not found in $PATH | Language server not installed | Install the binary (e.g., npm install -g typescript-language-server typescript) |

### ​Example error messages

- `Invalid JSON syntax: Unexpected token } in JSON at position 142`: check for missing commas, extra commas, or unquoted strings

- `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`: a required field is missing

- `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: JSON syntax error

- `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`: command path exists but contains no valid command files

- `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`: the `source` path in marketplace.json points to a non-existent directory

- `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`: remove duplicate component definitions or remove `strict: false` in marketplace entry

### ​Hook troubleshooting

- Check the script is executable: `chmod +x ./scripts/your-script.sh`

- Verify the shebang line: First line should be `#!/bin/bash` or `#!/usr/bin/env bash`

- Check the path uses `${CLAUDE_PLUGIN_ROOT}`: `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"`

- Test the script manually: `./scripts/your-script.sh`

- Verify the event name is correct (case-sensitive): `PostToolUse`, not `postToolUse`

- Check the matcher pattern matches your tools: `"matcher": "Write|Edit"` for file operations

- Confirm the hook type is valid: `command`, `http`, `prompt`, or `agent`

### ​MCP server troubleshooting

- Check the command exists and is executable

- Verify all paths use `${CLAUDE_PLUGIN_ROOT}` variable

- Check the MCP server logs: `claude --debug` shows initialization errors

- Test the server manually outside of Claude Code

- Ensure the server is properly configured in `.mcp.json` or `plugin.json`

- Verify the server implements the MCP protocol correctly

- Check for connection timeouts in debug output

### ​Directory structure mistakes

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← Only manifest here
├── commands/            ← At root level
├── agents/              ← At root level
└── hooks/               ← At root level

```

- Run `claude --debug` and look for “loading plugin” messages

- Check that each component directory is listed in the debug output

- Verify file permissions allow reading the plugin files

## ​Distribution and versioning reference

### ​Version management

```
{
  "name": "my-plugin",
  "version": "2.1.0"
}

```

- MAJOR: Breaking changes (incompatible API changes)

- MINOR: New features (backward-compatible additions)

- PATCH: Bug fixes (backward-compatible fixes)

- Start at `1.0.0` for your first stable release

- Update the version in `plugin.json` before distributing changes

- Document changes in a `CHANGELOG.md` file

- Use pre-release versions like `2.0.0-beta.1` for testing

## ​See also

- Plugins - Tutorials and practical usage

- Plugin marketplaces - Creating and managing marketplaces

- Skills - Skill development details

- Subagents - Agent configuration and capabilities

- Hooks - Event handling and automation

- MCP - External tool integration

- Settings - Configuration options for plugins