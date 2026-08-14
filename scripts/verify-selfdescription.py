#!/usr/bin/env python3
"""Documents about this repository, checked against this repository.

Findings about the world do not drift, because a measurement is finished.
Documents about the system drift, because the system is not. Four instances are
recorded in the compost ledger; three share one shape, which is a document
holding a copy of a fact whose authority lives elsewhere in the tree, after the
authority moved underneath it.

Two checks, both deliberately narrow.

**Paths, in both directions.** Every path-shaped token that names something in
this repository is tested for existence. Separately, a token appearing in a
sentence that also carries a negation or deferral word is tested for the
inverse, and fails when the path is present. CLAUDE.md failed in that second
direction for two commits, asserting that a script did not exist while listing
it as required, and a plain existence check cannot see that. It is also the
direction that survived longest.

Text preserved on purpose is exempt from the second direction only. The
departure record and the compost ledger keep superseded claims visible beside
their corrections, which is the discipline those documents exist for, so a
paragraph carrying or immediately followed by a supersession marker is skipped.

**Universal quantifiers near tables.** A document asserting `every` or `none`
while also containing a table is listed for a person to read. That is entry 9's
shape: a headline claiming every object produced a referent, four lines above
its own table recording two that did not. No machine here can tell a sound
universal from an unsound one, so this half prints a review queue and exits
zero. It advises. It does not block, and it is not evidence that anything was
checked.

This is not a manifest, not a templating system, and it substitutes no values
into prose. It reads what is written and asks whether the tree agrees.
"""
import glob as globmod
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIRS = ["docs", "trellises"]
SCAN_FILES = ["CLAUDE.md", "README.md"]

NEGATION = re.compile(
    r"does not exist|do not exist|doesn't exist|not yet|unbuilt|deferred|"
    r"is missing|are missing|absent|will fail|does not yet|no longer exists",
    re.I)

# Text kept visible on purpose, beside its correction.
SUPERSEDED = re.compile(
    r"supersed|corrected \d{4}-\d{2}-\d{2}|a retraction|retraction,|"
    r"answered in part|preserved here because|stays because it was published",
    re.I)

UNIVERSAL = re.compile(r"\b(every|all of|none of|no claim|no document|no function)\b", re.I)

# How close a negation must sit to a path before it counts as being about it.
NEAR = 40

# A token that looks like a repository path. Globs are allowed and resolved.
PATH_TOKEN = re.compile(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.*-]+)+/?|[A-Za-z0-9_-]+\.(?:py|md|ndjson|json|yml|txt|sh)")


def top_level_entries():
    return {e for e in os.listdir(ROOT) if not e.startswith(".git")} | {".github", ".gitignore"}


TOP = top_level_entries()


def is_ours(token):
    """Only tokens whose first segment names something at the top of this
    repository. Upstream paths quoted in findings, like a vendored project's
    own cases/ directory, are not ours to resolve and are skipped."""
    head = token.strip("`").split("/")[0]
    return head in TOP


def resolves(token):
    t = token.strip("`").rstrip("/")
    p = os.path.join(ROOT, t)
    if "*" in t:
        return bool(globmod.glob(p))
    return os.path.exists(p)


def targets():
    out = list(SCAN_FILES)
    for d in SCAN_DIRS:
        for dirpath, _, files in os.walk(os.path.join(ROOT, d)):
            for f in files:
                if f.endswith(".md"):
                    out.append(os.path.relpath(os.path.join(dirpath, f), ROOT))
    return sorted(set(out))


def strip_front_matter(text):
    """The typed header is not prose. Its Purpose sentence legitimately says
    things like 'what is deliberately deferred' in the same block as the
    Depends-on paths, which reads to a regex as calling those paths deferred."""
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return (" " * len(m.group(0))) + text[m.end():] if m else text


def declared_absent(text, match):
    """Does a negation sit close enough to this path to be about it?

    Shared by both directions. Near a present path it is a failure; near an
    absent one it is the document doing its job."""
    window = text[max(0, match.start() - NEAR):match.end() + NEAR]
    rel_start = match.start() - max(0, match.start() - NEAR)
    rel_end = rel_start + (match.end() - match.start())
    for n in NEGATION.finditer(window):
        if abs(n.start() - rel_end) <= NEAR or abs(rel_start - n.end()) <= NEAR:
            return True
    return False


