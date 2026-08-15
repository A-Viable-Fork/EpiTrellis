---
Type: finding
Purpose: "That a verdict describes one encounter with an object rather than the object itself, established from a single object encountered four times, and what that costs a join between two parties."
Depends on: [docs/findings/probe-referent-stability.md]
Depended on by: [docs/corpus-index.md]
---

# Finding: A Verdict Is A Property Of An Encounter

**Instrument.** `probe/probe.py`, share-sheet capture on Android under Termux,
read back through `probe.py bundle`.
**n.** 1 object, 4 sightings, 2 verdicts. One device, one operator, one morning.
**Dates.** Encounters 2026-08-13. Observed in the bundle 2026-08-14.
**Operator.** One person.

No address from the corpus appears in this document. The journal is the
operator's reading history, and several of its URLs carry access rather than
merely address, so the object below is described by shape.

## Result

One object, a post on a single host, was encountered four times in one morning
by one instrument. Those four encounters produced two verdicts:
`stable_referent` and `producer_refused`.

Same referent, same normalization, same code, same device, hours apart. The two
verdicts disagree about something with only one answer per encounter, which is
whether the payload was obtained.

**A verdict describes an encounter. The instrument exports verdicts as though
they described objects.** The bundle's `kinds` array is a set, presented without
order, without time, and without any signal that two of its members contradict
each other. Fifteen other objects in the same bundle carried exactly one verdict
each, which is why the shape had gone unnoticed: an object seen once produces a
verdict list that looks like a property of the object, and is indistinguishable
from one.

## What this does not establish

**Why the encounters differed.** The journal does not record enough to say.
Producer behaviour, network conditions, and instrument state are all consistent
with what was written, and nothing distinguishes them. Naming a cause here would
be speculation, and the honest position is that four encounters disagreed and
the record cannot say why.

There is a temptation to reach for one. `docs/findings/probe-referent-stability.md`
records a retraction about the same host in the same corpus, where a refusal was
traced to the instrument sending a bare user-agent string and disappeared under
browser-shaped headers. That is a documented instrument-side cause for a refusal
of this host on this day. It is not evidence about *these* encounters: the
journal does not record which sighting used which headers, so whether the
retracted refusal is one of these four cannot be established from the record.
The plausible story and the supported one are different things here, and only
the second belongs in a finding.

**That this is common.** One object. The other fifteen in the same bundle were
each seen once, so this corpus contains exactly one opportunity for the effect
to appear, and it appeared. That is not a rate.

**That the verdicts are wrong.** Both may be correct reports of what happened at
the time each was taken. That is the point: correct per encounter, and
incoherent when collapsed onto an object.

## The consequence for join

This is the part that matters beyond one device.

Two parties intersecting bundles compare verdict sets. Each set may be
internally inconsistent, and neither party can see it in the other's bundle. The
receiving party sees a list of verdicts attached to a hash, with no way to know
that the list disagrees with itself, no way to ask when any member was reached,
and no way to tell an object seen once from an object seen four times with
conflicting results. `seen` gives the count and nothing else.

The join still works, because the join is set intersection over hashes and the
hashes are unaffected. What degrades is what a matched object *means* once
matched. A verdict set is being treated as a description of the object by
whoever receives it, and it is not one.

This is recorded as a limitation of the current join rather than as a thing to
fix. Attaching time to bundle objects would change the bundle from a minimal
join artifact into a log, and the cost of that is the argument the bundle exists
to make: what travels is small, so multi-homing stays free. Nothing here is
worth paying that with yet.

What was added instead is visibility. `bundle` now counts objects carrying more
than one verdict, and separately counts those carrying `stable_referent`
together with `producer_refused`, reporting both in the printed output and in
`bundle.json` under `verdicts`. The narrow pair is deliberate: those two
disagree about whether the payload was obtained. Everything else is left
uncounted, because multiplicity is not contradiction and no general
compatibility rule over the verdict vocabulary is defensible from one object.

## Recorded, not acted on

Two producers that the referent finding lists as having produced no referent,
Facebook and NYT, now appear in the bundle carrying derived referent hashes and
`producer_refused` verdicts. That is exactly the shape the discard fix was meant
to produce.

It was reached by read-time derivation over rows written before the fix, not by
the fixed capture path running. **The live capture path has not been tested.**
The code that keeps a referent when a fetch fails has been exercised only
against a stub. An operator re-run is now confirmation of something already
visible in the derivation rather than the discovery of it, and that is a weaker
test than it would have been a day earlier.
