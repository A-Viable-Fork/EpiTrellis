---
Type: design
Purpose: "What the phone application is after the referent probe, superseding the parts of v0.1 named in it."
Depends on: [docs/findings/probe-referent-stability.md, docs/departure-from-epistack.md]
Depended on by: [docs/corpus-index.md]
---

# TRELLIS POCKET, REVISED

**What the phone application is, after measurement**

Design revision v0.2 · 13 August 2026
Supersedes the v0.1 proposal in the parts named below
Evidence: referent stability probe, n=9 encountered objects, 8 further instrument captures

---

## What changed

The v0.1 design was built around a worry that turned out to be misplaced, and it under-weighted a problem that turned out to be the real one.

**The worry.** Personalized feeds, ephemeral content, and A/B-split delivery would mean encountered objects carry no referent stable enough for structure to attach. This was named the sharpest known break in the hypothesis and made the first gate.

**The measurement.** Nine encountered objects across seven producers. Every one produced a resolvable, stable referent. Zero failures.

| Producer | Referent | Payload |
|---|---|---|
| Substack | canonical, og:url, DOI lifted from a body citation | 10,799 chars, full |
| arXiv | canonical, og:url, DOI | 5,022 chars, abstract |
| X | canonical, og:url | 955 to 1,449 chars, tweet body carried in the title tag |
| YouTube | canonical, normalized: strips the share token, resolves the mobile redirect | 50 to 71 chars. The object is a video |
| Reddit | shortlink resolves cleanly to the canonical comments URL | 6 chars in an 8KB response |
| Claude | title only | 14 chars in a 50KB application bundle |
| Facebook | none | HTTP refusal |

Referent stability is not the problem. Two producers gave a *better* referent than the URL shared: YouTube normalized away a tracking parameter and a mobile-host redirect, and Substack surfaced a DOI that was inside the article rather than in its metadata.

**The real problem is payload, and it splits three ways.**

*Not text at all.* YouTube, and by extension podcasts, images, video. The referent is excellent. There was never going to be a body to fetch. Nothing is broken; the object is simply not made of text.

*Withheld by the producer.* Reddit returns 200 OK with a six-character stub. Facebook refuses outright. These are refusals, one of which does not announce itself. The content renders perfectly in the producer's own application; it will not come down an HTTP request from a script.

*Behind a render.* Claude ships a real application bundle and fills the page client-side. Distinguishable from a refusal by size: an application is large and a brush-off is not.

Each has a different answer, and two of the three are answered by reading what the application already drew on the device's own screen.

---

## What this does to the architecture

**The acquisition layer becomes the hard part, and the device becomes the answer.**

In v0.1, root was optional, peripheral, and justified by ambience: a faster gesture, more context, nicer invocation. Under measurement that justification is weak and the honest one is different.

The producers that withhold payload from a script render it fine in their own application. Accessibility services and screen-level capture read what is already on the display. So privileged local capture stops being a convenience and becomes the answer to a specific, measured, reproducible failure affecting a large share of what people actually encounter.

This does not promote root to a requirement. It relocates the argument. Non-root capture is sufficient for referents, which is the harder half of the problem, and it is sufficient for full payload wherever a producer serves it: Substack, arXiv, X, most ordinary web content. The privileged path recovers payload from the walled surfaces and nothing else. That boundary is now empirically drawn rather than asserted, which also makes the degradation path clear: without root, walled objects are addressable, annotatable, relatable, and their text is absent.

**The reference is the join key, and it is derived locally.**

The most consequential result is one the probe produced as a side effect. Each of those canonical references was derived by a receiver acting alone, with no cooperation from the producer, and it is deterministic: another person resolving the same object independently lands on the same address.

That is the whole coordination substrate. Two people who have never communicated, using different clients, converge on one identity for one object without any shared canonicalizer, index, or negotiation. The producer-side participation floor really is empty, and this is what it buys.

**Payload separates cleanly from identity, and copyright follows.**

Reddit's stub, Facebook's refusal, and YouTube's video all fail to yield payload while yielding a fine referent. The system coordinates around objects it does not hold, which is the copyright separation from v0.1 arriving as an observed property rather than a design choice.

---

## What the application is

