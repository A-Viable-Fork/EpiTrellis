---
Type: reference
Purpose: "The record of what changed between the EpiStack competition submission and EpiTrellis, with the evidence that forced each change, maintained as further changes occur."
Depends on: [docs/findings/probe-referent-stability.md, trellises/parent-decomposition-v1.5.md, docs/document-style-guide.md, docs/status-ledger.md]
Depended on by: [README.md, docs/design/pocket-revised-v0.2.md, docs/compost-ledger.md]
---

# Departure from EpiStack

EpiStack was submitted to the FLF EpiStack competition in July 2026. EpiTrellis is what survived reading twenty other submissions and then measuring the world the design assumed.

The population figures throughout this document were recounted from the audit on 2026-08-14 and are now: twenty-two public repositories carrying twenty-one submissions, since the two A-Viable-Fork repositories are one entry, and since `bioc/epistack` and `epistack-app/epistack-legal` are name collisions and were never in the population. Fifteen of the twenty-two carry no license file. Seven carry one: five MIT, one GPL-3.0, one AGPL-3.0. Earlier figures in the entries below are marked where they were wrong and are not removed.

This document is maintained. Each entry names what the submission held, what overturned it, and what survived. Entries are not removed when superseded; a later entry supersedes an earlier one and both stay visible, which is the same discipline the journal applies to findings.

---

## 1. Eleven invariants stopped being conditions of membership

**Held.** Composition without laundering requires shared invariants. Eleven were stated: claims carry types, standing stays at or below what its supports deliver, grading reads structure and stays blind to who produced a claim, a claim crossing an untyped boundary sits at the floor until locally re-typed, and so on. A kernel satisfying them could compose; one that did not, could not.

**Overturned by.** Twenty-one public submissions built independently, twenty of them by other people, varying on nearly every dimension the eleven fix: grade representation, relation vocabulary, independence measure, crux definition, disagreement representation, verification method, source classification. Several variations are better than the originals. A dimension five people fill five different ways is not a shared requirement, and a rule most competent implementations depart from describes one implementation carrying a universal quantifier.

**Survived.** All eleven, with a different modality. They are preconditions for particular capabilities rather than conditions of participation. Contamination detection is required for corroboration. Meaning pinning is required for native crossing. Neither is required to participate.

**Consequences.**

Conformance became a vector rather than a verdict. An artifact declares which functions it fills and the capabilities follow mechanically, so a registry entry describes rather than judges, can be written about anyone's work without permission, and gives nobody authority to delist.

Nulls became legitimate. A submission with no standing derivation at all, computing everything as queries at render time, is a choice rather than a deficiency. What matters is only the direction of error: dropping a function that removes a reading composes safely, and dropping one that inflates a reading does not.

Requirements moved to the receiver. A party who needs contamination detection requires it in their own standard. The party with the interest carries the requirement, and nobody is excluded from the commons so that a careful reader can be careful.

---

## 2. The producer-side floor is empty

**Held.** Content-addressing requires canonicalization, so every participant must share a canonicalizer for identity to be derivable. This looked like the one irreducible agreement point, a narrow waist by analogy with IP.

**Overturned by.** A construction. A receiver hashes received bytes under its own function and parses them with its own extractor, deriving identity with no producer cooperation. Native crossing survives too: a transmitted type bundle is re-derived and compared locally. Nothing requires the producer to have agreed to anything, or to know the substrate exists.

**Survived.** Shared canonicalization is the precondition for reference-without-payload, which is a capability. Copyright and dynamic content make that the common mode in practice, so identity contracts are near-universal in equilibrium while remaining optional in principle. Keeping the two distinct is what prevents an identity contract from becoming an unnoticed capture point.

**Why the analogy failed.** Routing requires both parties. Reading requires one. TCP/IP is the disanalogy, not the precedent.

---

## 3. Referent stability was the wrong worry

**Held.** The sharpest threat to a receiver-owned substrate is that encountered objects carry no referent stable enough for structure to attach: personalized feeds, ephemeral content, split delivery. This was made the first gate.

**Overturned by.** Measurement. Thirteen objects encountered in ordinary reading across seven producers, and every one produced a resolvable normalized address. Two produced a *better* referent than the URL shared: YouTube stripped a share token and resolved a mobile redirect, Substack surfaced a DOI from inside the article body.

**What replaced it.** Payload acquisition, which splits three ways with different answers. Not text at all, where the object is a video and a transcript is a capability rather than a fetch. Withheld by the producer, where Reddit returns a six-character stub inside a 200 OK and the Internet Archive cannot rescue a paywall. Behind a client-side render, distinguishable from a refusal by response size.