def paragraphs(text):
    """Offsets kept, so a report can name a line rather than guess one."""
    out, pos = [], 0
    for part in re.split(r"(\n\s*\n)", text):
        if not re.fullmatch(r"\n\s*\n", part or ""):
            out.append((pos, part))
        pos += len(part or "")
    return out


def is_table(par):
    stripped = [ln for ln in par.strip().splitlines() if ln.strip()]
    return bool(stripped) and all(ln.lstrip().startswith("|") for ln in stripped)


def sentences(par):
    """Table rows are excluded from the negation direction. A cell reading
    'Built, specified, deferred, open' names a ledger's sections rather than the
    status of a path sitting in the next column, and all four recorded instances
    were prose or bullets rather than rows. That is a real limit of this check
    and not a claim that rows cannot drift."""
    body = "\n".join(ln for ln in par.splitlines() if not ln.lstrip().startswith("|"))
    return re.split(r"(?<=[.!?])\s+", body)


fails, review = [], []

for rel in targets():
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        continue
    raw = open(path, encoding="utf-8", errors="replace").read()
    text = strip_front_matter(raw)

    # direction one: named paths exist. The header is included here on purpose,
    # since verify-docs.py already checks Depends-on but not prose paths.
    #
    # A path the sentence itself declares absent is exempt here and handled by
    # the other direction. Running this against 9cfad09, where CLAUDE.md
    # correctly said verify-docs.py did not exist yet and it correctly did not,
    # this half failed on a true statement. A document is allowed to name what
    # is not built; that is what the deferral list is for.
    for m in PATH_TOKEN.finditer(raw):
        tok = m.group(0)
        if not is_ours(tok) or resolves(tok):
            continue
        if declared_absent(raw, m):
            continue
        line = raw[:m.start()].count("\n") + 1
        fails.append("%s:%d names %s which does not exist" % (rel, line, tok))

    pars = paragraphs(text)
    for i, (off, par) in enumerate(pars):
        line = text[:off].count("\n") + 1

        # direction two: a path called absent that is present
        lookahead = " ".join(p for _, p in pars[i:i + 3])
        if not SUPERSEDED.search(lookahead):
            for sent in sentences(par):
                negs = list(NEGATION.finditer(sent))
                if not negs:
                    continue
                for m in PATH_TOKEN.finditer(sent):
                    tok = m.group(0)
                    if not (is_ours(tok) and resolves(tok)):
                        continue
                    # The negation has to be about this path. A sentence can
                    # name a path and, thirty words later, call something else
                    # absent: the status ledger names a design document and then
                    # reports that it listed two producers as absent from a
                    # corpus. Requiring adjacency separates "X does not exist"
                    # from "X says Y is absent". A claim far from its path is
                    # missed, which is the cost of not crying wolf.
                    near = any(abs(n.start() - m.end()) <= NEAR
                               or abs(m.start() - n.end()) <= NEAR for n in negs)
                    if near:
                        fails.append("%s:%d calls %s absent or deferred, but it exists"
                                     % (rel, line, tok))

        # advisory: a universal quantifier in a document that also has a table
        if ("|---" in text or "| ---" in text) and not is_table(par):
            for sent in sentences(par):
                if UNIVERSAL.search(sent) and len(sent.strip()) > 30:
                    review.append("%s:%d  %s" % (rel, line, " ".join(sent.split())[:120]))

print("%d document(s) checked against the tree" % len(targets()))

if review:
    print("\nreview queue: universal quantifiers in documents that contain a table.")
    print("a person reads these. nothing here was verified by running this script.\n")
    seen = set()
    for r in review:
        if r in seen:
            continue
        seen.add(r)
        print("  " + r)

if fails:
    print("\nSELF-DESCRIPTION CHECK FAILED\n")
    for f in fails:
        print("  " + f)
    print("\nA document about this repository disagrees with this repository.")
    print("The tree is the authority. Update the document.")
    sys.exit(1)

print("\nself-description check passed")
