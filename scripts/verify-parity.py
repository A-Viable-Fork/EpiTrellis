#!/usr/bin/env python3
"""Two implementations of two behaviours, checked against fixed answers.

`referent_key` and `capability_reason` each exist twice, in `probe/probe.py`
and in `functions/bundle/run`. That duplication is deliberate and is not to be
removed. A function is invoked as a subprocess and must be independently
readable; a shared import would couple every function to the instrument, which
is the coupling the subprocess boundary exists to prevent, and it is also what
lets a function carry its own license.

The cost of the duplication is that both failure modes are silent.

Divergent normalization produces hashes that look perfectly well formed and
simply do not join, and nothing anywhere raises. Divergent capability lists mean
the instrument and the export path disagree about what is safe to hand to
another person: the operator sees a warning in one place, no warning in the
other, and no reason to suspect either.

So the copies are pinned to fixtures rather than deduplicated. Four combinations
are checked, two implementations over two fixtures, and any disagreement names
the implementation and the input.

The fixtures pin PARITY, not correctness. Some expected values are wrong on
purpose and marked `"status": "defect"`: `mobile.de` normalizes to `de` because
the host prefix rule cannot tell a prefix from a name. Correcting that changes
every hash derived from such a host and breaks joins against journals already
written, so it is recorded here and decided elsewhere.
"""
import ast
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMPLS = [("probe", "probe/probe.py"), ("function", "functions/bundle/run")]


def load(rel):
    """Load an implementation without running it.

    Keeps imports, top-level assignments and definitions, and drops the rest.
    Structural rather than textual, so it survives the file being reordered and
    does not depend on a marker line. The function is a script that reads stdin
    at import time, which is why it cannot simply be imported."""
    path = os.path.join(ROOT, rel)
    tree = ast.parse(open(path, encoding="utf-8").read(), rel)
    keep = [n for n in tree.body if isinstance(
        n, (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef, ast.ClassDef))]
    ns = {"__name__": "parity_" + rel.replace("/", "_").replace(".", "_")}
    exec(compile(ast.Module(body=keep, type_ignores=[]), path, "exec"), ns)
    return ns


def assemble(case):
    """Capability addresses are stored as a shape with an {id} placeholder and
    assembled here. verify-privacy.py rejected the first version of that
    fixture, which spelled them out, and it was right to: a fabricated
    capability URL is indistinguishable from a real one to a reader and to a
    scanner. The shape says what is being tested; the literal never exists in
    the tree."""
    return case["shape"].replace("{id}", case.get("id", ""))


def fixture(name):
    with open(os.path.join(ROOT, "fixtures", "synthetic", name),
              encoding="utf-8") as f:
        return json.load(f)


fails = []
impls = {}
for label, rel in IMPLS:
    try:
        impls[label] = load(rel)
    except Exception as e:
        fails.append("%s: cannot load %s (%s)" % (label, rel, e))

norm = fixture("normalization.json")
caps = fixture("capability-urls.json")

if not fails:
    for label, ns in impls.items():
        fn = ns.get("referent_key")
        if not callable(fn):
            fails.append("%s: no referent_key" % label)
            continue
        for c in norm["cases"]:
            got = fn(c["in"])
            if got != c["key"]:
                fails.append(
                    "%s: referent_key(%r)\n      expected %s\n      got      %s"
                    % (label, c["in"], c["key"], got))

    for label, ns in impls.items():
        fn = ns.get("capability_reason")
        if not callable(fn):
            fails.append("%s: no capability_reason" % label)
            continue
        for c in caps["cases"]:
            url = assemble(c)
            got = bool(fn(url))
            if got != c["flag"]:
                fails.append(
                    "%s: capability_reason(%r) should %sflag and did %s"
                    % (label, url, "" if c["flag"] else "not ",
                       "" if got else "not"))

    # The fixtures cannot cover every input, so compare the shared data
    # directly as well. This catches a divergence on a shape nobody thought to
    # write down.
    if len(impls) == 2:
        a, b = impls["probe"], impls["function"]
        if a.get("NOISE_PARAMS") != b.get("NOISE_PARAMS"):
            only_p = sorted(set(a.get("NOISE_PARAMS", ())) - set(b.get("NOISE_PARAMS", ())))
            only_f = sorted(set(b.get("NOISE_PARAMS", ())) - set(a.get("NOISE_PARAMS", ())))
            fails.append("NOISE_PARAMS differ. only in probe: %s. only in "
                         "function: %s" % (only_p or "-", only_f or "-"))
        pa = [(r.pattern, w) for r, w in a.get("CAPABILITY_PATTERNS", [])]
        pb = [(r.pattern, w) for r, w in b.get("CAPABILITY_PATTERNS", [])]
        if pa != pb:
            fails.append("CAPABILITY_PATTERNS differ.\n      probe:    %s\n"
                         "      function: %s" % (pa, pb))

defects = sum(1 for c in norm["cases"] if c.get("status") == "defect")
print("%d normalization case(s) and %d capability case(s), against %d "
      "implementation(s)" % (len(norm["cases"]), len(caps["cases"]), len(impls)))
if defects:
    print("%d normalization case(s) pin a known defect rather than correct "
          "behaviour" % defects)

if fails:
    print("\nPARITY CHECK FAILED\n")
    for f in fails:
        print("  " + f)
    print("\nThese behaviours are duplicated on purpose and the fixture is what")
    print("keeps the copies honest. Do not resolve this by extracting a shared")
    print("module: fix the copy that drifted, or change the fixture if the")
    print("behaviour was meant to change, and change both copies together.")
    sys.exit(1)

print("parity check passed")
