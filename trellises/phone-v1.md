# PERSONAL DEVICE TRELLIS: PHONE

**Archetype:** Self-Governance (proposed new archetype), Engineering-secondary
**Domain:** Configuration, modification, and operational policy of one rooted Android phone, tracked across its lifecycle, with the trajectory of becoming a voice-first AI-assisted personal device.
**Status:** Active. Awaiting first modification or use-case Shore.

---

> **Operational Intent.** This trellis is the shared memory of a recursive coupling between operator and personal device. The phone is rooted, custom, and undergoing continuous modification toward a voice-primary AI-assistant configuration. The trellis exists because that trajectory cannot survive without persistent organization: every mod, every app, every use-case decision is otherwise lost to time, distraction, or accidental rollback. Decisions that capture attention against reflective interest are killed. Decisions that risk the substrate (loss of device, data, or root) are killed. Decisions that are merely suboptimal organization are redirected toward better-fit alternatives rather than rejected. The trellis logs everything, kills the unsafe, and proposes redirects for the rest.

## JURISDICTIONAL BOUNDARY

This trellis addresses the configuration, modification, and use-case policy of one specific rooted Android phone. It does not address:

- Personal devices other than this phone (laptop, tablet, watch). A sibling trellis can be spawned later under a Personal-Devices parent if the pattern stabilizes.
- Cloud-side services or accounts considered as systems in their own right. Account hygiene is in scope only insofar as it touches the phone.
- Specification of the larger Personal COS architecture. That work is upstream and referenced via Corpus Index.
- The user's broader research program on the COS / CK / Viable Fork. The phone is one node; the federation lives elsewhere.

These are legitimate questions. They require different infrastructure.

---

## STRATIFIED AXIOMATIC CORE

### Tier 0: Hard Floor (Absolute, Non-Negotiable)

**T0-AS, Attention Sovereignty.** [Value Commitment] The phone serves Function E. Configurations, apps, notification policies, or mods that steer attention toward proxy goals (engagement metrics, third-party objectives) at the cost of stated user intent are killed or redirected. *Falsification mode: a mod or app demonstrably steers attention toward proxy goals at the cost of stated user intent.*

**T0-SP, Substrate Preservation.** [Empirical Commitment] Modifications preserve the device, root state, and irreplaceable data. Failure modes that include loss of any of these require a documented and tested rollback before approval. *Falsification mode: a proposed modification touches /system, /vendor, /boot, recovery, modem, or bootloader without a rollback procedure verified to work on this hardware revision.*

**T0-KP, Knowledge Persistence.** [Methodological Commitment] Every modification, app install, and configuration change is logged in this trellis or a referenced sub-document before activation. State that is not recorded is treated as drift; the next Shore will surface it for either reconciliation or removal. *Falsification mode: actual phone state diverges from recorded state by more than a known-and-accepted delta.*

**T0-AP, Anti-Panopticon.** [Value Commitment] Installed components serve the operator. Any component that surveils the operator against reflective interest, regardless of vendor reputation or feature convenience, is killed. The post-root state exists precisely so this commitment can be enforced. *Falsification mode: a component is shown to phone-home, log behavior, or reactivate vendor surveillance without explicit operator consent.*

### Tier 1: Architecture (Translation Layer)

**T1-UC, Use-Case Partitioning.** [Methodological Commitment] The phone is operated as a small set of named use-cases, each with its own active policy: visible apps, launchable apps, permitted notifications, home screen / launcher state, assistant behavior, voice/screen ratio target, exit conditions. Use-cases are the canonical organizational unit. The default state is a use-case; there is no "no use-case" state. *Falsification mode: an interaction or app installation cannot be assigned to any defined use-case and the operator cannot articulate which use-case is active.*

**T1-VP, Voice Primacy as Telos.** [Value Commitment] The phone's evolution heads toward voice-first interaction. Modifications, app choices, and assistant configurations are evaluated, in part, against this trajectory. A mod that pulls toward screen-primacy is permitted only with explicit justification (e.g., a use-case where voice fails). The telos is revisable via full Shore but not via drift. *Falsification mode: cumulative direction of modifications over time shows screen-time growing rather than shrinking, with no explicit operator commitment to that direction.*

