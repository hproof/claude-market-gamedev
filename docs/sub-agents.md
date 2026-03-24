- Preserve context by keeping exploration and implementation out of your main conversation

- Enforce constraints by limiting which tools a subagent can use

- Reuse configurations across projects with user-level subagents

- Specialize behavior with focused system prompts for specific domains

- Control costs by routing tasks to faster, cheaper models like Haiku

## ​Built-in subagents

- Explore

- Plan

- General-purpose

- Other

- Model: Haiku (fast, low-latency)

- Tools: Read-only tools (denied access to Write and Edit tools)

- Purpose: File discovery, code search, codebase exploration

- Model: Inherits from main conversation

- Tools: Read-only tools (denied access to Write and Edit tools)

- Purpose: Codebase research for planning

- Model: Inherits from main conversation

- Tools: All tools

- Purpose: Complex research, multi-step operations, code modifications

| Agent | Model | When Claude uses it |

| --- | --- | --- |

| Bash | Inherits | Running terminal commands in a separate context |

| statusline-setup | Sonnet | When you run /statusline to configure your status line |

| Claude Code Guide | Haiku | When you ask questions about Claude Code features |

## ​Quickstart: create your first subagent

Open the subagents interface

```
/agents

```

Choose a location

Generate with Claude

```
A code improvement agent that scans files and suggests improvements
for readability, performance, and best practices. It should explain
each issue, show the current code, and provide an improved version.

```

Select tools

Select model

Choose a color

Configure memory

Save and try it out

```
Use the code-improver agent to suggest improvements in this project

```

## ​Configure subagents

### ​Use the /agents command

- View all available subagents (built-in, user, project, and plugin)

- Create new subagents with guided setup or Claude generation

- Edit existing subagent configuration and tool access

- Delete custom subagents

- See which subagents are active when duplicates exist

### ​Choose the subagent scope

| Location | Scope | Priority | How to create |

| --- | --- | --- | --- |

| --agents CLI flag | Current session | 1 (highest) | Pass JSON when launching Claude Code |

| .claude/agents/ | Current project | 2 | Interactive or manual |

| ~/.claude/agents/ | All your projects | 3 | Interactive or manual |

| Plugin’s agents/ directory | Where plugin is enabled | 4 (lowest) | Installed with plugins |

```
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'

```

### ​Write subagent files

```
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.

```

#### ​Supported frontmatter fields

| Field | Required | Description |

| --- | --- | --- |

| name | Yes | Unique identifier using lowercase letters and hyphens |

| description | Yes | When Claude should delegate to this subagent |

| tools | No | Tools the subagent can use. Inherits all tools if omitted |

| disallowedTools | No | Tools to deny, removed from inherited or specified list |

| model | No | Model to use: sonnet, opus, haiku, a full model ID (for example, claude-opus-4-6), or inherit. Defaults to inherit |

| permissionMode | No | Permission mode: default, acceptEdits, dontAsk, bypassPermissions, or plan |

| maxTurns | No | Maximum number of agentic turns before the subagent stops |

| skills | No | Skills to load into the subagent’s context at startup. The full skill content is injected, not just made available for invocation. Subagents don’t inherit skills from the parent conversation |

| mcpServers | No | MCP servers available to this subagent. Each entry is either a server name referencing an already-configured server (e.g., "slack") or an inline definition with the server name as key and a full MCP server config as value |

| hooks | No | Lifecycle hooks scoped to this subagent |

| memory | No | Persistent memory scope: user, project, or local. Enables cross-session learning |

| background | No | Set to true to always run this subagent as a background task. Default: false |

| effort | No | Effort level when this subagent is active. Overrides the session effort level. Default: inherits from session. Options: low, medium, high, max (Opus 4.6 only) |

| isolation | No | Set to worktree to run the subagent in a temporary git worktree, giving it an isolated copy of the repository. The worktree is automatically cleaned up if the subagent makes no changes |

### ​Choose a model

- Model alias: Use one of the available aliases: `sonnet`, `opus`, or `haiku`

- Full model ID: Use a full model ID such as `claude-opus-4-6` or `claude-sonnet-4-6`. Accepts the same values as the `--model` flag

- inherit: Use the same model as the main conversation

- Omitted: If not specified, defaults to `inherit` (uses the same model as the main conversation)

### ​Control subagent capabilities

#### ​Available tools

```
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---

```

```
---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---

```

#### ​Restrict which subagents can be spawned

```
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---

```

```
tools: Agent, Read, Bash

```

#### ​Scope MCP servers to a subagent

```
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.

```

#### ​Permission modes

| Mode | Behavior |

| --- | --- |

| default | Standard permission checking with prompts |

| acceptEdits | Auto-accept file edits |

| dontAsk | Auto-deny permission prompts (explicitly allowed tools still work) |

| bypassPermissions | Skip permission prompts |

| plan | Plan mode (read-only exploration) |

#### ​Preload skills into subagents

```
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.

```

#### ​Enable persistent memory

```
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.

```

| Scope | Location | Use when |

| --- | --- | --- |

| user | ~/.claude/agent-memory/<name-of-agent>/ | the subagent should remember learnings across all projects |

