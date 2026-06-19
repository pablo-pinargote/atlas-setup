#!/usr/bin/env python3
"""
Reads .code-workspace files and generates folders with symlinks
so that tools without workspace support (Claude Code, Codex, VS Code)
can open a single folder and see the same repos that Cursor sees.

Usage:
    .venv/bin/python gen_workspaces.py                                    # generate all
    .venv/bin/python gen_workspaces.py rocket/oss.code-workspace          # specific workspace
    .venv/bin/python gen_workspaces.py rocket/oss.code-workspace --dry-run
"""

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path


def strip_trailing_commas(text: str) -> str:
    """Remove trailing commas before } or ] (VS Code allows them, stdlib json doesn't)."""
    return re.sub(r",\s*([}\]])", r"\1", text)


def parse_workspace(path: Path) -> list[str]:
    """Parse a .code-workspace file and return the list of folder paths."""
    raw = path.read_text()
    data = json.loads(strip_trailing_commas(raw))
    return [f["path"] for f in data.get("folders", [])]


def resolve_names(paths: list[str]) -> dict[str, str]:
    """
    Map each path to a symlink name.
    If two paths share the same basename, disambiguate by prepending the parent folder
    with -- as separator.
    Returns: { symlink_name: original_path }
    """
    basenames = [Path(p).name for p in paths]
    counts = Counter(basenames)

    result = {}
    for p in paths:
        pp = Path(p)
        name = pp.name
        if counts[name] > 1:
            name = f"{pp.parent.name}--{name}"
        result[name] = p

    return result


def clean_symlinks(folder: Path, dry_run: bool) -> list[str]:
    """Remove only symlinks inside folder. Returns list of removed names."""
    removed = []
    if not folder.exists():
        return removed
    for entry in folder.iterdir():
        if entry.is_symlink():
            removed.append(entry.name)
            if not dry_run:
                entry.unlink()
    return removed


def process_workspace(ws_file: Path, dry_run: bool) -> None:
    """Process a single .code-workspace file."""
    concept_dir = ws_file.parent
    ws_name = ws_file.stem  # e.g. "oss" from "oss.code-workspace"
    target_dir = concept_dir / f"_{ws_name}"

    print(f"\n{'[DRY RUN] ' if dry_run else ''}{ws_file.relative_to(ws_file.parent.parent)}")

    # Parse workspace
    try:
        paths = parse_workspace(ws_file)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"  ERROR: failed to parse: {e}")
        return

    if not paths:
        print("  SKIP: no folders defined")
        return

    # Create target dir
    if not target_dir.exists():
        print(f"  mkdir {target_dir.name}/")
        if not dry_run:
            target_dir.mkdir()

    # Clean existing symlinks only
    removed = clean_symlinks(target_dir, dry_run)
    if removed:
        print(f"  cleaned {len(removed)} symlink(s): {', '.join(removed)}")

    # Resolve names and create symlinks
    name_map = resolve_names(paths)
    for link_name, target_path in name_map.items():
        link_path = target_dir / link_name
        target = Path(target_path)

        if not target.exists():
            print(f"  WARN: target does not exist: {target_path}")

        if link_path.exists() and not link_path.is_symlink():
            print(f"  SKIP: {link_name} is a real file/folder, not overwriting")
            continue

        print(f"  {link_name} -> {target_path}")
        if not dry_run:
            link_path.symlink_to(target_path)


def main():
    parser = argparse.ArgumentParser(description="Generate workspace folders with symlinks")
    parser.add_argument("files", nargs="*", help="Specific .code-workspace file(s) to process. If omitted, processes all.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without making changes")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()

    if args.files:
        ws_files = []
        for f in args.files:
            p = Path(f)
            if not p.is_absolute():
                p = script_dir / p
            p = p.resolve()
            if not p.exists():
                print(f"ERROR: {f} not found")
                return
            if p.suffix != ".code-workspace":
                print(f"ERROR: {f} is not a .code-workspace file")
                return
            ws_files.append(p)
    else:
        ws_files = sorted(script_dir.glob("*/*.code-workspace"))

    if not ws_files:
        print("No .code-workspace files found.")
        return

    print(f"Found {len(ws_files)} workspace(s)")
    if args.dry_run:
        print("DRY RUN — no changes will be made\n")

    for ws_file in ws_files:
        process_workspace(ws_file, args.dry_run)

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Done.")


if __name__ == "__main__":
    main()