**T1-RV, Reversibility by Default.** [Methodological Commitment] Modifications are reversible unless explicitly tagged as one-way. One-way mods require a separate justification and a record of the optionality being given up. Soft mods (Magisk modules, app-level config, Tasker scripts) are preferred over hard mods (custom ROM flashes, recovery changes) when they accomplish the same goal. *Falsification mode: a one-way modification was performed without the explicit one-way tag and rationale being recorded first.*

### Tier 2: Methodology

**T2-MP, Modification Protocol.** [Methodological Commitment] Every modification follows a fixed six-step protocol: state intent, record before-state (versions, hashes, configs), specify rollback, perform change, verify after-state, log it. A change without all six steps is unfinished. *Falsification mode: a mod is in production whose log is missing rollback or after-state.*

**T2-AA, Attention Audit.** [Methodological Commitment] At each Shore cadence, the active app set is reviewed against actual usage. Apps installed-but-unused, or whose use does not map to any use-case, become candidates for removal. *Falsification mode: an app remains on the phone for more than one Shore cycle without a defined use-case and is defended on inertia alone.*

**T2-DD, Drift Detection.** [Methodological Commitment] Recorded state and actual state are compared periodically. Divergence is either accepted (logged, absorbed into recorded state) or remediated. Accumulated unaddressed drift across Shore cycles is itself a Tier 1 pressure signal. *Falsification mode: drift accumulates across Shore cycles without being addressed.*

---

## LINTER

**[LINTER MODE: MIXED]** This trellis uses kill-mode for substrate-violating or attention-capturing actions and redirect-mode for organizational and optimization decisions. Most failures produce redirects. A small set of failures produces hard kills.

**Linter evolution via post-mortem.** Linter rules are retrospectively generated from post-mortems of significant failures. After resolving a major failure (a brick, a distraction relapse, a config-loss event), ask: what structural blindness allowed this? Each class-block kill in the Exclusion Reservoir is a candidate for a new Linter rule.

### Universal Entries

**The Unmapped Mod.** [KILL MODE] *Test: a proposed modification has no clear mapping to any Tier 0 floor or Tier 1 architecture commitment.* Remediation: the mod cannot proceed until the operator articulates which architecture commitment it serves. Lacking that, the mod is rejected.

**The False Isomorphism.** [KILL MODE] *Test: a justification claims that some other phone-mod community / configuration "works the same way" without checking whether the structural correspondence holds for this device, this root state, this use-case set.* Remediation: kill the cargo-cult mod. Demand a check on this hardware before re-proposing.

**The Naked Spec.** [FLAG MODE] *Test: an entry uses Magisk / Xposed / Android-internals vocabulary without translating to use-case-level intent.* Remediation: flag for translation. The trellis is read by Function E, not by the kernel.

### Domain-Specific Entries

**The Distraction Trap.** [KILL MODE] *Test: a proposed app, widget, notification policy, or home-screen change has any of: infinite-feed UI, unbounded notification class, default-allowed background activity that does not serve a stated use-case.* Remediation: killed. The operator may propose a redirected version with explicit attention-floor protection (notifications off, scheduled access only, home-screen exclusion, etc.).

**The Disorganization Drift.** [REDIRECT MODE] *Test: a proposed install or config change has no entry in the modification log being prepared, no defined use-case, or no rollback. Or: the operator reaches for the phone and cannot articulate which use-case they are entering.* Remediation: redirect the operator to define use-case and complete the log entry before the action lands. The action itself is not rejected; it cannot reach production state without the entry.

**The Brick Trap.** [KILL MODE] *Test: a modification touches /system, /vendor, /boot, recovery, modem, or bootloader without a verified rollback tested on a backup state of this same device, OR proposes an OTA-blocking change without explicit recognition of the security-update tradeoff.* Remediation: killed until the rollback is verified or the tradeoff is explicitly accepted in the log.

**The Vendor Capture Trap.** [KILL MODE] *Test: a re-installation or update reintroduces a Google / OEM / operator service that was previously deliberately removed, OR a proposed convenience feature requires re-enabling a surveillance vector that the rooted state was meant to remove.* Remediation: killed. Convenience does not override Anti-Panopticon. If the operator wants the convenience, the relevant Tier 0 commitment must be revisited at full Shore.

