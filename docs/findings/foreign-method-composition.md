---
Type: finding
Purpose: "What vendoring an independently designed competition method established about this substrate, which is that the vendoring mechanism works and composition remains untested because the journal had nothing to offer it."
Depends on: [functions/concentration/GAP.md, functions/concentration/ATTRIBUTION.md]
Depended on by: [docs/corpus-index.md, docs/status-ledger.md]
---

# Finding: Foreign Method Composition

**Instrument.** `functions/concentration/`, wrapping `concentration.py` and
`warrant.py` from `kyaloeric/epistemic-stack` at commit
`89d6632abd0b7678b738b722547d17b984fe1014`, MIT, vendored byte for byte.
**n.** 1 foreign method, over a 27-event synthetic journal covering 9 objects.
**Dates.** 2026-08-14.
**Operator.** One person, one repository, one afternoon.

## Result

**Proof 2 reads: mechanism confirmed, composition untested.**

Those are two claims and only the first is established. A foreign method can sit
in this tree, keep its bytes, keep its license, and be invoked by the loader
without being rewritten into our epistemology. That is a result about the
loader and the vendoring discipline.

It is not a result about composition. The journal handed the method an empty
room. His arithmetic never ran on anything, because there was nothing for it to
run on, so nothing was learned about whether an independently designed method
can operate over what this substrate holds. Reporting this as Proof 2 succeeding
would be reporting the wrapper's own reflection as evidence.

## The four grades and which came back

The outcome was graded before it was run, so that a weak result could not be
narrated into a strong one afterward.

| Grade | Meaning | Outcome |
|---|---|---|
| Composes with signal | His math runs over an honest translation and returns a non-empty concentration or crux result | no |
| Composes empty | It runs, validates, and returns nothing, because our journal carries no relation between objects and therefore no edges and no conclusion | **this one** |
| Composes only by invention | It returns something, and only because the wrapper manufactured structure the journal does not hold | no |
| Fails to compose | It cannot be called at all | no |

Nine nodes, zero edges, zero conclusions, zero concentration results, zero
cruxes, zero circular-support flags.

## What the method said about us, in its own words

`warrant.assess_graph` never calls `validate_graph`. The wrapper calls it
explicitly, and its warnings are the finding stated in his vocabulary rather
than ours, which is what makes this evidence rather than self-report.

Once per object:

> claim 28e9e3212d06ddb6 has kind 'None' (expected one of ['assumption',
> 'conclusion', 'evidence', 'inference', 'methodological']).

And once for the corpus as a whole:

> no claim has kind 'conclusion' — concentration is computed per conclusion, so
> there will be nothing to audit. Mark your bottom-line claim(s) with "kind":
> "conclusion".

## The gap is a missing layer, not a missing field

This is the same weight as the referent stability result and it points the other
way. Referents held where they were expected to break. Here the substrate is
missing something structural that no amount of additional fields would supply.

The journal individuates objects. `reference` and `finding` both carry
`object_hash`, derived locally with no producer cooperation, so a set of
distinct nodes falls out without inventing anything. That is the one place the
two shapes meet.

**The journal carries no relation between objects at any granularity.** There is
no lossy version of the edge set, no coarse approximation, and no partial
translation. There are zero edges, and any other number would have to be
manufactured.

A faithful translation needs three things, and they are needed in order:

**Propositional content**, distinct from the object. An object is a document; a
claim is a proposition. The journal individuates the first and is silent on the
second.

**A typed directional relation between propositions.** Someone has to assert
that this proposition supports that one. That assertion does not come from
encountering an object. It comes from reading two of them and forming a view.

**A conclusion.** A proposition marked as the bottom line under audit.
Concentration is computed per conclusion, and the journal does not record
questions.

The order is load-bearing. Propositions without relations still yield nothing,
because concentration is a property of a support structure. Relations without a
conclusion still yield nothing, because concentration is computed per
conclusion. The missing layer is the one where a receiver stops recording and
starts arguing.

## Three inventions that were available and were refused

Each would have produced a number that looks like a result. They are recorded
because the reach for them is itself the finding, and because the first is
genuinely tempting.

**The `Depends on` graph in `docs/`.** A real directed acyclic graph over real
nodes, already checked in both directions by `verify-docs.py`. It represents
document dependency rather than evidential support, so a concentration score
over it would describe our documentation while reading as a result about our
evidence. Its cleanliness is what makes it dangerous.

**Co-occurrence.** A shared `object_hash` means two events concern one object.
An `alt_referent` means two addresses denote one object. A `fetch_pair` means
one URL was fetched twice with different headers, which is a fact about the
instrument. None of the three is support.

**`finding.kind` as a claim kind.** Every value types the instrument's outcome
rather than a claim about the world. Mapping them onto his kinds would have
silenced the validator's warnings while making the numbers meaningless, which is
strictly worse than the warnings.

`functions/concentration/GAP.md` carries the local detail: the exact input shape
`assess_graph` requires, field by field, and what our events hold against it.

## What this does not establish

**Composition, at all.** The vendored copy is functional: against upstream's own
`eggs` case, 202 claims and 220 edges, it returns 39 concentration results, 10
cruxes and 2 circular-support flags, and against `blackholes`, 157 claims and
363 edges, it returns 21, 10 and 1. So the empty result is a fact about our
journal rather than about the vendoring. But the wrapper exercised only his
input validation and his empty path. The dependency collapse, the decay walk,
the crux ranking and the Tarjan detector all sat idle. Composition has been
attempted and not tested.

**Anything about foreign methods in general.** n=1. Whether other independently
built methods want the same claim-graph shape is unmeasured, and it is the
question that decides whether capability supply is the bottleneck here or
whether the competition built for a layer above the one this repository built.

## A scaling note, for whoever wires this to a real journal

`loader.invoke` kills a function at 120 seconds. On upstream's largest case,
1590 claims and 4434 edges with 212 conclusions, `concentration_for` was
measured at 0.41 seconds per conclusion over the first five, and the cost varies
with the conclusion because supporter counts range from a handful to 1002.

The call counts are established by reading the code rather than by timing. His
own CLI path, `compute_concentration`, calls `concentration_for` once per
conclusion, so 212 calls. But `assess_graph`, which is the entry point here and
the one his own web endpoint uses, calls it once per conclusion inside
`deterministic_cruxes` and then again for every conclusion when building its
`concentration` list, so 424 calls for the same graph. Twice the work for the
same answer.

A full `assess_graph` run on that case completes in 165 seconds, returning 212
concentration results, 10 cruxes and 40 circular-support flags. It is not a
hang. It is roughly 45 seconds past the loader's timeout, and his own CLI path,
doing half the calls for the same answer, would land under it.

The first attempt here was killed at two minutes and reported as not finishing,
which established only that it exceeded two minutes. The number above is what
replaced that.

The shipped `cases/covid/out/concentration.json` records all 212 conclusions of
the shipped `graph.json`, so his pipeline did complete on this graph. Nothing
here is broken. A journal ever rich enough to produce a real support graph would
meet the timeout before it met a wrong answer, and the fix belongs in the
wrapper or the loader rather than in his bytes.
