## ​Bundled skills

| Skill | Purpose |

| --- | --- |

| /batch <instruction> | Orchestrate large-scale changes across a codebase in parallel. Researches the codebase, decomposes the work into 5 to 30 independent units, and presents a plan. Once approved, spawns one background agent per unit in an isolated git worktree. Each agent implements its unit, runs tests, and opens a pull request. Requires a git repository. Example: /batch migrate src/ from Solid to React |

| /claude-api | Load Claude API reference material for your project’s language (Python, TypeScript, Java, Go, Ruby, C#, PHP, or cURL) and Agent SDK reference for Python and TypeScript. Covers tool use, streaming, batches, structured outputs, and common pitfalls. Also activates automatically when your code imports anthropic, @anthropic-ai/sdk, or claude_agent_sdk |

| /debug [description] | Troubleshoot your current Claude Code session by reading the session debug log. Optionally describe the issue to focus the analysis |

| /loop [interval] <prompt> | Run a prompt repeatedly on an interval while the session stays open. Useful for polling a deployment, babysitting a PR, or periodically re-running another skill. Example: /loop 5m check if the deploy finished. See Run prompts on a schedule |

| /simplify [focus] | Review your recently changed files for code reuse, quality, and efficiency issues, then fix them. Spawns three review agents in parallel, aggregates their findings, and applies fixes. Pass text to focus on specific concerns: /simplify focus on memory efficiency |

## ​Getting started

### ​Create your first skill

Create the skill directory

```
mkdir -p ~/.claude/skills/explain-code

```

Write SKILL.md

```
---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

When explaining code, always include:

1. **Start with an analogy**: Compare the code to something from everyday life
2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
3. **Walk through the code**: Explain step-by-step what happens
4. **Highlight a gotcha**: What's a common mistake or misconception?

Keep explanations conversational. For complex concepts, use multiple analogies.

```

Test the skill

```
How does this code work?

```

```
/explain-code src/auth/login.ts

```

### ​Where skills live

| Location | Path | Applies to |

| --- | --- | --- |

| Enterprise | See managed settings | All users in your organization |

| Personal | ~/.claude/skills/<skill-name>/SKILL.md | All your projects |

| Project | .claude/skills/<skill-name>/SKILL.md | This project only |

| Plugin | <plugin>/skills/<skill-name>/SKILL.md | Where plugin is enabled |

#### ​Automatic discovery from nested directories

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute

```

#### ​Skills from additional directories

## ​Configure skills

### ​Types of skill content

```
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation

```

```
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target

```

### ​Frontmatter reference

```
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read, Grep
---

Your skill instructions here...

```

| Field | Required | Description |

| --- | --- | --- |

| name | No | Display name for the skill. If omitted, uses the directory name. Lowercase letters, numbers, and hyphens only (max 64 characters). |

| description | Recommended | What the skill does and when to use it. Claude uses this to decide when to apply the skill. If omitted, uses the first paragraph of markdown content. |

| argument-hint | No | Hint shown during autocomplete to indicate expected arguments. Example: [issue-number] or [filename] [format]. |

| disable-model-invocation | No | Set to true to prevent Claude from automatically loading this skill. Use for workflows you want to trigger manually with /name. Default: false. |

| user-invocable | No | Set to false to hide from the / menu. Use for background knowledge users shouldn’t invoke directly. Default: true. |

| allowed-tools | No | Tools Claude can use without asking permission when this skill is active. |

| model | No | Model to use when this skill is active. |

| effort | No | Effort level when this skill is active. Overrides the session effort level. Default: inherits from session. Options: low, medium, high, max (Opus 4.6 only). |

| context | No | Set to fork to run in a forked subagent context. |

| agent | No | Which subagent type to use when context: fork is set. |

| hooks | No | Hooks scoped to this skill’s lifecycle. See Hooks in skills and agents for configuration format. |

#### ​Available string substitutions

| Variable | Description |

| --- | --- |

| $ARGUMENTS | All arguments passed when invoking the skill. If $ARGUMENTS is not present in the content, arguments are appended as ARGUMENTS: <value>. |

| $ARGUMENTS[N] | Access a specific argument by 0-based index, such as $ARGUMENTS[0] for the first argument. |

| $N | Shorthand for $ARGUMENTS[N], such as $0 for the first argument or $1 for the second. |

| ${CLAUDE_SESSION_ID} | The current session ID. Useful for logging, creating session-specific files, or correlating skill output with sessions. |

| ${CLAUDE_SKILL_DIR} | The directory containing the skill’s SKILL.md file. For plugin skills, this is the skill’s subdirectory within the plugin, not the plugin root. Use this in bash injection commands to reference scripts or files bundled with the skill, regardless of the current working directory. |

| ${CLAUDE_PROJECT_ROOT} | The root directory of the project where Claude Code is running. Use this to write files to the project root, regardless of the current working directory. |

```
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS

```

### ​Add supporting files

```
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)

