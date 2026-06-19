#!/usr/bin/env bash
# SessionStart hook: orient the agent to the current workspace/project so a new
# session never starts cold. Generic — gated on a CLAUDE.md or STATUS.md in cwd,
# and injects STATUS.md (the living "current state") directly when present.
[ -f CLAUDE.md ] || [ -f STATUS.md ] || exit 0

ctx="SESSION START — Orient before doing substantive work: read CLAUDE.md in full; skim any SPEC_*.md / BACKLOG.md at the workspace root; and consult the Atlas framework for the method/conventions (run \`bash ~/.claude/atlas-fetch.sh llms.txt\` for the index, then fetch the piece you need). Do NOT start from zero or make the user re-explain the workspace, repos, or what the project is."

if [ -f STATUS.md ]; then
    ctx="$ctx"$'\n\n'"=== STATUS.md — current state & next steps (read this first) ==="$'\n'"$(cat STATUS.md)"
fi

jq -n --arg ctx "$ctx" \
  '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$ctx}}'