**A retraction inside the retraction.** LessWrong was reported as refusing, and that was an artifact of the instrument sending a bare user-agent string. With browser-shaped headers it returned 121,682 characters cleanly. The claim that the site best suited to this substrate was least reachable by it was wrong and is preserved here because it was published.

**Superseded, 2026-08-14.** The paragraph above says thirteen objects across seven producers and every one producing a resolvable normalized address. Both figures were wrong. It was thirteen objects across ten producers, of which eleven produced a verified referent. The two that did not, Facebook and NYT, were discarded by the instrument and not by the objects: the probe records no referent when the fetch fails, so it threw away a shared URL it already held. The overturning here still stands, and it stands on a smaller number than was claimed. See `docs/findings/probe-referent-stability.md` and entry 9 of `docs/compost-ledger.md`.

---

## 4. Licensing became segmented

**Held.** AGPL-3.0 across the whole repository.

**Overturned by.** The same reading that produced entry 1. EpiStack was the least composable entry in a field about composition. Sixteen of twenty-three public submissions shipped with no license at all, which under default copyright makes a field organized around compounding legally uncompoundable, and one AGPL entry is a smaller version of the same problem.

**Survived.** Copyleft where a provider could host a closed fork. The change is that one license across all layers is wrong, because the layers have opposite failure modes. A closed spec kills the waist, so the spec is CC0. An openly licensed hosted service invites a fork that publishes nothing, so the application layer is AGPL. License each layer against its own capture risk.

**A consequence discovered afterward.** Running functions as subprocesses over stdin and stdout creates no linking and no derivative-work relationship, so GPL, MIT, proprietary, and unlicensed functions coexist without contaminating each other. The isolation design was chosen for other reasons and turns out to be the licensing answer. Any design where functions link into the host forces one license across the whole ecosystem.

**Superseded, 2026-08-14.** "Sixteen of twenty-three public submissions" above was wrong in both numbers. It is fifteen of twenty-two public repositories with no license file, against seven that carry one: five MIT, one GPL-3.0, one AGPL-3.0. The argument is unchanged and the proportion barely moves. One of the fifteen declares MIT in its README while shipping no `LICENSE` file, which counts as unlicensed under default copyright regardless of what was intended, and is the sharpest small illustration of why the check reads the file.

---

## 5. What EpiStack got right and EpiTrellis keeps

The untyped floor, generalized. A claim arriving without a type participates fully, is addressable and citable, and grounds nothing until someone locally re-types it. The same construction now covers functions, capabilities, standing, and vocabularies. It was built once for types and turned out to be the general mechanism.

Non-inheritance. A claim resting on settled support does not inherit settledness; only its own basis reaches that tier. This is the one rule in the grade fold whose removal produces laundering rather than a different opinion.

Conservative contamination counting. Footprint closure over-counts shared dependence on purpose, because the error you cannot afford is believing two supports are independent when they are not. The same algorithm, pointed at providers rather than sources, is how apparent exit diversity gets tested.

Recomputation as the trust model, now graded rather than binary. Reproducible, replayable, attested, witnessed, folding by meet along a composed path. Determinism is not inherited, for the same reason settledness is not.

The honest accounting of gaps as a first-class output. The sorry ledger, the exclusion reservoir, and the discipline of recording what was killed and what would bring it back.

---

## 6. Open, and known to be open

The game-integrity family has no answer. Capabilities whose residue is a specification for evasion cannot externalize their learning, so the countermeasure that works for boundary functions does not work where concentration historically occurred.

Fork-choice coordination survives every resource being portable. Participants can leave and still cannot converge on where to go.

The self-governance tier, an operator's policy over their own device, is probably a sixth tier in the decomposition and is currently unrecorded.

`scripts/verify-docs.py` does not exist, so documents can still drift from artifacts. Entry 3 above cites thirteen objects while an earlier design document cites nine, and that drift occurred within a day of the document being written.

**Superseded in part, 2026-08-14.** `scripts/verify-docs.py` now exists and runs in CI. The paragraph above stays because it was published. What it got right survives: documents can still drift, because the check reads typed headers and dependency reciprocity and does not read cited figures. The specific drift it names is still unchecked by any script, and it was worse than a stale count. `docs/design/pocket-revised-v0.2.md` cites nine objects across seven producers while `docs/findings/probe-referent-stability.md` holds thirteen across ten, and the same design document lists TikTok and Google Docs as absent from the corpus when the finding records both as measured. A stale coverage claim reads as a limitation honestly admitted, which makes it harder to notice than a stale number. That document now carries a dated correction pointing at the finding, and the original text stays because a design document is expected to be overturned and the record of it is the point.
