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
