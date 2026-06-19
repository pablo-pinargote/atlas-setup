---
description: Bootstrap the current directory as a new Atlas, following the canonical recipe defined in the Atlas framework.
argument-hint: [optional topic name]
---

Bootstrap the current directory as a new Atlas. **The recipe — which files to create, the scaffold, the naming, the templates — is DEFINED IN THE ATLAS FRAMEWORK. Do not improvise or restate it here; fetch it and execute it.**

Optional topic name: $ARGUMENTS

1. **Load the recipe:** invoke the `workspace-baseline` skill, or fetch it directly:
   ```
   bash ~/.claude/atlas-fetch.sh method/06-bootstrap.md   # bootstrap recipe + Atlas CLAUDE.md template
   bash ~/.claude/atlas-fetch.sh method/03-atlas-anatomy.md   # files of record + naming (if needed)
   ```
   `atlas-fetch.sh` reads the single source in `~/.claude/atlas-source` (a URL → curl, or a local clone → cat). The framework is the source of truth; this command only triggers it. If the fetch fails, surface it — don't improvise.
2. **Pre-flight:** CWD must be a fresh Atlas dir — symlinks to real repos present, and no `CLAUDE.md` yet. **Bootstrap runs once.** If a baseline already exists → STOP and redirect to **`/atlas-sync`** — that's the command that reconciles an existing Atlas, including **adding or removing repos** (sync owns the repo set, init does not). If there are no symlinks → STOP and ask the user to create the Atlas dir + symlinks first (that's the user's step, not this command's).
3. **Execute the recipe** step by step, exactly as the framework defines it — including reading each repo's `readme.md`/`package.json` for its per-repo orientation block and asking the user when ambiguous.
4. **Report** what was created.
