#!/usr/bin/env python3
"""Every document carries a well-formed typed header, and the dependency
graph agrees with itself in both directions.

The common failure is a document that quietly acquires dependents and stops
being safe to revise. Checking Depends-on against Depended-on-by catches it
mechanically rather than by anyone remembering.

Both directions are checked. Depends-on must be matched by the target's
Depended-on-by, and Depended-on-by must be matched by the target's Depends-on,
because a document that claims dependents nobody claims back is the same
unverified assertion pointing the other way.

A document with no typed header fails rather than warning. The style guide
says a wrong header fails the build, and omitting the header entirely was the
cheap way around that."""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN = ["docs", "trellises", "spec"]
EXTRA = ["README.md", "CLAUDE.md"]
TYPES = {"specification", "reference", "finding", "design"}
FIELDS = ["Type", "Purpose", "Depends on", "Depended on by"]

def parse(path):
    text = open(path, errors="replace").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    head, body = {}, m.group(1)
    for field in FIELDS:
        fm = re.search(r"^%s:\s*(.*)$" % re.escape(field), body, re.M)
        if fm:
            head[field] = fm.group(1).strip()
    for k in ("Depends on", "Depended on by"):
        v = head.get(k, "[]").strip()
        head[k] = [x.strip() for x in v.strip("[]").split(",") if x.strip()]
    return head

docs, fails = {}, []

targets = list(EXTRA)
for d in SCAN:
    p = os.path.join(ROOT, d)
    for dirpath, _, files in os.walk(p):
        for f in files:
            if f.endswith(".md"):
                targets.append(os.path.relpath(os.path.join(dirpath, f), ROOT))

for rel in sorted(set(targets)):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        continue
    head = parse(path)
    if head is None:
        fails.append("%s: no typed header" % rel)
        continue
    missing = [f for f in FIELDS if f not in head]
    if missing:
        fails.append("%s: header missing %s" % (rel, ", ".join(missing)))
        continue
    if head["Type"] not in TYPES:
        fails.append("%s: Type '%s' is not one of %s" % (rel, head["Type"], sorted(TYPES)))
    docs[rel] = head

for rel, head in docs.items():
    for dep in head["Depends on"]:
        if not os.path.exists(os.path.join(ROOT, dep)):
            fails.append("%s: depends on %s which does not exist" % (rel, dep))
        elif dep in docs and rel not in docs[dep]["Depended on by"]:
            fails.append("%s depends on %s, but %s does not list it under "
                         "'Depended on by'" % (rel, dep, dep))
    for dep in head["Depended on by"]:
        if not os.path.exists(os.path.join(ROOT, dep)):
            fails.append("%s: depended on by %s which does not exist" % (rel, dep))
        elif dep in docs and rel not in docs[dep]["Depends on"]:
            fails.append("%s claims %s as a dependent, but %s does not list it "
                         "under 'Depends on'" % (rel, dep, dep))

print("%d document(s) with typed headers" % len(docs))
if fails:
    print("\nDOC CHECK FAILED\n")
    for f in fails: print("  " + f)
    sys.exit(1)
print("doc check passed")
print("\nnot yet checked: figures cited in prose against the journal.")
print("that needs a findings pipeline. documents can still drift.")
