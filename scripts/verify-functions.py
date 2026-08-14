#!/usr/bin/env python3
"""Every function runs against the synthetic fixture without crashing.

A function that fails on an event it does not recognize is broken, because
the journal grows and functions do not update in lockstep.

Two tolerance cases, because the first one alone proved too weak. An
unrecognized event type is filtered out by the usual `event == "finding"`
guard before any field is read, so it never reaches the code that indexes
fields. The second case keeps a known event type and varies its fields, which
is what actually caught four functions indexing `kind` directly."""
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
    # tolerance check one: an unknown event type must not crash it
    res2 = loader.invoke(fn, events + [{"event": "unknown_future_type", "x": 1}], args)
    if not res2["ok"]:
        fails.append("%s: crashed on an unrecognized event type" % name)

    # tolerance check two: a known event type with fields removed and fields
    # added. The spec requires tolerating unknown fields as well as unknown
    # event types, and check one never exercises that.
    res3 = loader.invoke(fn, events + [
        {"event": "finding"},
        {"event": "finding", "kind": "stable_referent",
         "unknown_field": {"nested": [1, 2]}, "flags": []},
        {"event": "reference"},
        {"event": "capture", "later_addition": None},
    ], args)
    if not res3["ok"]:
        fails.append("%s: crashed on a known event type with fields removed "
                     "or added (%s)" % (name, res3.get("stderr", "").strip()[-120:]))

if fails:
    print("\nFUNCTION CHECK FAILED\n")
    for f in fails: print("  " + f)
    sys.exit(1)
print("\nfunction check passed")
