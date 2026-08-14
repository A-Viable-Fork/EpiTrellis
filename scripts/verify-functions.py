#!/usr/bin/env python3
"""Every function runs against the synthetic fixture without crashing.

A function that fails on an event it does not recognize is broken, because
the journal grows and functions do not update in lockstep."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kernel"))
import loader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = os.path.join(ROOT, "fixtures", "synthetic", "journal.ndjson")
events = loader.read_journal(FIX)
fns = loader.discover()
if not fns:
    print("no functions discovered"); sys.exit(1)

fails = []
for name, fn in fns.items():
    args = ["/tmp/epitrellis-verify-bundle.json"] if name == "join" else []
    if name == "join":
        b = loader.invoke(fns["bundle"], events)
        open(args[0], "w").write(b["lines"][0] and json.dumps(b["lines"][0]) or "{}")
    res = loader.invoke(fn, events, args)
    status = "ok" if res["ok"] else "FAILED"
    print("  %-12s %s  %s  (%d lines, %d text)"
          % (name, fn["hash"][:12], status, len(res["lines"]), len(res["text"])))
    if not res["ok"]:
        fails.append("%s: exit %s %s" % (name, res.get("code"), res.get("stderr", "")[:200]))
    # tolerance check: unknown event type must not crash it
    res2 = loader.invoke(fn, events + [{"event": "unknown_future_type", "x": 1}], args)
    if not res2["ok"]:
        fails.append("%s: crashed on an unrecognized event type" % name)

if fails:
    print("\nFUNCTION CHECK FAILED\n")
    for f in fails: print("  " + f)
    sys.exit(1)
print("\nfunction check passed")
