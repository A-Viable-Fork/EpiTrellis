# Gap: what his method needs that this journal does not carry

Written 2026-08-14, against commit `89d6632abd0b7678b738b722547d17b984fe1014`
of `kyaloeric/epistemic-stack`.

The method runs. It validates our translation, accepts it, computes over it, and
returns nothing. That is not a failure of the wrapper and not a defect in his
code. It is the shape of our journal becoming visible under a foreign
instrument, which is what the exercise was for.

## What he needs

`warrant.assess_graph` reads a dictionary with `claims` and `edges`.

**Claims** must be a non-empty list. Each needs an `id`, unique across the list.
Each should carry a `kind` drawn from `evidence`, `inference`, `assumption`,
`conclusion` or `methodological`; a kind outside that set is a warning rather
than an error. `text` and `attestations` are optional and get filled in by
`_normalize`.

**Edges** must be a list, and each needs `from`, `to` and `type`. The type
should be drawn from `supports`, `contradicts`, `is_evidence_for`, `restates`,
`caveats`, `depends_on` or `context_mutation`. Only three of those carry
evidential weight, at fixed strengths: `is_evidence_for` and `depends_on` at
1.0, `supports` at 0.6.

**At least one claim must have kind `conclusion`.** Concentration is computed
per conclusion. With no conclusion there is no question to ask, and the returned
concentration list is empty no matter how rich the rest of the graph is.

## What we have

The journal records six event types: `capture`, `reference`, `fetch_pair`,
`finding`, `archive_policy` and `archive_attempt`. Every one of them is a
statement about the act of encountering an object, or about what came back when
the receiver tried to fetch it. None of them is a statement about the world, and
none relates one object to another.

**Nodes exist and are honest.** `reference` and `finding` both carry
`object_hash`, derived locally from the object with no producer cooperation.
That individuates objects, so a set of distinct nodes falls out of the journal
without inventing anything. This is the one place his shape and ours meet.

**Kinds do not exist.** The journal never records what an object asserts. It
records that an object was encountered, what address resolved to it, and whether
its bytes could be obtained. `evidence`, `inference`, `assumption` and
`conclusion` are positions in an argument, and the journal contains no argument.
The wrapper therefore assigns no kind, and his validator says so, once per node
and once more for the absent conclusion. Those warnings are the finding stated
in his vocabulary rather than ours.

**Edges do not exist at any granularity.** This is the load-bearing gap.
Nothing in the journal expresses that one object supports, contradicts,
restates, caveats or depends on another. The journal is a record of encounters,
and encounters are not related to each other by anything the instrument
observes. There is no lossy version of this edge set, no coarse approximation,
and no partial translation. There are zero edges, and any number other than zero
would have to be manufactured.

## Three edges that were available and were refused

Each of these produces a graph his code would happily score, and each score
would be about nothing. They are recorded because the reach for them is itself
the finding.

**The `Depends on` graph in `docs/`.** It is a real directed acyclic graph over
real nodes, and `verify-docs.py` already checks it in both directions. It is
also document dependency, meaning "this document would be wrong without that
one", which is not evidential support between claims about the world. Running
concentration over it would return a plausible number describing the shape of
our documentation, and it would read as a result about our evidence. It is the
most tempting of the three precisely because the data is clean.

**Co-occurrence.** Two findings sharing an `object_hash`, an entry in
`alt_referents`, or the two halves of a `fetch_pair` all look like relations.
None is support. A shared `object_hash` means two events concern the same
object. An `alt_referent` means two addresses denote one object. A `fetch_pair`
means the same URL was fetched twice with different headers, which is a fact
about the instrument's method and not about any object's grounding. Turning any
of these into an edge would assert that one thing supports another because they
were seen together.

**`finding.kind` as a claim kind.** The values are `stable_referent`,
`client_rendered`, `soft_refusal`, `producer_refused`, `no_reference`,
`payload_no_referent`, `recovered_from_archive`. Every one types the
instrument's outcome. None types a claim about the world. Mapping them onto
`evidence` or `conclusion` would silence his validator's warnings while making
the resulting numbers meaningless, which is strictly worse than the warnings.

## What a faithful translation would require

Not new fields on existing events. The journal would need a new kind of event
that it currently has no way to produce, because the receiver would have to
assert something rather than record something.

Concretely, three things are missing and they are missing in order.

**Propositional content.** Something that says what an object asserts, distinct
from what the object is. An object is a document; a claim is a proposition. The
journal individuates the first and is silent on the second. Extracting
propositions from payload is a separate capability that does not exist here, and
it is not a parsing problem: it requires judgment about what a text claims.

**A relation between propositions, with a type and a direction.** Someone or
something has to assert that this proposition supports that one. That assertion
does not come from encountering an object. It comes from reading two of them and
forming a view, which is the receiver's judgment and not the instrument's
observation. His seven edge types are seven ways of holding such a view.

**A conclusion.** A proposition marked as the bottom line under audit. This is
the most receiver-specific of the three: what counts as the conclusion depends
entirely on the question being asked, and the journal does not record questions.

The order matters. Propositions without relations still yield nothing, because
concentration is a property of a support structure. Relations without a
conclusion still yield nothing, because concentration is computed per
conclusion. The gap is not one missing field, it is a missing layer, and the
layer is the one where a receiver stops recording and starts arguing.

## What this establishes

His method composes with our substrate at the level of nodes and refuses to
pretend at the level of edges. That is the correct behavior from both sides. The
substrate holds objects; the method measures arguments; the two meet only where
someone has built an argument out of objects, and nobody has yet.

The result is worth more than a number would have been. A concentration score
here would have meant the wrapper invented a claim graph, and the number would
have described the invention.
