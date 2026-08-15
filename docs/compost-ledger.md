---
Type: reference
Purpose: "The record of approaches killed while building EpiTrellis, each with what killed it and what would bring it back, so a reader can audit the kills rather than take the result on trust."
Depends on: [docs/departure-from-epistack.md, docs/document-style-guide.md]
Depended on by: [docs/status-ledger.md]
---

# Compost Ledger

Every entry names the approach at its strongest, the specific thing that killed
it, and what would reactivate it. This applies to the reader the same
subtraction the substrate applies to a claim: do not take the result on trust,
audit the kills.

Entries carried forward from EpiStack are marked. New entries are dated.

---

**1. Eleven invariants as conditions of membership.** Carried from EpiStack.
Killed by observed variance across twenty-one independent implementations. A
dimension five people fill five ways admits no shared requirement.
Reactivation: a demonstration that some capability's precondition set is
universal, such that no receiver could rationally decline it.

**2. Canonicalization as a universal participation floor.** 2026-08-12.
Proposed on the argument that content addressing requires shared serialization.
Killed by construction: a receiver hashing received bytes under its own function
needs no producer cooperation, and native crossing survives because a
transmitted bundle is re-derived locally. The error was importing a waist from a
system whose cooperation requirements are inverted.
Reactivation: an operation between two parties that fails when payload
transmission is available and no contract is shared.

**3. Machine-checkable preconditions.** 2026-08-12. Requiring every capability
precondition to evaluate mechanically to true or false. Killed as an
attenuation-line violation: many preconditions are intrinsically semantic, and
requiring mechanical evaluation drags generative judgment into the fixed seam.
Reactivation: none as stated. Warrant-representability replaced it, where the
runtime resolves what warrant exists rather than whether the precondition holds.

**4. State survival as the anti-capture property.** 2026-08-12. Removing a
provider must not invalidate unrelated objects, relations, identity, or receiver
state. Killed by email: Gmail satisfies it completely and remains load-bearing
for whether mail is delivered, because deliverability quality has scale
economies a small provider cannot buy past.
Reactivation: a demonstration that capability substitutability is entailed by
state survival in some restricted class.

**5. Blanket residue publication.** 2026-08-12. Opening the concentration loop
by requiring a capability's learning residue to be published. Killed twice:
receiver-specific residue cannot be published without destroying privacy, and
adversarial residue cannot be published because publication is an evasion
specification. What survives publishes only for public facts, which are the
capabilities least prone to concentration.
Reactivation: a privacy-preserving derived-observation format, or an outcome-only
format whose evasion degradation is measurably slow.

**6. Referent stability as the first gate.** 2026-08-13. Killed by measurement:
thirteen of thirteen encountered objects produced a resolvable referent.
Replaced by payload acquisition, which splits three ways.
Reactivation: an object population where referents do not hold. The probe
measured objects that were shareable, which selects on the property tested.
*Corrected 2026-08-14: it was eleven of thirteen verified, not thirteen of
thirteen. Two were discarded by the instrument, which records no referent when
the fetch fails, and not by any property of the objects. The kill stands on the
corrected number. The original text is left above because the overstatement is
itself an entry, filed as 9 below.*

**7. Attack conversion as a separate function.** 2026-08-12. Sybil dissolution,
where forging N corroborators costs N genuine contributions and the attacker
becomes a contributor. Killed as a category error: it is the success condition
of manufacture resistance, not a distinct job.
Reactivation: an instance where conversion occurs without cost imposition.

**8. Two app builds, native and web.** 2026-08-13. One for reach and one for
sovereignty. Killed because two builds means one is real and the other rots, and
the one with users will be the real one.
Reactivation: none. The replacement is storage as a contract the user selects,
so one build serves both.

**8a. The journal is append-only, without exception.** 2026-08-15. Weakened
deliberately, and recorded here rather than quietly, because the rule is one the
project has held to since the first commit and still holds everywhere else.

Held: no row is ever rewritten or deleted. A superseded finding stays visible
beside its replacement, and the record of having been wrong is part of the
evidence.

Killed by a case the rule cannot answer. An unlisted link is a capability rather
than an address: possession is the access. The operator's journal contains two,
a `claude.ai/share/` link and a Google Docs `/d/` id, and both had already left
the device inside a bundle. Excluding them from future exports does not help,
because the disclosure is the address and the journal holds it. Append-only says
the only remedy is to keep it forever.

