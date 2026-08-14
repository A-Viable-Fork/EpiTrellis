# RECEIVER SUBSTRATE TRELLIS

**Archetype:** Operational, Normative secondary
**Parent:** Epistemic Substrate Decomposition Trellis v1.4
**Hierarchy contract:** Trellis Radiation (sibling spawn)
**Sibling:** Capture Dynamics Trellis. Relationship type: **complementary**
**Domain:** A receiver-controlled information substrate on personal devices, in which arbitrary encountered objects participate at zero capability and additional structure supplied by any party unlocks additional capabilities
**Status:** Active. No gate sorry designated. Gate candidates listed; first Shore must select one or record why the trellis proceeds without.

---

> **Operational Intent.** This trellis governs the construction of a working receiver-side substrate: a thin installed runtime that locally instantiates encountered objects with no producer cooperation, multiplexes capability providers that need no application identity of their own, and holds receiver state in a form no single client implementation owns. The deliverable is an artifact that runs, plus the findings it forces back to the parent. What gets killed: any construction requiring producer cooperation for local instantiation; any construction making receiver state meaningful only to the client that wrote it; any construction requiring a capability provider to acquire platform application identity for a capability that needs no application privilege; any design resting on a platform policy specific rather than its structure. What gets logged: every capability slot the artifact needs and cannot fill, every object class that resists instantiation, every place the implementation makes a concept feel obvious. The trellis exists to make the implementation an adversary of the parent's carving rather than its author.

---

## HIERARCHY

**Inherited from parent, in force here without restatement:** T0-GN, T0-GS, T0-FS, T0-NL, T0-SEAT, T1-EX, T1-ARG, T1-TIER, T1-EMPT, T1-UNL, T2-CONTAM, T2-CITE, T2-DIR, and Linter rules L1 through L14, including both leakage gates.

**Inherited resolutions treated as settled here:** the producer-side participation floor is empty (parent S-0); capability state is a compiled object rather than a taxonomic category (parent S-19); preconditions are warrant-representable rather than machine-checkable (parent S-10).

**Sibling coupling.** The Capture Dynamics trellis supplies the constraints this trellis must satisfy. This trellis supplies the test cases that sibling needs. Neither is prior. A finding in either that contradicts the other triggers a Shore in both.

**Leakage to parent.** Nothing discovered here enters the parent register as a concept without population trace or full T1-ARG discharge. The parent's L11 governs inbound; this trellis's L-A5 governs outbound.

---

## JURISDICTIONAL BOUNDARY

This trellis addresses what must be built and what the building reveals. It does not address:

- The taxonomy of functions. That is the parent's jurisdiction, and this trellis feeds it evidence rather than entries.
- Whether capability provision stays contestable. That is the sibling's jurisdiction.
- The merit or ranking of any competition submission, per the parent's boundary, which extends to every artifact in this chain.
- Business model, funding, organizational form, and legal structure.
- The substantive content of any knowledge domain the substrate carries.

---

## CHILD-SPECIFIC TIER 0

**T0-PROD. No producer cooperation.** `[Structural Commitment]`
No construction may require the producer of an object to do anything for a receiver to instantiate that object locally. The producer may be ignorant of the substrate, hostile to it, or defunct. Constructions requiring producer participation are capabilities with preconditions, never floors.
*Falsification mode: an operation is exhibited in the running artifact that fails when the producer takes no action, and the operation is presented as basic rather than as an unlocked capability.*

**T0-CLIENT. Client-independent receiver state.** `[Structural Commitment]`
Receiver state must be interpretable by an implementation other than the one that wrote it. Local persistence is insufficient: state that only the removed client can read is not survival. The unit is objects, capability-contract descriptions, and receiver state interchange.
*Falsification mode: a second independent implementation cannot reconstruct the receiver's usable world from exported state.*

**T0-APPID. No application identity for capability provision.** `[Structural Commitment]`
A capability provider must not require its own platform application identity in order to provide a capability, unless the capability genuinely requires application-level privilege. Where application identity is required, the requirement is stated and justified by the privilege, never by convenience.
*Falsification mode: adding a capability to the running system requires a new installed package whose privileges the capability does not use.*

**T0-DATED. No policy-specific foundations.** `[Structural Commitment]`
No design may rest on a specific platform policy provision. Structures extracted from platform behavior are permitted; policy specifics carry dates and go stale. A design that breaks when a named policy changes has taken a dependency on a party outside the substrate.
*Falsification mode: a named policy provision is changed hypothetically and a structural commitment of the artifact fails.*

---

## CHILD-SPECIFIC TIER 1

**T1-EXEC. Execution location is a contract.** `[Structural Commitment]`
Provider execution context (remote service, local interpreted module, local model, community attestation, native platform component, human network) is a contract property and never fixed by the function. Location determines who sees inputs, who accumulates residue, what survives provider removal, what can be recomputed, and what scale economies arise, so it carries game-integrity consequences and must be declared per provider.
*Falsification mode: a function statement in this trellis presupposes an execution location.*

