# Global rules

## Atlas projects

When the open project is an **Atlas** — a folder whose root has both `CLAUDE.md` and `STATUS.md`
(a symlink-aggregator of several independent repos) — orient before doing substantive work:

- **Read `CLAUDE.md` in full** (project orientation + standing decisions) and **`STATUS.md`**
  (current state & next steps) first. Don't start cold or make the user re-explain the project,
  its repos, or what it is.
- Skim any `SPEC_*.md` / `BACKLOG.md` at the root.
- The **Atlas method** (architecture, stores model, SPEC lifecycle, discipline, bootstrap recipe)
  is canonical at **https://atlas.paranoid.software**. Fetch it when needed via
  `bash ~/.gemini/atlas-fetch.sh llms.txt` (index) then the piece you need — or invoke the
  **`workspace-baseline`** skill. Do not improvise the method from memory.
- To **bootstrap** a new Atlas, or **reconcile** an existing one (add/remove repos, refresh
  `STATUS.md`), invoke the **`workspace-baseline`** skill — it fetches and follows the canonical
  recipe.

(Outside an Atlas, ignore this section.)
