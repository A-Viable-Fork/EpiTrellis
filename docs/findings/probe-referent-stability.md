---
Type: finding
Purpose: "What the referent stability probe established across thirteen encountered objects, with the retractions it forced."
Depends on: [probe/MANUAL.md]
Depended on by: [docs/departure-from-epistack.md, docs/status-ledger.md, docs/design/pocket-revised-v0.2.md, README.md, docs/findings/verdict-is-per-encounter.md, docs/findings/join-intersects-the-wrong-field.md]
---

# Finding: Referent Stability

**Instrument.** `probe/probe.py`, share-sheet capture on Android under Termux.
**n.** 13 objects encountered in ordinary reading, plus 8 instrument artifacts excluded.
**Dates.** 2026-08-13.
**Operator.** One person, one device, one day.

## Result

Eleven of thirteen encountered objects produced a verified, normalized referent,
derived locally with no cooperation from the producer. The remaining two were
discarded by the instrument rather than by any property of the object. The
receiver held a good shared URL for both, and the probe records no referent when
the fetch fails, so it threw away an address it already possessed.

| Producer | Referent | Payload |
|---|---|---|
| LessWrong | canonical | 121,682 chars |
| Substack | canonical, og:url, DOI from body | 10,799 chars |
| arXiv | canonical, og:url, DOI | 5,022 chars |
| X | canonical, og:url | tweet body carried in the title tag |
| Google Docs | og:url resolving to /mobilebasic | 8,369 chars |
| YouTube | canonical, normalized: share token stripped, mobile redirect resolved | video, not text |
| TikTok | canonical via share shortlink | video, not text |
| Reddit | shortlink resolves to canonical comments URL | 6 chars in an 8,459-byte response, 4 of 4 |
| Facebook | shared URL held, discarded on fetch failure | HTTP refusal |
| NYT | shared URL held, discarded on fetch failure | 403, no archive snapshot, save attempt returned 520 |

## What this overturned

**Referent stability was the wrong gate.** It was the sharpest expected break in
the receiver-substrate hypothesis and it did not occur. Two producers supplied a
better referent than the URL shared.

**Payload is the problem, and it splits three ways.** Not text at all. Withheld
by the producer. Behind a client-side render. Each has a different answer and two
are addressable by reading what the producer's own application already rendered.

**A retraction.** LessWrong was reported refusing with HTTP 429. That was the
instrument sending a bare user-agent string. With browser-shaped headers it
returned cleanly. The claim that the site best suited to this substrate was least
reachable by it was wrong.

**A second retraction.** Reddit was classified `client_rendered`. It is not: an
application bundle is large and Reddit's response is 8KB with 475 bytes of script.
It is a refusal that returns 200, now classified `soft_refusal`.

**A third retraction, 2026-08-14.** This document said "Every encountered object
produced a resolvable, normalized referent" four lines above its own table
recording two that did not, and the claim propagated to the README, the compost
ledger, and the departure record. The true reading is eleven of thirteen
verified, with two discarded by the instrument. The old claim is preserved here
because it was published, and the failure is recorded as entry 9 of the compost
ledger.

## What this does not establish

**The denominator understates.** The probe records no referent when a fetch
fails, so an object whose address was fine and whose bytes were refused is
counted as producing nothing. Facebook and NYT are both that case. This is a
known instrument bug and not a property of the objects, and until it is fixed
the eleven is a floor rather than a measurement.

*Fixed in the instrument 2026-08-14, not in this corpus. A refused fetch now
keeps the referent it already derived and records it with the flag
`referent_held`, so referent stability and payload acquisition stop being
conflated. The eleven above is unchanged, because this measurement was taken
with the old instrument and a measurement is not re-run by editing the document
that reports it. A later run under the current probe is what would move the
number.*

*Provenance, recorded 2026-08-14. Every row of this corpus was written by a
probe that predates both the instrument stamp and the referent-hashing code, so
its `reference` rows carry no `referent_key` and its `finding` rows carry no
`object_hash`. Captures written from 2026-08-14 onward carry an `instrument`
field holding the SHA-256 of the running probe. Absence of that field is the
marker for the older instrument, and the rows were not retroactively stamped.
The missing hashes are recoverable by derivation at read time, since
`object_hash` is a pure function of a URL those rows already carry.*

The probe measured objects that were shareable, which selects on the property
being tested. Objects that cannot be shared as a link never entered the sample
and their frequency is unmeasured.

Absent from the corpus: Instagram, news paywalls other than one, Slack, email,
anything geo-varying, and any application offering no share affordance beyond a
screenshot.

Two readings remain distinguishable only with more data. Either producers
converged on stable canonical identity because link previews, search indexing,
and their own analytics all demand it, in which case this generalizes. Or
research-adjacent reading skews toward well-formed sources, in which case it
does not.
