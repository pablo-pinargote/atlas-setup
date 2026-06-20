# Atlas — partner setup guide (macOS + Windows)

A **manual, copy-paste** setup. No install script: every step is a command you run yourself,
so you see exactly what it does. The only file you edit by hand is `settings.json`, and you
back it up first — nothing here overwrites your existing Claude Code config.

> **What Atlas is:** a tool-agnostic, spec-driven way to run large, multi-repo, AI-assisted
> projects — any agent opens a project cold and knows what it is, where it lives, where the work
> stands, and how it ships. Full framework: **https://atlas.paranoid.software**.

> **Deferred (later guide):** the shared **memory store** and the **DEVIATIONS** workflow. The
> Atlas lifecycle works fully without them.

---

## 0. Before you start — prerequisites

> **Windows users:** do **everything** below in **Git Bash** (installed with Git for Windows),
> not PowerShell/cmd. The Atlas tooling is bash + `jq`/`curl`, and Claude Code runs the hooks
> through Git Bash. Install tools with `winget` in PowerShell, then **reopen Git Bash**.

Install these once:

| Tool | What it's for here | macOS (Terminal) | Windows (PowerShell, then reopen Git Bash) |
|---|---|---|---|
| **Git** (+ Git Bash) | Clone the framework (option B). On **Windows**, Git Bash is the shell that runs the Atlas hooks and scripts. | `brew install git` | `winget install Git.Git` |
| **jq** | A small command-line **JSON tool**. Claude Code passes each hook a blob of JSON (the prompt, session info); the hooks use `jq` to read it and to build their JSON reply. You also use `jq` to check `settings.json` is valid. Without it, the hooks fail. | `brew install jq` | `winget install jqlang.jq` |
| **Python 3** | Runs the generator (`gen_workspaces.py`) that turns a `.code-workspace` into the Atlas's symlink folder. | `brew install python` (or preinstalled) | `winget install Python.Python.3.12` |

**Windows only — allow symlinks:** Settings → *Privacy & security* → *For developers* →
turn **Developer Mode ON**. (Lets the generator create symlinks without admin.)

Check everything is there (Terminal / Git Bash):

```bash
git --version
jq --version
claude --version
python3 --version || python --version
```

*Each line prints a version number — that's how you confirm the tool is installed and on your
PATH. (`||` means "try `python3`; if it's missing, try `python`.")*

You also need **this `atlas-setup` folder** on your machine and **your repos already cloned**.

---

## 1. Create the workspaces folder

Run in Terminal / Git Bash:

```bash
mkdir -p ~/workspaces
```
*`mkdir -p` makes the folder; `-p` means "don't error if it already exists, create parents as needed."*

Create its `.gitignore` (generated Atlas folders and local junk):

