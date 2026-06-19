---
name: workspace-baseline
description: Use when bootstrapping a new Atlas (symlink-aggregator project root), editing CLAUDE.md / STATUS.md / BACKLOG.md / DEVIATIONS.md / SPEC_*.md / DRAFT_*.md / _archived/, deciding where a piece of knowledge belongs across the stores, or auditing the user-global setup. The canonical Atlas framework (architecture + bootstrap recipe) lives in the Atlas framework doc, fetched via `~/.claude/atlas-fetch.sh`. This skill is the entry point — fetch the framework, then act.
---

# workspace-baseline

The canonical Atlas framework (architecture + bootstrap recipe) lives in the **Atlas framework doc**, fetched via `~/.claude/atlas-fetch.sh` from the source configured in `~/.claude/atlas-source` (the official site `https://atlas.paranoid.software`, or a local clone). This skill is the entry point: fetch the framework, then act.

> **Memory store & deviations are not wired up yet** in this baseline setup. The framework describes a *required* cross-tool memory store (and an optional candidates-promotion flow); configuring one is a later step. For now, universal-rule promotion and the `DEVIATIONS` workflow are deferred.

## Step 1 — load the framework definition

```
bash ~/.claude/atlas-fetch.sh llms.txt          # the index — start here
bash ~/.claude/atlas-fetch.sh llms-full.txt     # the whole framework in one file
bash ~/.claude/atlas-fetch.sh method/06-bootstrap.md   # a specific piece
```

`atlas-fetch.sh` resolves the single source in `~/.claude/atlas-source`: a URL → `curl`, a local path → `cat`. If it fails, the source is unreachable / misconfigured — surface that, don't improvise the framework from memory.

Returns the Atlas framework:

- **The Atlas model** (`method/01-the-atlas.md`) — an **Atlas** is a symlink-aggregator project root; why it exists.
- **The stores model** (`method/02-stores-model.md`) — where each kind of knowledge lives; the decision tree.
- **Atlas anatomy** (`method/03-atlas-anatomy.md`) — the root files of record (incl. `STATUS.md`), naming, the per-repo orientation block.
- **The SPEC lifecycle** (`method/04-spec-lifecycle.md`) — READY → IN PROGRESS → IN REVIEW → SHIPPED → archived.
- **The discipline** (`method/05-discipline.md`) — small deliverable specs; review before shipped; clean baseline; commit-message hygiene.
- **The bootstrap recipe + Atlas `CLAUDE.md` template** (`method/06-bootstrap.md`).
- **Optional git-versioning** (`method/07-optional-git-versioning.md`).

## Step 2 — apply per the framework

- **Bootstrapping a new Atlas** → follow the recipe (`method/06-bootstrap.md`).
- **Modifying any Atlas root file of record** (`CLAUDE.md`, `STATUS.md`, `BACKLOG.md`, `SPEC_*.md`, `DRAFT_*.md`, `DEVIATIONS.md`, `_archived/`) → consult the stores model / anatomy (`method/02`, `method/03`) for what goes in each. `STATUS.md` = the living "where we are", injected at session start by the `session-orient.sh` hook; CLAUDE.md = static orientation/why.
- **Deciding where a piece of knowledge belongs** → use the decision tree in the stores model (`method/02-stores-model.md`).

## Commands (the on-demand entry points)

Two user-global slash commands operate on an Atlas; both are thin wrappers that fetch and follow the canonical recipe/model in the Atlas framework (`atlas-fetch.sh`):

- **`/atlas-init`** — bootstrap the current directory as a new Atlas (discovers symlinks, creates `CLAUDE.md` with per-repo blocks, `.claude/settings.local.json`, `STATUS.md`, `BACKLOG.md`, `DEVIATIONS.md`, `_archived/`). Pre-flight stops if a baseline already exists or there are no symlinks.
- **`/atlas-sync`** — reconcile an existing Atlas: regenerate `STATUS.md` and, when the repo set changed, add/remove per-repo orientation blocks (sync owns adding/removing repos — init does not).

Memory mechanism: a `SessionStart` hook (`session-orient.sh`) injects `STATUS.md` at start; a `Stop` hook (`atlas-sync-reminder.sh`) nudges the agent to offer `/atlas-sync` when `STATUS.md` goes stale (throttled). There is no automatic write — checkpointing is deliberate.

## Naming

The concept is an **Atlas** (a map of the project's repos), NOT a "workspace" — "workspace" is overloaded. An Atlas directory is conventionally `_<topic>/` (the generator names it from the `.code-workspace` file).

## What is NOT in this skill

- The actual architecture text → in the Atlas framework doc (`atlas-fetch.sh`).
- The actual CLAUDE.md skeleton → in the framework (`method/06-bootstrap.md`).
- The actual bootstrap steps → in the framework (`method/06-bootstrap.md`).

This skill only exists to route Claude to the **framework doc** at the right moments. If the configured source is unreachable and no local clone is set in `~/.claude/atlas-source`, surface the problem — do not improvise.
