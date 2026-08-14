---
Type: reference
Purpose: "What is built, what is specified and unbuilt, and what is deliberately deferred, so a reader can tell claims about the system from claims about the plan."
Depends on: [docs/document-style-guide.md, docs/findings/probe-referent-stability.md]
Depended on by: [README.md, docs/departure-from-epistack.md]
---

# Status Ledger

## In one read

A measuring instrument runs on a phone with no app and no store. A loader runs
four functions discovered by presence and identified by hash. Four checks pass
and two of them caught real problems on their first run. Everything else is
specified, deferred, or open.

## How to read this ledger

**Built** means it runs and a check proves it.
**Specified** means it is written down and does not run.
**Deferred** means it is deliberately not being built yet, with a reason.
**Open** means nobody has an answer.

A claim not appearing here is not a claim about this system.

## Built

| Thing | Check |
|---|---|
| Referent normalization and object hashing | `functions/bundle`, two-party join demonstrated |
| Capture via share sheet, no producer cooperation | `probe/probe.py`, 13 objects |
| Archive fallback with consent and capability-URL warning | `probe/probe.py` |
| Function loader: discovery, hashing, subprocess invocation | `scripts/verify-functions.py` |
| Four functions: report, recent, bundle, join | `scripts/verify-functions.py` |
| Privacy gate on real capture data | `scripts/verify-privacy.py` |
| License presence per function | `scripts/verify-license.py` |
| Unknown-event tolerance | `scripts/verify-functions.py` |
| Typed header on every document | `scripts/verify-docs.py` |
| Dependency reciprocity, Depends-on to Depended-on-by | `scripts/verify-docs.py` |

## Specified, not built

| Thing | Where |
|---|---|
| Function manifest and type signatures | `spec/function.md`, deliberately deferred |
| Vocabulary bundles and translators | design only |
| Capability precondition graph | parent trellis S-10 |
| Capture dependency closure over providers | child B, B-1. Algorithm exists in EpiStack |
| Learning-residue instrument | child B, B-2 |
| Client-independent state interchange | child A, A-3 |
| Release continuity after maintainer loss | child A, A-5 |

## Deferred, with reason

**Function distribution and registries.** Local loading only. What a function
must declare about itself will be learned from the functions people write.

**`verify-docs.py` number checking.** Header and dependency checking is
achievable now. Checking that cited figures match the journal needs a findings
pipeline that does not exist. Documents can still drift, and one currently has.

**The self-governance tier.** An operator's policy over their own device.
Probably a sixth tier in the decomposition, unrecorded.

## Open

Game-integrity residue is unpublishable in principle, so opening the learning
loop works for boundary functions and fails where concentration occurred.

Fork-choice coordination survives every resource being portable.

Whether n=1 value is enough to hold anyone. This is the most likely cause of
death and no architecture substitutes for it.

Whether the object population that resists capture is large. The probe measured
objects that were shareable, which selects on the property being tested.