**T1-RESID. Residue accrues at the narrowest non-provider locus.** `[Normative Commitment]`
Information generated by exercising a capability accrues at the narrowest locus whose scope matches what was learned: public residue to the shared substrate, receiver-private residue to the receiver, community-scoped residue to the community under its contracts. The provider is never the default custodian.
*Falsification mode: a capability is implemented such that exercising it transfers to the provider information the receiver could have retained.*

**T1-FAIL. Build what fails soonest.** `[Methodological Commitment]`
Among available next steps, prefer the one that produces a disconfirming result earliest and cheapest. The artifact's value to the program is the findings it forces, and a finding arrives only where something can fail.
*Falsification mode: a build increment is undertaken whose failure mode is not stated in advance.*

---

## LINTER

**[LINTER MODE: FLAG-PRIMARY WITH SELECTIVE KILL]** per Operational archetype. Tier 0 violations kill. Everything else flags with a redirect.

### L-A1. The Vertical Integration Creep `[FLAG]`
*Test: is the client absorbing a job that should be a replaceable contract, because implementing it inside is easier this week?*
Redirect: state the contract the client is currently the sole filler of, and record it as an owed seam rather than a completed feature. Every absorbed job is a future capture point in the client itself.

### L-A2. The Convenience Center `[FLAG]`
*Test: is a default becoming structurally necessary? A default provider, a default index, a default relay, a default identity source.*
Redirect: test removal. If removing it breaks unrelated state, it has stopped being a default. Defaults are permitted; irreplaceable defaults are the failure, per the sibling's contestable-focality position.

### L-A3. The Portability Illusion `[KILL]`
*Test: is state exportable but interpretable only by the exporting client?*
Kill under T0-CLIENT. Portability is a property of the receiving end, not the sending end.

### L-A4. The Policy Date `[KILL]`
*Test: does a structural commitment rest on a specific platform policy provision rather than on the structure the provision instantiates?*
Kill under T0-DATED. Restate on the structure or remove the commitment.

### L-A5. The Implementation Carve `[FLAG]`
*Test: is a concept being proposed to the parent because the implementation makes it feel obvious, with no population trace and no T1-ARG discharge?*
Redirect: hold it here as an implementation finding. The parent's question is whether the implementation exposes a missing job or reveals two fused, and neither is answered by the job feeling natural in code.

### L-A6. The Residue Leak `[FLAG]`
*Test: does exercising a capability hand the provider information the receiver could have kept?*
Redirect: state what the provider must see to perform the job, and what it currently sees. The gap is the leak. Note that portability without a retention constraint hands every provider a copy while the architecture calls it custody, which is a legal or cryptographic problem the artifact cannot solve alone.

### L-A7. The Advertised Defense `[FLAG]`
*Test: does a protective capability function only by being legible to the adversary, such that deterrence requires disclosure and disclosure is the trigger?*
Redirect: separate the capability's operation from its announcement, and decide each independently. Two known instances: self-propagation deters removal only if the platform knows the software survives removal; aggressive identity resistance advertises that identity is load-bearing. Held in the parent library with an obligation, no tier standing.

---

## GATE CANDIDATES

No gate designated at spawn. The first Shore selects one or records why the trellis proceeds without.

**GC-1. Referent stability.** Do the objects people actually encounter carry stable enough referent for structure to attach? Personalized feeds, ephemeral content, and A/B-split delivery mean two receivers instantiate different bytes and neither is wrong. Share links may manufacture stable identity the feed never exposed, which is a capability nobody built for this. This is the sharpest known break in the hypothesis and it is testable in weeks.

**GC-2. Multiplexing.** Can one thin runtime resolve non-package capability contracts on a mainstream device, across enough execution locations for T1-EXEC to be real rather than nominal?

**GC-3. Client independence.** Can a second implementation reconstruct the receiver's world from exported state? Untestable until a second implementation exists, which makes it a late gate and a real one.

---

## DISCHARGE LEDGER