**The Lock-In Trap.** [FLAG MODE] *Test: a proposed mod constrains the future modification space, removes optionality, prevents ROM updates, or hard-codes a configuration costly to reverse.* Remediation: flagged. Operator must explicitly tag the mod as one-way and record what optionality is being given up before proceeding.

**The Mode Confusion.** [REDIRECT MODE] *Test: an active app or notification belongs to a use-case other than the one currently active, and is permitted to interrupt.* Remediation: redirect to the use-case policy. If the policy needs to permit this interruption class, that policy update is itself a mod and follows the modification protocol.

**The Telos Drift.** [FLAG MODE] *Test: cumulative modifications over a time window pull away from voice-primary interaction, with no explicit operator commitment to the screen-primary direction.* Remediation: flag at next Shore. Either commit explicitly to the new direction (revising T1-VP via full Shore) or reverse the drift.

---

## EXCLUSION RESERVOIR (ARCHIVE OF CONDITIONAL VIABILITY)

No entries yet. First entries populated after the first modification kill or first failure post-mortem.

**Entry template:**

**[ENTRY ID]. [Short descriptive name]**
- **Dead Entry:** [What was attempted]
- **Target Domain / Target Sorry:** [What it was aimed at]
- **Justifiable Intent:** [Why it seemed promising; the surviving goal]
- **Killed By:** [Specific element: tier constraint, Linter rule, empirical result]
- **Block Scope:** Point Block (this specific approach) or Class Block (entire family)
- **Structural Residue:** [What survives and remains reusable]
- **Reactivation Conditions:** [Specific, testable conditions]
- **Trellis Version at Block:** v[X.Y]
- **Date:** [Date]

---

## DISCHARGE LEDGER (SORRY LEDGER)

**Gate sorry:** S-UC-001. Without a crystallized use-case partition, all organizational structure on the phone is downstream of an undefined taxonomy. Every other sorry traces relevance to this one.

**Classification taxonomy:**
- **Resolvable:** Known path exists, execution pending.
- **Frontier:** Requires new conceptual or design work.
- **Blocked:** Dependency prevents discharge.

**Difficulty taxonomy:** LOW, MODERATE, HIGH, CRITICAL BOTTLENECK, FRONTIER.

| Sorry ID | Obligation | Classification | Difficulty | Dependencies | Deliverable | Status |
|---|---|---|---|---|---|---|
| S-UC-001 | Define the canonical use-case partition. Each use-case carries: name, purpose, active app set, notification policy, launcher / home-screen state, voice/screen ratio target, exit conditions. | Resolvable | CRITICAL BOTTLENECK | None | Use-case registry document referenced from Corpus Index. | Open |
| S-VP-001 | Specify the voice-first interaction architecture target: which assistant, which voice command surface (Tasker / custom / vendor), which fallbacks, which use-cases are voice-primary versus voice-supplementary. | Frontier | HIGH | S-UC-001 | Voice architecture spec. | Open |
| S-MOD-001 | Build the canonical modification log. Every existing root-level mod, Magisk module, system app removal, and significant config currently in production is recorded with rollback information. | Resolvable | HIGH | None (parallel to S-UC-001) | Modification log document with current-state snapshot. | Open |
| S-PAN-001 | Audit the current installed base for vendor capture vectors. Identify any reintroduced surveillance components and decide explicitly: keep with acknowledged tradeoff, remove, or replace. | Resolvable | MODERATE | S-MOD-001 | Audit findings with disposition per item. | Open |
| S-ALG-001 | Define operator-specific Algedonic Override thresholds: minutes-of-unintentional-use trigger, anxiety markers, sleep-degradation markers, in-person-interaction markers. | Resolvable | MODERATE | None | Threshold spec inserted into Shore Protocol. | Open |

---

## SHORE PROTOCOL

**Cadence.** Sub-element Shore on per-modification or per-event basis. Full Shore on architectural events (Tier 1 revision, archetype reconsideration, use-case partition restructuring).

**Trigger events.**

