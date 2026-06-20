---
name: workspace-baseline
description: Use when bootstrapping a new Atlas (symlink-aggregator project root), editing CLAUDE.md / STATUS.md / BACKLOG.md / DEVIATIONS.md / SPEC_*.md / DRAFT_*.md / _archived/, deciding where a piece of knowledge belongs across the stores, or auditing the Atlas setup. The canonical Atlas framework (architecture + bootstrap recipe) lives in the Atlas framework doc, fetched via `~/.gemini/atlas-fetch.sh`. This skill is the entry point — fetch the framework, then act.
---

# workspace-baseline

The canonical Atlas framework (architecture + bootstrap recipe) lives in the **Atlas framework doc**, fetched via `~/.gemini/atlas-fetch.sh` from the source in `~/.gemini/atlas-source` (the official site `https://atlas.paranoid.software`, or a local clone). This skill is the entry point: fetch the framework, then act.

> **Memory store & deviations are not wired up here yet.** The framework describes a *required* cross-tool memory store and an optional candidates-promotion flow; configuring one is a later step. For now, universal-rule promotion and the `DEVIATIONS` workflow are deferred.

## Step 1 — load the framework definition

```
bash ~/.gemini/atlas-fetch.sh llms.txt          # the index — start here
bash ~/.gemini/atlas-fetch.sh llms-full.txt     # the whole framework in one file
bash ~/.gemini/atlas-fetch.sh method/06-bootstrap.md   # a specific piece
```

`atlas-fetch.sh` resolves the single source in `~/.gemini/atlas-source`: a URL → `curl`, a local path → `cat`. If it fails, the source is unreachable / misconfigured — surface that, don't improvise the framework from memory.

Returns the Atlas framework:

- **The Atlas model** (`method/01-the-atlas.md`) — an **Atlas** is a symlink-aggregator project root; why it exists.
- **The stores model** (`method/02-stores-model.md`) — where each kind of knowledge lives; the decision tree.
- **Atlas anatomy** (`method/03-atlas-anatomy.md`) — the root files of record (incl. `STATUS.md`), naming, the per-repo orientation block.
- **The SPEC lifecycle** (`method/04-spec-lifecycle.md`) — READY → IN PROGRESS → IN REVIEW → SHIPPED → archived.
- **The discipline** (`method/05-discipline.md`) — small deliverable specs; review before shipped; clean baseline; commit-message hygiene.
- **The bootstrap recipe + Atlas `CLAUDE.md` template** (`method/06-bootstrap.md`).
- **Optional git-versioning** (`method/07-optional-git-versioning.md`).

## Step 2 — apply per the framework

- **Bootstrapping a new Atlas** → follow the recipe (`method/06-bootstrap.md`): discover symlinks, create `CLAUDE.md` (per-repo orientation blocks), `STATUS.md`, `BACKLOG.md`, `DEVIATIONS.md`, `_archived/`. Pre-flight: stop if a baseline already exists or there are no symlinks.
- **Reconciling an existing Atlas** (`/atlas-sync` equivalent) → regenerate `STATUS.md`, and when the repo set changed, add/remove per-repo orientation blocks (sync owns the repo set; init does not).
- **Modifying any Atlas root file of record** → consult the stores model / anatomy (`method/02`, `method/03`) for what goes in each.
- **Deciding where a piece of knowledge belongs** → use the decision tree in the stores model (`method/02-stores-model.md`).

## What is NOT in this skill

- The actual architecture text / recipe / template → in the Atlas framework doc (`atlas-fetch.sh`). This skill only routes to it. If the configured source is unreachable and no local clone is set in `~/.gemini/atlas-source`, surface the problem — do not improvise.