```bash
printf '_*/\n.venv/\n.idea/\n' > ~/workspaces/.gitignore
```
*`printf … > file` writes those lines into a file. This tells git to ignore the generated
`_<name>/` Atlas folders (they're just symlinks, rebuilt by the generator).*

**Model:** under `workspaces/` you make a subfolder per concept; inside it a `.code-workspace`
file lists the repos for a task; the generator turns that into a `_<name>/` folder of symlinks —
**that folder is your Atlas.**

## 2. Copy the generator

First go into this `atlas-setup` folder (so the copy commands are simple). Replace the path with
where you put it:

```bash
cd ~/atlas-setup     # ← wherever this folder lives on your machine
```

Copy the generator into the workspaces folder:

```bash
cp gen_workspaces.py ~/workspaces/
```
*`cp <source> <dest>` copies a file. This places the generator where you'll run it from.*

## 3. Pick the framework source

You'll set this in step 4. Choose **one**:

- **A — Public site:** `https://atlas.paranoid.software`
- **B — Local clone** *(recommended for the workshop — works offline):*
  ```bash
  git clone https://github.com/paranoid-software/atlas.git ~/atlas
  ```
  The source is then the folder path: `~/atlas`

## 4. Install the Atlas machinery (manual)

Still inside the `atlas-setup` folder. Each command copies one known thing to one known place.

**4.1 — Make the folders** inside your Claude Code config dir (`~/.claude/`):

```bash
mkdir -p ~/.claude/hooks ~/.claude/commands ~/.claude/skills/workspace-baseline
```

**4.2 — Copy the files.** Each line copies one piece into `~/.claude/`: the **fetch helper**
(reads the framework), the **3 hooks**, the **2 slash-commands** (`/atlas-init`, `/atlas-sync`),
and the **skill** that routes Atlas work. Nothing here touches your existing files.

```bash
cp claude/atlas-fetch.sh                              ~/.claude/   # reads atlas-source, fetches framework files
cp claude/hooks/session-orient.sh                     ~/.claude/hooks/   # shows STATUS.md at session start
cp claude/hooks/atlas-sync-reminder.sh                ~/.claude/hooks/   # nudges /atlas-sync when STATUS is stale
cp claude/hooks/skill-reminder-workspace-baseline.sh  ~/.claude/hooks/   # routes Atlas prompts to the skill
cp claude/commands/atlas-init.md                      ~/.claude/commands/   # the /atlas-init command
cp claude/commands/atlas-sync.md                      ~/.claude/commands/   # the /atlas-sync command
cp claude/skills/workspace-baseline/SKILL.md          ~/.claude/skills/workspace-baseline/   # the entry-point skill
```

**4.3 — Set the framework source** — one line, pick the value from step 3:

```bash
# Public site:
printf '%s\n' 'https://atlas.paranoid.software' > ~/.claude/atlas-source

# …OR the local clone (use the real absolute path — see step 6 for how to get one):
printf '%s\n' "$HOME/atlas" > ~/.claude/atlas-source
```
*Run **only one** of the two. This writes a single line into `~/.claude/atlas-source` — the one
place that says where the framework lives. `atlas-fetch` reads that line: if it starts with
`http` it downloads with `curl`; otherwise it treats it as a local folder and reads with `cat`.*

Test it before going further:

```bash
bash ~/.claude/atlas-fetch.sh llms.txt | head -3
```
*`atlas-fetch.sh llms.txt` asks the framework for its index file; `head -3` shows the first 3
lines. This is exactly how the Atlas commands read the framework — if it works here, they work.*

You should see the framework index. If you get a `configure ~/.claude/atlas-source` error or a
timeout, fix the source line above (the clone path is the most reliable).

## 5. Add the 3 hooks to `settings.json` (by hand)

**5.1 — Back it up first** (so you can always undo):

```bash
cp ~/.claude/settings.json ~/.claude/settings.json.bak 2>/dev/null || echo "{}" > ~/.claude/settings.json
```
*Copies your current settings to a `.bak` you can restore from. If you don't have a
`settings.json` yet, the `|| …` part creates an empty one (`{}`) so the next steps have a file
to edit.*

**5.2 — Open it** in your editor:

```bash
code ~/.claude/settings.json      # VS Code; or open it with any text editor
```

**5.3 — Add two things**, keeping everything you already have:

**(a)** ensure this key exists at the top level (add it if missing — it's the framework
recommendation; leave it as-is if you intentionally use auto-memory):

```json
"autoMemoryEnabled": false,
```

**(b)** add the three hooks. **If you have NO `"hooks"` section yet**, paste this whole block:

```json
"hooks": {
  "SessionStart": [
    { "hooks": [ { "type": "command", "command": "bash \"$HOME/.claude/hooks/session-orient.sh\"" } ] }
  ],
  "Stop": [
    { "hooks": [ { "type": "command", "command": "bash \"$HOME/.claude/hooks/atlas-sync-reminder.sh\"" } ] }
  ],
  "UserPromptSubmit": [
    { "hooks": [ { "type": "command", "command": "bash \"$HOME/.claude/hooks/skill-reminder-workspace-baseline.sh\"" } ] }
  ]
}
```

**If you ALREADY have a `"hooks"` section**, don't replace it — just add **one entry** into each
of the three arrays (create the array if that event isn't there). For example, an existing
`SessionStart` becomes:

```json
"SessionStart": [
  { "hooks": [ { "type": "command", "command": "your-existing-hook" } ] },
  { "hooks": [ { "type": "command", "command": "bash \"$HOME/.claude/hooks/session-orient.sh\"" } ] }
]
```

**5.4 — Save**, and confirm it's valid JSON:

```bash
jq . ~/.claude/settings.json >/dev/null && echo "settings.json OK"
```
*`jq .` parses the file and re-prints it; `>/dev/null` hides that output, so you only see
`settings.json OK` if it parsed. This catches typos before Claude Code chokes on them.*

If `jq` reports an error, you have a typo (usually a missing or extra comma) — fix it or restore
the backup: `cp ~/.claude/settings.json.bak ~/.claude/settings.json`.

## 6. Create your first Atlas

**6.1 — Get your repos' absolute paths.** In Terminal / Git Bash, `cd` into each repo and run
`pwd`:

```bash
cd /path/to/your/repo-a && pwd
```
*`cd` moves into the folder; `pwd` ("print working directory") prints its full absolute path —
that exact string is what the `.code-workspace` needs.*
- macOS prints e.g. `/Users/you/repo-a`
- Windows Git Bash prints e.g. `/c/Users/you/repo-a`
- (Shortcut on macOS: drag the folder onto the Terminal window to paste its path.)

**6.2 — Write a `.code-workspace`** listing those paths:

```bash
mkdir -p ~/workspaces/demo
cat > ~/workspaces/demo/first.code-workspace <<'EOF'
{
  "folders": [
    { "path": "/Users/you/repo-a" },
    { "path": "/Users/you/repo-b" }
  ]
}
EOF
```
*`cat > file <<'EOF' … EOF` writes everything between the two `EOF` markers into the file. (Or
just create the file in a text editor and paste the JSON.) Replace the two paths with what `pwd`
gave you.*

**6.3 — Generate the Atlas** (`python3` on macOS; `python` on Windows if `python3` isn't found):

```bash
cd ~/workspaces
python3 gen_workspaces.py demo/first.code-workspace
```

This creates `~/workspaces/demo/_first/` with a symlink to each repo.

**6.4 — Bootstrap it in Claude Code.** Open `demo/_first/` in Claude Code and run:

```
/atlas-init
```

It fetches the recipe from the framework and creates `CLAUDE.md` (a per-repo block per symlink),
`STATUS.md`, `BACKLOG.md`, `DEVIATIONS.md`, `_archived/`, and `.claude/settings.local.json`.

## 7. Day to day

- **Session start** auto-shows `STATUS.md` so you never start cold (the `session-orient` hook).
- **Added/removed a repo?** Edit the `.code-workspace`, re-run `python3 gen_workspaces.py …`,
  then run `/atlas-sync` (it reconciles the repo set; `/atlas-init` does not).
- **Checkpoint progress:** `/atlas-sync` regenerates `STATUS.md`.

## 8. Using Atlas from Cursor (no extra setup)

If you also use **Cursor**, you don't configure anything for Atlas there. Recent Cursor reads
**Claude Code's config from `~/.claude/`** — so once you've done step 4, Cursor automatically gets:

- the **hooks** (incl. `session-orient`, so it opens an Atlas already oriented),
- the **commands** (`/atlas-init`, `/atlas-sync`),
- the **skill** (`workspace-baseline`).

They show up under **"Claude User config"** in Cursor's *Settings → Hooks* and *Rules, Skills,
Subagents* tabs. **Do not copy these into `~/.cursor/`** — that just creates duplicates. The one
thing that is per-tool is the memory store: when you set up coco/mem0 later, add it to Cursor's
own MCP config (`~/.cursor/mcp.json`) too.

> Quick check it's live: open an Atlas in Cursor, start a new Agent chat, and ask "what's the
> state of this Atlas?" without giving context — it should already know from `STATUS.md`.

## 9. Using Atlas from Antigravity (real setup)

Antigravity (Google's IDE) does **not** read `~/.claude/`, so it needs its own setup. It uses
`~/.gemini/` for everything. From this folder, in Terminal / Git Bash:

```bash
mkdir -p ~/.gemini/skills/workspace-baseline

cp gemini/atlas-fetch.sh                         ~/.gemini/atlas-fetch.sh
cp gemini/skills/workspace-baseline/SKILL.md     ~/.gemini/skills/workspace-baseline/SKILL.md
chmod +x ~/.gemini/atlas-fetch.sh

# framework source (one line — URL or local clone)
printf '%s\n' 'https://atlas.paranoid.software' > ~/.gemini/atlas-source
```

**Orientation rule.** Antigravity has no Claude-style session hooks, so orientation is an
**always-on global rule** in `~/.gemini/GEMINI.md`. Append the contents of
`gemini/GEMINI.atlas-section.md` to your `~/.gemini/GEMINI.md` (don't overwrite — that file is
**shared with Gemini CLI**, so keep anything already there):

```bash
cat gemini/GEMINI.atlas-section.md >> ~/.gemini/GEMINI.md
```

**Memory store (coco/mem0).** Per-tool, like everywhere — add it to Antigravity's MCP config
`~/.gemini/config/mcp_config.json` when you set up the memory store (deferred).

**Verify:**

```bash
bash ~/.gemini/atlas-fetch.sh llms.txt | head -3    # should print the framework index
```

Then in Antigravity: confirm the **`workspace-baseline`** skill shows up (Skills panel) and that
opening an Atlas orients the agent (the `GEMINI.md` rule). What you get: coco (memory) + the
skill + the orientation rule + framework access — functional parity with Claude/Cursor. The one
gap is convenience slash-commands (`/atlas-init`, `/atlas-sync`): the **skill covers that work**
(ask it to bootstrap/sync); add Antigravity *Workflows* via its UI later if you want the
shortcuts.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `configure ~/.claude/atlas-source` | Re-do step 4.3 with a valid URL or clone path. |
| `jq: command not found` | Install jq (step 0); on Windows **reopen Git Bash** after installing. |
| Hooks do nothing on Windows | You're not in **Git Bash**, or Git for Windows isn't installed (step 0). |
| `gen_workspaces.py` symlink error (Windows) | Turn on **Developer Mode** (step 0), then re-run. |
| Public URL times out | Use the **local clone** (step 3B) and redo step 4.3. |
| Broke `settings.json` | `cp ~/.claude/settings.json.bak ~/.claude/settings.json` |

## What's in this folder

```
atlas-setup/
├── README.md                  ← this guide
├── gen_workspaces.py          ← the Atlas generator (you copy it in step 2)
├── claude/                    ← Claude Code machinery (step 4) — Cursor inherits it via interop
│   ├── atlas-fetch.sh
│   ├── atlas-source.example   ← reference only (step 4.3 creates the real one)
│   ├── hooks/                 ← session-orient · atlas-sync-reminder · skill-reminder
│   ├── commands/              ← /atlas-init · /atlas-sync
│   └── skills/workspace-baseline/SKILL.md
└── gemini/                    ← Antigravity setup (step 9) — its own ~/.gemini/ files
    ├── atlas-fetch.sh
    ├── atlas-source.example
    ├── GEMINI.atlas-section.md ← append to ~/.gemini/GEMINI.md (orientation rule)
    └── skills/workspace-baseline/SKILL.md
```

## Which tools need what

| Tool | coco (MCP) | hooks / commands / skills | Setup needed |
|---|---|---|---|
| **Claude Code** | its own config | native (`~/.claude/`) | steps 1–7 |
| **Cursor** | its own config | **inherits Claude's** via interop | nothing (just verify) |
| **Antigravity** | its own config (`~/.gemini/...`) | **its own** (`~/.gemini/`) | step 9 |
