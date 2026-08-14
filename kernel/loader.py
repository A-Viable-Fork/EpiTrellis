#!/usr/bin/env python3
"""
Epitrellis loader.

License: Apache-2.0

Discovers functions by presence, identifies them by the hash of their file,
and runs them as subprocesses over stdin and stdout.

It imposes no manifest, no language, no vocabulary. What a function declares
about itself is a separate forkable concern; what it does is between it and
whoever ran it.
"""

import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FUNCTIONS = [
    os.path.join(ROOT, "functions"),
    os.path.expanduser("~/.epitrellis/functions"),
]
JOURNAL = os.path.expanduser("~/trellis-probe/journal.ndjson")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def discover():
    """A directory containing an executable named `run` is a function.
    Presence is registration. There is no index to corrupt and no
    gatekeeper to petition."""
    found = {}
    for base in FUNCTIONS:
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            run = os.path.join(base, name, "run")
            if not os.path.isfile(run) or not os.access(run, os.X_OK):
                continue
            lic = None
            for cand in ("LICENSE", "LICENSE.txt", "LICENSE.md"):
                p = os.path.join(base, name, cand)
                if os.path.exists(p):
                    lic = open(p).readline().strip()[:60]
                    break
            found[name] = {
                "name": name,
                "path": run,
                "dir": os.path.join(base, name),
                "hash": sha256_file(run),
                "license": lic,
                "source": base,
            }
    return found


def read_journal(path=None):
    p = path or JOURNAL
    if not os.path.exists(p):
        return []
    out = []
    for line in open(p):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def invoke(fn, events, args=None, timeout=120):
    """Run a function. Its stdout is returned as parsed lines where they
    parse and raw strings where they do not, because a function is entitled
    to print to a human as well as to a machine."""
    payload = "".join(json.dumps(e) + "\n" for e in events)
    try:
        proc = subprocess.run(
            [fn["path"]] + list(args or []),
            input=payload.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout", "lines": [], "text": []}

    lines, text = [], []
    for raw in proc.stdout.decode("utf-8", "replace").splitlines():
        if not raw.strip():
            continue
        try:
            lines.append(json.loads(raw))
        except Exception:
            text.append(raw)

    return {
        "ok": proc.returncode == 0,
        "code": proc.returncode,
        "lines": lines,
        "text": text,
        "stderr": proc.stderr.decode("utf-8", "replace")[:2000],
    }


def main():
    fns = discover()

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("epitrellis loader\n")
        print("  loader.py list")
        print("  loader.py run <name> [args...]")
        print("  loader.py hash <name>\n")
        print("%d function(s) available:" % len(fns))
        for f in fns.values():
            print("  %-12s %s  %s" % (f["name"], f["hash"][:12],
                                      f["license"] or "NO LICENSE"))
        return 0

    cmd = sys.argv[1]

    if cmd == "list":
        for f in fns.values():
            print(json.dumps({"name": f["name"], "hash": f["hash"],
                              "license": f["license"], "source": f["source"]}))
        return 0

    if cmd == "hash":
        if len(sys.argv) < 3 or sys.argv[2] not in fns:
            print("unknown function", file=sys.stderr)
            return 2
        print(fns[sys.argv[2]]["hash"])
        return 0

    if cmd == "run":
        if len(sys.argv) < 3:
            print("usage: loader.py run <name> [args...]", file=sys.stderr)
            return 2
        name = sys.argv[2]
        if name not in fns:
            print("unknown function: %s" % name, file=sys.stderr)
            print("available: %s" % ", ".join(fns), file=sys.stderr)
            return 2

        events = read_journal()
        res = invoke(fns[name], events, sys.argv[3:])

        for t in res["text"]:
            print(t)
        for l in res["lines"]:
            print(json.dumps(l))
        if not res["ok"]:
            sys.stderr.write(res.get("stderr", ""))
            return res.get("code", 1)
        return 0

    print("unknown command: %s" % cmd, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
