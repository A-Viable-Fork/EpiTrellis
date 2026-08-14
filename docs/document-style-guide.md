---
Type: specification
Purpose: "Defines the typed header every document carries, the four document types, and the two checks that keep the dependency graph honest."
Depends on: []
Depended on by: [docs/status-ledger.md, docs/compost-ledger.md, docs/departure-from-epistack.md, docs/corpus-index.md, CLAUDE.md, docs/design/workflow-spec-v0.1.md, trellises/parent-decomposition-v1.5.md, trellises/child-receiver-substrate-v0.1.md, trellises/child-capture-dynamics-v0.1.md, trellises/phone-v1.md]
---

# Document Style Guide

Every document under `docs/`, `trellises/` and `spec/`, along with `README.md`
and `CLAUDE.md`, carries a typed header. The header is not decoration:
`scripts/verify-docs.py` reads it, and a document whose header is wrong or
missing fails the build.

## The required header

```
---
Type: specification | reference | finding | design
Purpose: "One sentence. What this document is for, not what it contains."
Depends on: [paths]
Depended on by: [paths]
---
```

## The four types

**specification** defines a mechanism others cite. It is the source of truth for
what it defines, and a claim about that mechanism made elsewhere is wrong if it
disagrees.

**reference** records something for audit rather than defining it: ledgers,
indexes, the departure record.

**finding** reports what an instrument established, with a date and an n. A
finding may kill a design. A design may not suppress a finding.

**design** proposes. A design document carries no authority over a finding and
is expected to be overturned.

## The two dependency chains

`Depends on` is what this document would be wrong without. `Depended on by` is
what would be wrong if this document changed.

They are maintained separately and checked against each other, because the
common failure is a document that quietly acquires dependents and stops being
safe to revise.

## What verify-docs.py enforces

1. Every document in scope has a well-formed header with all four fields. A
   document with no header at all fails, rather than passing quietly, because
   omitting the header was otherwise the cheapest way around the first rule.
2. Every path in `Depends on` exists and reciprocally lists this document under
   `Depended on by`, and every path in `Depended on by` exists and reciprocally
   lists this document under `Depends on`. Both directions, because a document
   claiming dependents that do not claim it back is the same unchecked assertion
   pointing the other way.

## The discipline for new documents

State the purpose before writing the body. If the purpose sentence needs an
"and", the document is two documents.

Prose over bullets. No em dashes. Say what something is rather than what it is
not. When something is dead, say it is dead.
