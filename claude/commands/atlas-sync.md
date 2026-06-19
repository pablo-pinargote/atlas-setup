---
description: Regenerate the current Atlas's STATUS.md digest (and update CLAUDE.md if a standing decision changed), per the Atlas model defined in the Atlas framework.
argument-hint: [optional focus area]
---

Checkpoint the current Atlas's memory now. **The model — what STATUS holds, what CLAUDE holds, the digest rules, file naming — is DEFINED IN THE ATLAS FRAMEWORK. Do not restate or improvise it here; fetch it and apply it.**

Optional focus: $ARGUMENTS

1. **Load the definition:** `bash ~/.claude/atlas-fetch.sh method/02-stores-model.md` and `bash ~/.claude/atlas-fetch.sh method/03-atlas-anatomy.md` (the files of record + the "Adding or removing a repo" reconciliation), or invoke the `workspace-baseline` skill. `atlas-fetch.sh` reads the single source in `~/.claude/atlas-source` (URL → curl, local clone → cat). That returns the Atlas stores model — how `STATUS.md` and `CLAUDE.md` work and what goes where. If the fetch fails, surface it — don't improvise.
2. **Locate the Atlas root** — nearest dir at/above CWD with `STATUS.md`. If none, say it's not an Atlas and stop.
3. **Reconcile the repo set** (sync owns this — adding/removing a repo is a sync, not a re-init): compare the symlinks present in the Atlas root against the per-repo orientation blocks in `CLAUDE.md` §1 and the `additionalDirectories` in `.claude/settings.local.json`.
   - **Repo added** → add its per-repo orientation block (role · contributes · stack · cadence — read its README; ask if ambiguous) and add its real target path to `additionalDirectories`.
   - **Repo removed** → flag the stale block + settings entry and **ask before deleting**.
4. **Apply the model:** regenerate `STATUS.md` exactly as the framework defines it (a digest of the `BACKLOG`/`SPEC_`/`DRAFT_`/`_archived` artifacts), and update `CLAUDE.md` only if a standing decision/orientation fact changed (the repo-set reconciliation in step 3 is one such change). Let the framework decide what belongs where — your job is to apply that definition to this session, not duplicate it.
5. **Report** what you wrote to `STATUS.md`, `CLAUDE.md` (incl. any repo blocks added/removed), and `.claude/settings.local.json`.