```

```
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)

```

### ​Control who invokes a skill

- `disable-model-invocation: true`: Only you can invoke the skill. Use this for workflows with side effects or that you want to control timing, like `/commit`, `/deploy`, or `/send-slack-message`. You don’t want Claude deciding to deploy because your code looks ready.

- `user-invocable: false`: Only Claude can invoke the skill. Use this for background knowledge that isn’t actionable as a command. A `legacy-system-context` skill explains how an old system works. Claude should know this when relevant, but `/legacy-system-context` isn’t a meaningful action for users to take.

```
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded

```

| Frontmatter | You can invoke | Claude can invoke | When loaded into context |

| --- | --- | --- | --- |

| (default) | Yes | Yes | Description always in context, full skill loads when invoked |

| disable-model-invocation: true | Yes | No | Description not in context, full skill loads when you invoke |

| user-invocable: false | No | Yes | Description always in context, full skill loads when invoked |

### ​Restrict tool access

```
---
name: safe-reader
description: Read files without making changes
allowed-tools: Read, Grep, Glob
---

```

### ​Pass arguments to skills

```
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit

```

```
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.

```

```
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.

```

## ​Advanced patterns

### ​Inject dynamic context

```
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...

```

- Each `!`<command>`` executes immediately (before Claude sees anything)

- The output replaces the placeholder in the skill content

- Claude receives the fully-rendered prompt with actual PR data

### ​Run skills in a subagent

| Approach | System prompt | Task | Also loads |

| --- | --- | --- | --- |

| Skill with context: fork | From agent type (Explore, Plan, etc.) | SKILL.md content | CLAUDE.md |

| Subagent with skills field | Subagent’s markdown body | Claude’s delegation message | Preloaded skills + CLAUDE.md |

#### ​Example: Research skill using Explore agent

```
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references

```

- A new isolated context is created

- The subagent receives the skill content as its prompt (“Research $ARGUMENTS thoroughly…”)

- The `agent` field determines the execution environment (model, tools, and permissions)

- Results are summarized and returned to your main conversation

### ​Restrict Claude’s skill access

```
# Add to deny rules:
Skill

```

```
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)

```

## ​Share skills

- Project skills: Commit `.claude/skills/` to version control

- Plugins: Create a `skills/` directory in your plugin

- Managed: Deploy organization-wide through managed settings

### ​Generate visual output

```
mkdir -p ~/.claude/skills/codebase-visualizer/scripts

```

```
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python *)
---

# Codebase Visualizer

Generate an interactive HTML tree view that shows your project's file structure with collapsible directories.

## Usage

Run the visualization script from your project root:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

This creates `codebase-map.html` in the current directory and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder

```

- A summary sidebar showing file count, directory count, total size, and number of file types

- A bar chart breaking down the codebase by file type (top 8 by size)

- A collapsible tree where you can expand and collapse directories, with color-coded file type indicators

```
#!/usr/bin/env python3
"""Generate an interactive collapsible tree visualization of a codebase."""

import json
import sys
import webbrowser
from pathlib import Path
from collections import Counter

IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]
    colors = {
        '.js': '#f7df1e', '.ts': '#3178c6', '.py': '#3776ab', '.go': '#00add8',
        '.rs': '#dea584', '.rb': '#cc342d', '.css': '#264de4', '.html': '#e34c26',
        '.json': '#6b7280', '.md': '#083fa1', '.yaml': '#cb171e', '.yml': '#cb171e',
        '.mdx': '#083fa1', '.tsx': '#3178c6', '.jsx': '#61dafb', '.sh': '#4eaa25',
    }
    lang_bars = "".join(
        f'<div class="bar-row"><span class="bar-label">{ext}</span>'
        f'<div class="bar" style="width:{(size/total_size)*100}%;background:{colors.get(ext,"#6b7280")}"></div>'
        f'<span class="bar-pct">{(size/total_size)*100:.1f}%</span></div>'
        for ext, size in sorted_exts
    )
    def fmt(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.1f} MB"

    html = f'''<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"><title>Codebase Explorer</title>
  <style>
    body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
    .container {{ display: flex; height: 100vh; }}
    .sidebar {{ width: 280px; background: #252542; padding: 20px; border-right: 1px solid #3d3d5c; overflow-y: auto; flex-shrink: 0; }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 10px 0; font-size: 18px; }}
    h2 {{ margin: 20px 0 10px 0; font-size: 14px; color: #888; text-transform: uppercase; }}
    .stat {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #3d3d5c; }}
    .stat-value {{ font-weight: bold; }}
    .bar-row {{ display: flex; align-items: center; margin: 6px 0; }}
    .bar-label {{ width: 55px; font-size: 12px; color: #aaa; }}
    .bar {{ height: 18px; border-radius: 3px; }}
    .bar-pct {{ margin-left: 8px; font-size: 12px; color: #666; }}
    .tree {{ list-style: none; padding-left: 20px; }}
    details {{ cursor: pointer; }}
    summary {{ padding: 4px 8px; border-radius: 4px; }}
    summary:hover {{ background: #2d2d44; }}
    .folder {{ color: #ffd700; }}
    .file {{ display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; }}
    .file:hover {{ background: #2d2d44; }}
    .size {{ color: #888; margin-left: auto; font-size: 12px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
  </style>
</head><body>
  <div class="container">
    <div class="sidebar">
      <h1>📊 Summary</h1>
      <div class="stat"><span>Files</span><span class="stat-value">{stats["files"]:,}</span></div>
      <div class="stat"><span>Directories</span><span class="stat-value">{stats["dirs"]:,}</span></div>
      <div class="stat"><span>Total size</span><span class="stat-value">{fmt(data["size"])}</span></div>
      <div class="stat"><span>File types</span><span class="stat-value">{len(stats["extensions"])}</span></div>
      <h2>By file type</h2>
      {lang_bars}
    </div>
    <div class="main">
      <h1>📁 {data["name"]}</h1>
      <ul class="tree" id="root"></ul>
    </div>
  </div>
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `<summary><span class="folder">📁 ${{node.name}}</span><span class="size">${{fmt(node.size)}}</span></summary>`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `<span class="dot" style="background:${{colors[node.ext]||'#6b7280'}}"></span>${{node.name}}<span class="size">${{fmt(node.size)}}</span>`;
        parent.appendChild(li);
      }}
    }}
    data.children.forEach(c => render(c, document.getElementById('root')));
  </script>
</body></html>'''
    output.write_text(html)

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')

```

## ​Troubleshooting

### ​Skill not triggering

- Check the description includes keywords users would naturally say

- Verify the skill appears in `What skills are available?`

- Try rephrasing your request to match the description more closely

- Invoke it directly with `/skill-name` if the skill is user-invocable

### ​Skill triggers too often

- Make the description more specific

- Add `disable-model-invocation: true` if you only want manual invocation

### ​Claude doesn’t see all my skills

## ​Related resources

- Subagents: delegate tasks to specialized agents

- Plugins: package and distribute skills with other extensions

- Hooks: automate workflows around tool events

- Memory: manage CLAUDE.md files for persistent context

- Built-in commands: reference for built-in `/` commands

- Permissions: control tool and skill access