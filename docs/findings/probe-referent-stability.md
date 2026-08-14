---
Type: finding
Purpose: "What the referent stability probe established across thirteen encountered objects, with the retractions it forced."
Depends on: [probe/MANUAL.md]
Depended on by: [docs/departure-from-epistack.md, docs/status-ledger.md, docs/design/pocket-revised-v0.2.md, README.md]
---

# Finding: Referent Stability

**Instrument.** `probe/probe.py`, share-sheet capture on Android under Termux.
**n.** 13 objects encountered in ordinary reading, plus 8 instrument artifacts excluded.
**Dates.** 2026-08-13.
**Operator.** One person, one device, one day.

## Result

Every encountered object produced a resolvable, normalized referent, derived
locally with no cooperation from the producer.

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
| Facebook | none | HTTP refusal |
| NYT | none | 403, no archive snapshot, save attempt returned 520 |

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

## What this does not establish

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