Survived, and this is most of the rule. Exclusion from an export is a separate
mechanism that stays fully append-only: a `redaction` event names a capture, the
rows remain, the bundle skips them and reports how many it skipped, and an
`unredact` event reverses the decision without erasing that it was made. That
covers everything except the case where holding the bytes is itself the harm.

What was given up, stated plainly: `probe.py purge` rewrites the journal and
deletes rows. No bytes-are-forever guarantee survives it. What was kept instead
is weaker and worth naming precisely: the record cannot silently lose things.
The rewrite appends an event saying a rewrite happened, when, and how many rows
went, and deliberately not what they were. A reader of a purged journal can see
that it is incomplete and by how much, which is the property that actually
carries the evidential weight. "Nothing was removed" was never the thing being
protected; "nothing was removed without saying so" was.

Reactivation: a way to hold a capability URL that makes possession safe. Nothing
here is close to that, and the fallback is not to hold it.

**9. The headline of a document about not overclaiming, overclaimed.**
2026-08-14. `docs/findings/probe-referent-stability.md` asserted that every
encountered object produced a resolvable referent, four lines below its own table
recording two that did not. The claim propagated to three other documents.
Killed by an outside reading of the tree by a party with no attachment to it, in
one pass. The author had read the document repeatedly without seeing it.
Reactivation: none. The residue is that internal review does not catch this
class, and the checks did not either, because no check compares a prose claim
against a table in the same file.

**10. Trusting a document to hold a copy of a fact about the tree.**
2026-08-14. Not an approach anyone proposed, which is why it took four instances
to see: it is what the repository does by default every time a document
describes the system rather than the world.

The shape. A document holds a copy of a fact whose authority lives elsewhere in
the tree, and the authority moves underneath it. Findings about the world do not
drift this way, because a measurement is finished. Documents about the system
drift because the system is not.

Four instances, three of them that shape:

*Entry 9's universal quantifier.* The referent finding asserted that every
encountered object produced a resolvable referent, four lines above its own table
recording two that did not. This one is not the copy shape. It is a claim
contradicted by evidence in the same file, and it is filed here because it was
found in the same pass and shares the residue.

*`docs/design/pocket-revised-v0.2.md`'s coverage claim.* It listed TikTok and
Google Docs as absent from the corpus while the finding recorded both as
measured. A stale coverage claim reads as a limitation honestly admitted, which
is what let it survive several readings.

*CLAUDE.md's check count.* It listed three checks and said all three must pass,
after a fourth had landed and was running in CI.

*CLAUDE.md asserting `scripts/verify-docs.py` did not exist.* Written when it did
not, left standing after it did, and still live in the tree for two commits after
the same document's Checks section had already been corrected to require it. One
document, two sections, opposite claims about one file.

Killed by: `scripts/verify-selfdescription.py`, and by deleting the copies rather
than maintaining them. Counts of checks and inventories of function names now
point at `scripts/` and `functions/` instead of restating them. A pointer cannot
go stale, and the count argued nothing anywhere.

What the check catches, established by running it against the commits where each
instance was live rather than by assertion:

| Instance | Caught | By which half |
|---|---|---|
| CLAUDE.md says `verify-docs.py` does not exist | yes, at every commit where it was live | negation direction |
| CLAUDE.md check count of three | no | neither |
| pocket-revised coverage claim | no | neither |
| Entry 9's universal quantifier | listed for review, not caught | advisory half |

Running it against history also failed the check itself. At `9cfad09`, where
CLAUDE.md correctly said `verify-docs.py` did not exist yet and it correctly did
not, the existence direction reported the true statement as a failure. A document
is allowed to name what is not built, which is what a deferral list is for. The
fix exempts a path from the existence direction when the sentence declares it
absent, since the other direction already covers the case where such a path turns
out to be present. Neither half had been run against history before that, and the
error would have shipped.

**A fifth instance, 2026-08-14, and the first one inside the instrument rather
than in a document.** The journal could not say which code wrote it. Establishing
that the first corpus came from a probe predating the referent-hashing code took
four separate diagnostic commands and a deduction from absent keys, when one
field on the capture event would have shown it outright. `probe.py bundle`
reporting 0 objects was read as a bug in bundle; bundle was reading correctly and
the rows lacked the field.

