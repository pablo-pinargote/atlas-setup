#!/bin/sh
# atlas-fetch (Antigravity) — read one file of the Atlas framework from the configured source.
#
# The source is a SINGLE, mutually-exclusive value in ~/.gemini/atlas-source:
#   - a URL          (http:// or https://)  -> fetched with curl
#                       (https://atlas.paranoid.software — the official site)
#   - a local path   (anything else)        -> read from the cloned repo with cat
#
# Usage:  atlas-fetch.sh <relative/path>
#   e.g.  atlas-fetch.sh llms.txt
#         atlas-fetch.sh method/06-bootstrap.md
src=$(head -1 "$HOME/.gemini/atlas-source" 2>/dev/null | tr -d '[:space:]')
[ -n "$src" ] || { echo "atlas-fetch: configure ~/.gemini/atlas-source (a URL or a repo path)" >&2; exit 1; }
[ -n "${1:-}" ] || { echo "atlas-fetch: usage: atlas-fetch.sh <relative/path>" >&2; exit 2; }
case "$src" in
  http://*|https://*) exec curl -fsS --max-time 5 "$src/$1" ;;
  *)                  exec cat "$src/$1" ;;
esac
