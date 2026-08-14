#!/usr/bin/env python3
"""Every function directory declares a license.

Fifteen of the twenty-two public repositories in the competition this project
came out of shipped with no license file, which under default copyright makes
them legally uncompoundable. A field organized around compounding produced
artifacts nobody may build on. This check exists so that does not happen here.

One of the fifteen declares MIT in its README and ships no LICENSE file, which
is why this check looks for the file and not for an intention."""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FN = os.path.join(ROOT, "functions")
missing = []

for name in sorted(os.listdir(FN)) if os.path.isdir(FN) else []:
    d = os.path.join(FN, name)
    if not os.path.isdir(d):
        continue
    if not os.path.isfile(os.path.join(d, "run")):
        missing.append("%s: no executable named run" % name); continue
    if not os.access(os.path.join(d, "run"), os.X_OK):
        missing.append("%s: run is not executable" % name)
    if not any(os.path.exists(os.path.join(d, c))
               for c in ("LICENSE", "LICENSE.txt", "LICENSE.md")):
        missing.append("%s: no LICENSE" % name)

if missing:
    print("LICENSE CHECK FAILED\n")
    for m in missing: print("  " + m)
    sys.exit(1)
print("license check passed")
