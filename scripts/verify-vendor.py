#!/usr/bin/env python3
"""Vendored foreign code still has the bytes it was vendored with.

The composition claim rests entirely on the vendored method being unmodified.
A reformat, a lint pass, or a well-meant fix to an awkward import would leave
the claim standing in the documents while making it false in the tree, and
nothing else here would notice.

This is a fixed list of hashes for the directories we have actually vendored.
It is deliberately not a manifest format and not a registry: there is no schema,
nothing declares itself, and adding a second vendored method means adding lines
to the dict below. If that ever becomes unwieldy, the answer is still not a
manifest, it is fewer vendored copies."""
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# path relative to ROOT -> sha256 of the bytes as vendored
VENDORED = {
    # kyaloeric/epistemic-stack @ 89d6632abd0b7678b738b722547d17b984fe1014, MIT.
    # See functions/concentration/ATTRIBUTION.md.
    "functions/concentration/vendor/src/concentration.py":
        "3848b8af2c77675ed6a9ba6fac9f66f47f01a6dc7dc3515cc0fe687efca1c077",
    "functions/concentration/vendor/src/warrant.py":
        "c2160f3e62649336ef8b0d4ac10d18141fc7d0dbcd82926b7e9ffa461cfa1e98",
    "functions/concentration/vendor/src/__init__.py":
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


fails = []
for rel, expected in sorted(VENDORED.items()):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        fails.append("%s: vendored file is missing" % rel)
        continue
    actual = sha256_file(path)
    if actual != expected:
        fails.append("%s: bytes changed\n      expected %s\n      found    %s"
                     % (rel, expected, actual))

# A vendored directory without its attribution is a licensing problem as much as
# a provenance one, since the upstream copyright line lives there.
for rel in sorted(VENDORED):
    d = rel.split("/vendor/")[0]
    for required in ("ATTRIBUTION.md", "LICENSE"):
        p = os.path.join(ROOT, d, required)
        if not os.path.exists(p):
            fails.append("%s: vendored code with no %s" % (d, required))

print("%d vendored file(s) checked" % len(VENDORED))
if fails:
    print("\nVENDOR CHECK FAILED\n")
    for f in fails:
        print("  " + f)
    print("\nVendored bytes are the composition claim. If a change was")
    print("deliberate, it is a different method and belongs to a new commit")
    print("hash in ATTRIBUTION.md, not to an updated expectation here.")
    sys.exit(1)
print("vendor check passed")