| project | .claude/agent-memory/<name-of-agent>/ | the subagent’s knowledge is project-specific and shareable via version control |

| local | .claude/agent-memory-local/<name-of-agent>/ | the subagent’s knowledge is project-specific but should not be checked into version control |

- The subagent’s system prompt includes instructions for reading and writing to the memory directory.

- The subagent’s system prompt also includes the first 200 lines of `MEMORY.md` in the memory directory, with instructions to curate `MEMORY.md` if it exceeds 200 lines.

- Read, Write, and Edit tools are automatically enabled so the subagent can manage its memory files.

##### Persistent memory tips

- `project` is the recommended default scope. It makes subagent knowledge shareable via version control. Use `user` when the subagent’s knowledge is broadly applicable across projects, or `local` when the knowledge should not be checked into version control.

- Ask the subagent to consult its memory before starting work: “Review this PR, and check your memory for patterns you’ve seen before.”

- Ask the subagent to update its memory after completing a task: “Now that you’re done, save what you learned to your memory.” Over time, this builds a knowledge base that makes the subagent more effective.

```
Update your agent memory as you discover codepaths, patterns, library
locations, and key architectural decisions. This builds up institutional
knowledge across conversations. Write concise notes about what you found
and where.

```

#### ​Conditional rules with hooks

```
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

```

```
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0

```

#### ​Disable specific subagents

```
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}

```

```
claude --disallowedTools "Agent(Explore)"

```

### ​Define hooks for subagents

- In the subagent’s frontmatter: Define hooks that run only while that subagent is active

- In `settings.json`: Define hooks that run in the main session when subagents start or stop

#### ​Hooks in subagent frontmatter

| Event | Matcher input | When it fires |

| --- | --- | --- |

| PreToolUse | Tool name | Before the subagent uses a tool |

| PostToolUse | Tool name | After the subagent uses a tool |

| Stop | (none) | When the subagent finishes (converted to SubagentStop at runtime) |

```
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---

```

#### ​Project-level hooks for subagent events

| Event | Matcher input | When it fires |

| --- | --- | --- |

| SubagentStart | Agent type name | When a subagent begins execution |

| SubagentStop | Agent type name | When a subagent completes |

```
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}

```

## ​Work with subagents

### ​Understand automatic delegation

### ​Invoke subagents explicitly

- Natural language: name the subagent in your prompt; Claude decides whether to delegate

- @-mention: guarantees the subagent runs for one task

- Session-wide: the whole session uses that subagent’s system prompt, tool restrictions, and model via the `--agent` flag or the `agent` setting

```
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes

```

```
@"code-reviewer (agent)" look at the auth changes

```

```
claude --agent code-reviewer

```

```
{
  "agent": "code-reviewer"
}

```

### ​Run subagents in foreground or background

- Foreground subagents block the main conversation until complete. Permission prompts and clarifying questions (like `AskUserQuestion`) are passed through to you.

- Background subagents run concurrently while you continue working. Before launching, Claude Code prompts for any tool permissions the subagent will need, ensuring it has the necessary approvals upfront. Once running, the subagent inherits these permissions and auto-denies anything not pre-approved. If a background subagent needs to ask clarifying questions, that tool call fails but the subagent continues.

- Ask Claude to “run this in the background”

- Press Ctrl+B to background a running task

### ​Common patterns

#### ​Isolate high-volume operations

```
Use a subagent to run the test suite and report only the failing tests with their error messages

```

#### ​Run parallel research

```
Research the authentication, database, and API modules in parallel using separate subagents

```

#### ​Chain subagents

```
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them

```

### ​Choose between subagents and main conversation

- The task needs frequent back-and-forth or iterative refinement

- Multiple phases share significant context (planning → implementation → testing)

- You’re making a quick, targeted change

- Latency matters. Subagents start fresh and may need time to gather context

- The task produces verbose output you don’t need in your main context

- You want to enforce specific tool restrictions or permissions

- The work is self-contained and can return a summary

### ​Manage subagent context

#### ​Resume subagents

```
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]

```

- Main conversation compaction: When the main conversation compacts, subagent transcripts are unaffected. They’re stored in separate files.

- Session persistence: Subagent transcripts persist within their session. You can resume a subagent after restarting Claude Code by resuming the same session.

- Automatic cleanup: Transcripts are cleaned up based on the `cleanupPeriodDays` setting (default: 30 days).

#### ​Auto-compaction

```
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}

```

## ​Example subagents

- Design focused subagents: each subagent should excel at one specific task

- Write detailed descriptions: Claude uses the description to decide when to delegate

- Limit tool access: grant only necessary permissions for security and focus

- Check into version control: share project subagents with your team

### ​Code reviewer

```
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.

```

### ​Debugger

```
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.

```

### ​Data scientist

```
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.

```

### ​Database query validator

```
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.

```

```
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0

```

```
chmod +x ./scripts/validate-readonly-query.sh

```

## ​Next steps

- Distribute subagents with plugins to share subagents across teams or projects

- Run Claude Code programmatically with the Agent SDK for CI/CD and automation

- Use MCP servers to give subagents access to external tools and data