A receiver-owned memory that accrues from ordinary reading, and becomes a shared one where other people happen to have been.

### Alone, which is where it must work first

Share a link. The receiver resolves the reference, records what it found, and keeps it. Later, encountering the same object or a related one, the earlier encounter is present: what you saved, what you thought, what it connected to, what has since been corrected.

This must be worth using at n=1. Every network of this shape that has died, died from opening the object and finding nobody there. Personal memory is the only version that works on day one, and other people's contributions have to be additive rather than the premise.

The n=1 value proposition, stated plainly: *what have I encountered about this, what did I conclude last time, and which of my saved conclusions does this new thing affect.*

### With people you have chosen

You sync bundles with a handful of peers directly. Opening an object, their notes on it are present, because you already pull from them. No center, works offline, ceiling is your address book.

### With communities

A Discord, a lab, a reading group. You subscribe to their bundle and their annotations on that object appear. The community is a set of coordination commitments, not a server. Removing Discord removes a surface and leaves the community's durable state intact.

### With strangers

This requires an index: given an object address, who has published anything about it. That is a center, and pretending otherwise would be dishonest.

What makes it survivable is that it is a pointer service holding addresses and locations, never content. Because content is addressed by hash, an index cannot misrepresent what a claim says, only which claims exist. Query several and merge. Removing one costs coverage and destroys nothing, since local state and peer bundles are untouched.

Replaceable center rather than sovereign root, and it is testable rather than aspirational: delete the index and check what stops working.

Note what never happens. Nobody fetches content from the original site on anyone else's behalf. Substack is never involved and never knows. What moves between people is annotation keyed to an address each side computed independently.

---

## Revised build order

Sequenced by what can produce a disconfirming result soonest.

**Done. Referent probe.** Answered. The result reshapes the rest.

**Next. Payload recovery from walled surfaces.** The measured failure. Screen or accessibility capture on the rooted device, applied to Reddit and Facebook specifically, and honest about whether what comes back is usable structure or a screenshot with text in it. This is the gate: if walled payload cannot be recovered into something structurable, the substrate is limited to the open web plus whatever people type themselves, which is a smaller design but still a real one.

**Then. Local memory at n=1.** The journal already holds the encounters. What is missing is retrieval and connection: same object seen again, related objects, affected conclusions. This is the adoption question and no amount of architecture substitutes for it.

**Then. Second client.** Client-independent receiver state cannot be retrofitted and cannot be verified without a second implementation. It stays early even though it produces no user-visible value.

**Then. Two-peer sync.** Two devices, direct bundle exchange, one object annotated on both. The smallest possible test of whether independently derived references actually join. Expected to work, given the probe results, and worth confirming before anything is built on the assumption.

**Later. Community bundles, then an index.**

Deferred, from v0.1: the interchange format stays an append-only event journal with no semantic schema until the data says what the schema must hold. A format others adopt becomes unkillable by adoption rather than by being right.

---

## What is still open

**Whether walled payload is recoverable into structure.** The next gate. Currently unknown.

**Whether n=1 is enough to hold anyone.** Unknown, and the most likely cause of death.

**Whether the index stays replaceable under success.** Discovery is the function that most wants a center, and it is the one an incumbent would concentrate first. Deferred to the capture-dynamics program with the loop test as the instrument.

**Non-text payload.** A video has a fine referent and no body. Transcripts are a capability, supplied by a provider, contestable and replaceable like any other. Not solved here, and correctly not the substrate's problem.

---

## What the measurement did not cover

Nine objects, one person, one device, one day. Every producer here is one a research-adjacent reader encounters. Absent: TikTok, Instagram, news paywalls, Google Docs, Slack, email, anything geo-varying, and anything from an application offering no share affordance beyond a screenshot.

That last category is the one that could still overturn this. The probe measured objects that were shareable, which is a selection on exactly the property being tested. Objects that cannot be shared as a link never entered the sample, and their frequency is unmeasured.

Two candidate readings of the referent result, distinguishable only with more data: producers converged on stable canonical identity because link previews, search indexing, and their own analytics all demand it, in which case the result generalizes; or research-adjacent reading skews toward well-formed sources, in which case it does not.