This widens the class beyond what entry 10 first described. The shape was stated
as a document holding a copy of a fact whose authority lives elsewhere in the
tree. Here there was no copy at all: the data did not describe itself, and the
authority for which code wrote a row existed nowhere. Documents drift by holding
a stale copy. Data drifts by holding none, and the failure looks like a bug in
whatever reads it. The class spans documents and data, which the original entry
did not anticipate.

Killed by stamping every capture with the SHA-256 of the running probe, and by
deriving the missing hashes at read time rather than rewriting rows. Absence of
the stamp is now itself the marker for the older instrument.

**This is not solved.** Two of four are caught by nothing. The check count is
caught only because the count was deleted, which fixes the instance and not the
class: any future prose count of anything is invisible to both halves. The
coverage claim is caught by neither half and no check was proposed for it,
because a claim that a corpus lacks something is a claim about the world and the
only authority is the journal, which is exactly the deferred number checking.
The advisory half produces a review queue of 55 lines, 27 of them in the
trellises where universals are the house style and almost all of them sound, and
a queue nobody reads is worth nothing. It did list entry 9's exact sentence at
the commit where that claim was live, which is the only evidence that the
advisory half is pointed at anything real.

**A sixth instance, 2026-08-14, in operator-facing output, which is a new
surface for the class.** `probe.py bundle` printed, on every run where anything
collapsed: "the same object reached twice by different addresses is one object,
and nothing had to agree for that to hold." On the device journal that case had
not occurred. The entire collapse was one object seen four times, every
alternate referent field was empty, and nothing in the data showed two distinct
addresses meeting at one key. The sentence described the capability the code was
written to demonstrate rather than the result the run produced.

It is the same shape as the documents, moved: a claim held in prose whose
authority is elsewhere, asserted in general terms where the specific case would
have been checkable. What is new is the surface. A document drifts silently
until someone reads it; a printed message is read by the operator on every run
and is the most likely thing to be quoted onward, which makes it the worst place
for the class to live and the last place anyone was looking for it.

Killed by having the message report what the run actually shows. It now splits
the collapse into repeats of one address and distinct addresses meeting at one
key, and when the second count is zero it says so rather than asserting it in
general. Neither number was available before, because the bundle keeps only the
referent key and the distinction lives in the journal.

No check catches this one either. The output is prose assembled at runtime and
`verify-selfdescription.py` reads files in the tree, not what a program prints.

**A seventh instance, 2026-08-15, and a different failure than the other six.**
`probe.py purge` deleted journal rows and left the payload bodies on disk. That
was known from the moment purge was written: it was flagged in the report, and
`probe/MANUAL.md` said so plainly for several commits. The documentation was
accurate the whole time. The command still did not do what its name says, and
the case that motivated redaction, an accidentally shared private thing, is
exactly the case where the body matters more than the address.

The other six instances are documents drifting away from a tree that moved. This
one is the opposite and worse: the document tracked the code perfectly, and the
accuracy is what let the defect sit. A limitation written down reads as a
decision. Nobody re-examines a decision, and "documented" and "handled" are
indistinguishable in a changelog.

This is the fifth or sixth time in this repository that documenting a defect has
substituted for fixing it. The others were smaller and mostly got fixed a turn
or two later, which is what made this one easy to leave: the pattern usually
self-corrects, so it does not look like a pattern.

No check catches it and none is proposed. A check that flags "this document
describes a limitation" would fire on every honest caveat in the corpus, and
the corpus is deliberately full of them. The distinction between a limitation
that is a decision and a limitation that is a defect awaiting attention is not
mechanical, and inventing a marker for it would produce a field nobody
maintains.

Reactivation: not applicable. What remains is a working note, that a limitation
recorded in a manual should carry whether it is accepted or merely known, and
that nothing currently makes anyone write that down.

The fifth instance is no better covered than the others. Nothing checks that a
journal row can name the code that wrote it, and no check here could: the
authority is a file on a phone this repository never sees.

Reactivation: not applicable, since nothing was killed that could return. What
would close it is the findings pipeline that recomputes cited figures from the
journal, which remains deferred.

A process note rather than a thing to build. Entry 9 and the check count were
both found by a reader coming to the tree cold, after the author had read those
documents repeatedly without seeing either. Two data points saying internal
review does not catch this class. The step that follows is a cold read before any
push touching a self-describing document, done by something that has not been
editing it. Recorded here rather than automated, because automating it is what
produced the illusion of coverage the last two times.
