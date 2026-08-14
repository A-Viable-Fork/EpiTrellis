#!/usr/bin/env python3
"""Refuse to let real capture data enter the repository.

This is the check that cannot be added later. Git history is not deletable
in practice, so one real export used once as a convenient fixture is a
permanent leak of reading history and of share links that carry access.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORBIDDEN_NAMES = re.compile(
    r"^(journal|findings|report)-\d{8}[-_]\d{4}\.(ndjson|csv|txt|md)$|"
    r"^journal\.ndjson$|^bundle\.json$", re.I)

CAPABILITY_URL = re.compile(
    r"claude\.ai/share/[0-9a-f-]{8,}|"
    r"docs\.google\.com/[a-z]+/d/[A-Za-z0-9_-]{20,}|"
    r"reddit\.com/r/[^/\s]+/s/[A-Za-z0-9]{6,}|"
    r"[?&](is|si|token|auth|key)=[A-Za-z0-9_-]{10,}", re.I)

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}
fails = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    rel_dir = os.path.relpath(dirpath, ROOT)
    for name in filenames:
        rel = os.path.join(rel_dir, name).lstrip("./")
        path = os.path.join(dirpath, name)

        is_fixture = rel.startswith("fixtures/")

        if FORBIDDEN_NAMES.match(name) and not is_fixture:
            fails.append("%s: looks like a real capture export" % rel)
            continue

        if os.path.getsize(path) > 4_000_000:
            continue
        try:
            text = open(path, "r", errors="replace").read()
        except Exception:
            continue

        for m in CAPABILITY_URL.finditer(text):
            fails.append("%s: URL carrying an access capability (%s...)"
                         % (rel, m.group(0)[:40]))
            break

        if is_fixture and name.endswith((".ndjson", ".json")):
            if '"synthetic"' not in text and '"synthetic":true' not in text.replace(" ", ""):
                fails.append("%s: fixture lacks a synthetic marker" % rel)

if fails:
    print("PRIVACY CHECK FAILED\n")
    for f in fails:
        print("  " + f)
    print("\nFixtures are hand-built or generated, never harvested.")
    sys.exit(1)

print("privacy check passed")
