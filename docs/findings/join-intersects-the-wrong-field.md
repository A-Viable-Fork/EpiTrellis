---
Type: finding
Purpose: "That for at least one producer the captured referent is unique to the act of sharing rather than to the object, so two parties who encountered the same object do not intersect on the field the join uses."
Depends on: [docs/findings/probe-referent-stability.md, docs/findings/verdict-is-per-encounter.md]
Depended on by: [docs/corpus-index.md]
---

# Finding: Join Intersects The Wrong Field

**Instrument.** `probe/probe.py`, share-sheet capture on Android under Termux,
read back through `probe.py bundle`.
**n.** 11 new captures over 2 producers, against a corpus that then held 39
findings and 27 objects. 6 Facebook objects, of which 5 carry an alternate
referent.
**Dates.** 2026-08-15.
**Operator.** One person, one device.

No address from the corpus appears here. The journal is the operator's reading
and several of its URLs carry access rather than merely address, so shapes are
given rather than instances.

## Result

For a Facebook share, the address the receiver captures is a per-share wrapper
of the form `facebook.com/share/p/<opaque-id>`. That identifier is unique to the
act of sharing, not to the object shared. The canonical post URL, which the page
volunteers about itself, is what two parties would have in common.

The consequence is exact. **Two people who share the same Facebook post derive
different primary hashes and do not intersect.** Both bundles hold the joinable
identity, and both hold it in `alt`, which the join treats as a candidate
equivalence rather than an assertion. The field the join intersects is `h`. The
field that would match is `alt`.

Five of the six new Facebook objects carry such an alternate referent. **These
are the first alternate referents to appear anywhere in this journal.** The
previous sixteen objects had none, which is why every earlier bundle reported
every `alt` field empty, and why the collapse observed earlier was entirely
exact-address repetition.

So the mechanism built for this case has now fired for the first time, and what
it revealed is that the primary field is the wrong one for this producer.

## What else the same run established

Eleven new captures, five NYT articles and six Facebook posts, all produced
resolvable references. Exclusions were unchanged at seven with no address and
two with no reference row, so nothing was discarded.

**That confirms the discard fix on the live capture path.** It had previously
been exercised only against a stub and, on old rows, by read-time derivation.
Referent held on every refusal.

NYT is uniform across six articles on three dates, free and paywalled alike:
`producer_refused` every time, referent held every time, canonical dated URLs
throughout.

## Recorded, not acted on

**Facebook splits within itself.** The reel refused; the six post shares came
back `client_rendered`. So refusal is a property of the producer for NYT and is
not a property of the producer for Facebook, where it varies by object type
within one host.

This bears on the payload split, which currently reads as three cases: not text
at all, withheld by the producer, behind a client-side render. A producer
occupying two of those at once, selected by what kind of object is being shared,
is not what a per-producer reading of that split would predict. The trellis that
would hold this has not been written, and this finding does not attempt it.

## What this does not establish

**That the join should change.** It should not, on this evidence. The manual's
position is that an `alt` hash match is a candidate equivalence and never an
assertion, and that position is correct: whether two addresses denote one object
is a judgment. Making the join intersect `alt` would silently promote a
proposal to an assertion for every user of every bundle.

**Who adjudicates the equivalence.** This is the open question the finding
leaves, and it is the reason the fix is not obvious. The producer volunteered
the canonical URL, so trusting it means trusting the producer about the identity
of its own object, which is precisely the cooperation this substrate is built to
do without. Trusting the receiver means each party decides alone and two careful
parties can still fail to match. Trusting a third party means naming one. The
substrate currently answers none of these, and a join that quietly picked one
would be answering it by default.

**That this generalizes beyond one producer.** One producer, six objects, one
device. Every other producer in the corpus captured an address that was already
the object's own. Whether per-share wrappers are common is unmeasured, though
the wrapper-host list in the probe suggests the shape is not rare.

**Why Facebook volunteers a canonical URL when its own share link does not
carry it.** Not investigated.
