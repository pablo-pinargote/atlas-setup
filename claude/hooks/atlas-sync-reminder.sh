#!/usr/bin/env bash
# Stop hook: when working inside an Atlas whose STATUS.md has gone stale, nudge the
# AGENT (via additionalContext) to OFFER a /atlas-sync checkpoint to the user.
# Gentle by design: only inside an Atlas, only when STATUS.md is >15min old, at most
# once per 30min per Atlas, never while already inside a Stop hook. The agent still
# applies judgment — it only offers a sync if real progress/decisions actually changed.

input=$(cat)

# Anti-loop guard.
[ "$(jq -r '.stop_hook_active // false' <<<"$input" 2>/dev/null)" = "true" ] && exit 0

cwd=$(jq -r '.cwd // empty' <<<"$input" 2>/dev/null)
[ -z "$cwd" ] && exit 0

# Find the Atlas root: nearest dir at/above cwd containing STATUS.md.
dir="$cwd"; atlas=""
while [ -n "$dir" ] && [ "$dir" != "/" ]; do
  [ -f "$dir/STATUS.md" ] && { atlas="$dir"; break; }
  dir=$(dirname "$dir")
done
[ -z "$atlas" ] && exit 0   # not inside an Atlas → silent

status="$atlas/STATUS.md"
now=$(date +%s)
mtime=$(stat -f %m "$status" 2>/dev/null || stat -c %Y "$status" 2>/dev/null || echo "$now")
[ $(( now - mtime )) -lt 900 ] && exit 0   # STATUS.md fresh (<15min) → no nudge

# Throttle: at most one reminder per 30min per Atlas. State in a cache dir, not the Atlas.
cache="${TMPDIR:-/tmp}/atlas-sync-reminders"; mkdir -p "$cache" 2>/dev/null
key=$(printf '%s' "$atlas" | shasum 2>/dev/null | cut -d' ' -f1)
marker="$cache/${key:-default}"
if [ -f "$marker" ]; then
  last=$(cat "$marker" 2>/dev/null || echo 0)
  [ $(( now - last )) -lt 1800 ] && exit 0
fi
printf '%s' "$now" > "$marker"

msg="[atlas-sync] This Atlas's STATUS.md hasn't been updated in a while. If meaningful progress, decisions, or next steps changed this session, offer the user a quick /atlas-sync checkpoint — do not run it unprompted."
jq -n --arg ctx "$msg" '{hookSpecificOutput:{hookEventName:"Stop",additionalContext:$ctx}}'
exit 0