- A modification is proposed or installed (root-level, app, system config).
- A use-case is added, removed, or redefined.
- A failure occurs: brick, near-brick, root loss, data loss, attention-capture event the operator notices, distraction relapse.
- The operator reaches for the phone and cannot articulate the active use-case.
- A new sorry is opened or discharged.
- A literature-frontier event: new ROM, new Magisk-class capability, new vendor change, new attention-management or voice-assistant tool that materially changes the design space.

**Shore steps (in order):**

1. Update the Modification Log first. New intelligence is perishable.
2. Update the Exclusion Reservoir if anything was killed.
3. Query the Reservoir against revised state for reactivation candidates.
4. Check Linter pressure: is any rule firing repeatedly? If yes, candidate for promotion to Tier 0 or refinement of the rule.
5. Check Tier 1 under pressure: is any architecture commitment getting strained by accumulated mods?
6. Drift check: does recorded state match actual state?
7. Full Trellis Shore (separate cadence; requires explicit operator commitment).

### Algedonic Override

**Purpose.** Substrate-protection bypass of standard Shore. Triggered when biophysical or attentional viability is breached.

**Trigger conditions** (specifics to be fixed by S-ALG-001):

- Operator notices distraction relapse exceeding personal threshold.
- Operator notices anxiety, attention fragmentation, or compulsive use centered on the phone.
- A specific use-case has degraded into doom-scroll or its analog.
- Sleep, presence, or in-person interaction quality measurably suffers due to phone use.

**Protocol on trigger:**

1. All non-essential use-cases are suspended. The phone reverts to a minimal use-case (calls, navigation, emergency only) until reset.
2. The triggering pattern is logged as a candidate Exclusion Reservoir entry.
3. A Linter rule update is drafted: what would have caught this earlier?
4. Standard Shore is deferred until the substrate is recovered.

This override can be invoked by Function E at will. It is the operator's kill switch on the entire system.

---

## SHORE RECORD

| Date | Trigger Event | Modification Log Updated | Reservoir Updated | Discharge Ledger Updated | Tier Pressure | Full Shore? |
|---|---|---|---|---|---|---|
| 2026-04-27 | Trellis creation | Empty (S-MOD-001 open) | No entries | Gate sorry S-UC-001 initialized; S-VP-001, S-MOD-001, S-PAN-001, S-ALG-001 seeded | None | No |

---

## CORPUS INDEX

| ID | Title | Section Relation | Date | Notes |
|---|---|---|---|---|
| C-001 | Personal_COS_Implementation_Guide.pdf | Source for: Anti-Panopticon, Function E framing, Algedonic Override, Intent Verification, Touch Grass principle. | 2026-04-27 | Macro-COS guide. Operational vocabulary transplanted; software/server architecture not. |
| C-002 | COS_Software_Architecture_Blueprint_v0_1.pdf | Source for: Solvency Gate concept (attention-budget analog), Ambient Chaos Principle, Is-Ought separation as design pattern. | 2026-04-27 | Blueprint not adopted as stack; concepts adopted as principles. |

---

## NOTES ON ARCHETYPE: SELF-GOVERNANCE (CANDIDATE)

This trellis introduces a candidate seventh archetype: **Self-Governance**. Defining features:

- Trellis operator and protected substrate are the same agent. Function E is both the source of normative authority and the body whose attention, time, and cognitive integrity the trellis protects.
- The artifact under construction (here, the phone) is a recursive instrument: the operator shapes the artifact, and the artifact shapes the operator's interaction with the world. The substrate-coupling is bidirectional.
- The Linter operates in mixed mode by default: kill-mode for substrate-threatening or attention-capturing actions, redirect-mode for optimization and organization decisions.
- The kernel includes an Algedonic Override authorizing Function E to bypass standard Shore when substrate breach is detected.
- Standard Tier 0 commitments include Substrate Preservation, Attention Sovereignty, Knowledge Persistence, and Anti-Panopticon as a default set, adapted per substrate.

Promotion to the Meta-Trellis is conditional on this archetype proving stable across at least two instantiations. A second instance (laptop, personal information environment, or another device) under the same archetype would constitute the second data point.

---

*End of Trellis Document. Version 1.0. Initialized at first phone trellis creation.*
*Next Shore: Triggered on first modification, first use-case definition, or first failure event.*