| ID | Statement | Type | Status |
|---|---|---|---|
| A-1 | Referent stability across the encountered object population. See GC-1. | Empirical | Open, testable early |
| A-2 | Share-target interception as the acquisition primitive: receiver-initiated, inside existing applications, requiring no producer cooperation, and emitting a durable reference for objects that lack one. | Empirical | Open, candidate identified |
| A-3 | The receiver state interchange format. Parent S-0a: this is a shared agreement axis among receivers, distinct from the empty producer floor. | Structural | Open, load-bearing for T0-CLIENT |
| A-4 | Provider accountability seam. Provider existence, discoverability, invocability under this client, and invocability under this platform are four distinct capabilities. Network-layer permissionlessness establishes only the first, and a store-distributed client may carry obligations for third-party content reachable through it. Store build and direct build may therefore need different provider policies. | Structural | Open |
| A-5 | Release continuity after loss, compromise, departure, or disagreement involving any original maintainer. The author must not become the irreplaceable trust root. Mechanism deliberately unselected: single key, threshold signers, reproducible-build attestations, pinned maintainers, transparency records, independent build witnesses. Complicated by verification binding signing keys to a registered developer identity. | Structural | Open, mechanism unselected |
| A-6 | Out-of-band reach established while reach exists. The peer graph is the strongest form, and this argument is independent of self-replication. | Structural | Open |
| A-7 | Distribution build variants. The compliant build carries no propagation code and updates through its channel; the direct build carries propagation and updates itself. Precedent exists. Rests on structure, not policy text, per T0-DATED. | Operational | Open |
| A-8 | Whether the deployment ladder's rungs are a set to occupy rather than a sequence to climb, with late-rung sovereignty as the leverage that makes early rungs safe rather than as a destination. | Operational | Open |

---

## EXCLUSION RESERVOIR

Seeded from the parent's retractions where they bind here.

**AR-A01. Canonicalization as a participation floor**
- **Dead Entry:** Requiring all participants to share a canonicalizer so content-addressed identity is universally derivable.
- **Target:** Making objects addressable across parties without agreement.
- **Justifiable Intent:** Shared identity derivation is genuinely required for reference without payload.
- **Killed By:** Construction. A receiver hashing received bytes under its own function, parsing under its own extractor, needs no producer cooperation. The error was importing a waist from a system whose cooperation requirements are inverted: routing requires both parties, reading requires one.
- **Block Scope:** Class Block on all producer-cooperation floors.
- **Structural Residue:** Reference-without-payload is a real capability with a real precondition, and copyright plus dynamic content make it the common mode. Near-universal equilibrium, never a floor.
- **Reactivation Conditions:** An operation is exhibited that fails when payload transmission is available and no contract is shared.
- **Date:** 2026-08-12

**AR-A02. Remote service as the canonical provider form**
- **Dead Entry:** Making network endpoints the standard shape for capability providers, on the argument that services escape the platform application-identity gate.
- **Target:** Provider ecosystems that do not inherit a platform's identity gate.
- **Justifiable Intent:** The gate is real, and escaping it is necessary.
- **Killed By:** T0-FS inherited. The job is providing a capability without acquiring application identity; remote service is one contract for that job. Promoting it sacrifices local privacy, offline operation, receiver-local recomputation, cheap switching, and capabilities needing private receiver state. It also places the provider inside the learning loop by construction.
- **Block Scope:** Point Block. The contract remains available and important.
- **Structural Residue:** T1-EXEC. Execution location as a declared contract property with game-integrity consequences.
- **Reactivation Conditions:** All non-remote execution contracts are shown unworkable on target devices.
- **Date:** 2026-08-12

---

## SHORE PROTOCOL

**Cadence:** Event-driven, plus mandatory Shore at each build increment that produced a disconfirming result.

**Trigger events:**
1. An object class resists instantiation.
2. A capability slot is needed and cannot be filled without violating a Tier 0 constraint.
3. A concept feels obvious in implementation and has no population trace.
4. A platform behavior changes such that a design assumption requires restatement.
5. A sibling finding contradicts a commitment here.
6. A build increment produces its stated failure mode.

**Steps:**
1. Restate the failure without remedy.
2. Classify: missing capability, wrong tier constraint, or implementation error.
3. Check against T0-DATED: does the repair take a dependency on a party outside the substrate?
4. Check against L-A5: is this a finding for the parent or a convenience for the build?
5. Amend, and record which of Tier 0, Tier 1, Linter, or Ledger moved.
6. Propagate to sibling and parent, stating which entries are touched.

---

## CORPUS INDEX

| ID | Document | Role |
|---|---|---|
| CA-01 | Parent trellis v1.4 | Inherited constraints and resolutions. |
| CA-02 | Sibling: Capture Dynamics trellis | Supplies constraints this trellis must satisfy. |
| CA-03 | AVF EpiStack kernel and Knowledge Game | Prior implementation. Interaction primitives and the kernel whose binary must not become the waist, per T0-CLIENT. |
| CA-04 | Platform distribution and verification policy, 2026 | Structure extracted, specifics dated. Under T0-DATED, cited for structure only. |
| CA-05 | Adversarial exchange on the receiver-substrate hypothesis | Origin of T0-PROD, T0-CLIENT, T0-APPID, T1-EXEC, T1-RESID. Partial source independence: one author, two model instances. |

---

*Trellis Document. Version 0.1. Spawned at parent v1.4.*
*Next Shore: Gate selection, or first disconfirming build result, whichever arrives first.*
