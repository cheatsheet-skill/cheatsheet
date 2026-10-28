#!/usr/bin/env python3
"""Copy the student's starting material to a pristine snapshot before editing.

Usage:
    python snapshot.py SRC DEST

SRC can be a file or a folder. DEST must not exist yet (or be an empty folder)
and should live OUTSIDE the project, e.g. a scratch/temp directory, so the
snapshot never ends up in the submission.

Skips version-control and dependency/cache folders (.git, node_modules,
__pycache__, .venv, venv, build caches) to keep the snapshot small; the diff
review ignores them too.
"""
import argparse
import os
import shutil
import sys

SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv",
             ".mypy_cache", ".pytest_cache", ".idea", ".vscode", ".DS_Store"}


def ignore(_dir, names):
    return [n for n in names if n in SKIP_DIRS]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dest")
    a = ap.parse_args()

    src = os.path.abspath(a.src)
    dest = os.path.abspath(a.dest)
    if not os.path.exists(src):
        sys.exit(f"Source not found: {src}")
    if os.path.isdir(src) and (dest == src or dest.startswith(src + os.sep)):
        sys.exit("DEST is inside SRC. Put the snapshot outside the project folder.")
    if os.path.isfile(dest) or (os.path.isdir(dest) and os.listdir(dest)):
        sys.exit(f"DEST already exists and is not empty: {dest}")

    if os.path.isdir(src):
        if os.path.isdir(dest):
            os.rmdir(dest)
        shutil.copytree(src, dest, ignore=ignore, symlinks=True)
        count = sum(len(f) for _, _, f in os.walk(dest))
        print(f"Snapshot of folder saved: {dest} ({count} files)")
    else:
        os.makedirs(dest, exist_ok=True)
        target = os.path.join(dest, os.path.basename(src))
        shutil.copy2(src, target)
        print(f"Snapshot of file saved: {target}")
        print("Compare later with: review_changes.py", target, src)


if __name__ == "__main__":
    main()
