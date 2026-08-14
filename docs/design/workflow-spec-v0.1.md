---
Type: design
Purpose: "Licensing segmented by capture risk, repository layout, and the design-build-measure-verify-shore loop."
Depends on: [docs/document-style-guide.md]
Depended on by: [docs/corpus-index.md]
---

# TRELLIS: WORKFLOW SPECIFICATION

**From design through repository to recalibration**
v0.1 · 13 August 2026

---

## 1. Licensing, segmented by capture risk

The current EpiStack repository is AGPL-3.0, which makes it the least composable entry in a field about composition. Fifteen of twenty-two public repositories carry no license file, five are MIT, one is GPL-3.0, and one is AGPL-3.0. That asymmetry is worth fixing deliberately rather than by picking a single license for everything.

One license across the whole repository is wrong because the layers have opposite failure modes. A closed spec kills the waist. An openly-licensed hosted service invites a provider to fork, host, improve, and publish nothing.

| Layer | License | Reason |
|---|---|---|
| `spec/` | **CC0** | A format nobody can freely implement is not a waist. Zero friction, including for hostile implementers. |
| `kernel/` | **Apache-2.0** | Embeddable anywhere, and the explicit patent grant matters for something intended as infrastructure. MIT lacks it. |
| `functions/` | **per function, author's choice** | The loader imposes nothing. A function is a separate work. |
| `probe/` | **Apache-2.0** | Measurement instrument, meant to be run and modified by anyone. |
| `app/` | **AGPL-3.0** | The layer where a provider could host a closed fork. Network copyleft forces publication. |
| `fixtures/` | **CC-BY-4.0** | Data wants maximum reuse with attribution. |
| `trellises/`, `docs/` | **CC-BY-SA-4.0** | Methodology should propagate and stay open. |

The rule underneath: **license each layer against its own capture risk.** The waist gets the freest license because closing it is the worst outcome. The hosted layer gets the strongest copyleft because a closed hosted fork is the worst outcome there.

### The loader's licensing property

Running a function as a subprocess over stdin and stdout creates no linking and no derivative-work relationship. The loader can run GPL, MIT, proprietary, and unlicensed functions side by side without any of them contaminating each other or the kernel.

This was chosen for other reasons and it turns out to be the licensing answer too. Any design where functions link into the host process would force a single license across the whole function ecosystem, which is exactly the ontological hegemony the architecture refuses.

---

## 2. Repository layout

One repository initially. Discovery matters more than purity at n=1, and the structure below splits cleanly along license boundaries when it needs to.

```
trellis/
  README.md
  LICENSE-CC0.txt  LICENSE-APACHE.txt  LICENSE-AGPL.txt  LICENSE-CC-BY.txt

  spec/                       CC0
    journal.md                event types, append-only discipline
    function.md               stdin/stdout contract, hashing, discovery
    bundle.md                 what travels between parties
    referent.md               normalization rules for the join key

  kernel/                     Apache-2.0
    canonical.mjs             normalization and hashing
    loader.mjs                function discovery and invocation
    journal.mjs               append, read, never rewrite

  functions/                  per-function LICENSE, required
    report/       report.py       LICENSE  README.md
    bundle/       bundle.py       LICENSE  README.md
    join/         join.py         LICENSE  README.md
    recent/       recent.py       LICENSE  README.md

  probe/                      Apache-2.0
    probe.py                  capture, referent resolution, archive consent
    MANUAL.md

  fixtures/                   CC-BY-4.0
    synthetic/                hand-built journals covering each verdict
    cases/                    the three competition cases, if built

  trellises/                  CC-BY-SA-4.0
    parent-decomposition.md
    child-receiver-substrate.md
    child-capture-dynamics.md
    phone.md

  docs/                       CC-BY-SA-4.0
    design/                   pocket, workflow, syntheses
    findings/                 what the probe established, with dates

  scripts/                    Apache-2.0
    verify-docs.mjs           recompute every number in docs from fixtures
    verify-ledger.mjs         every sorry has a status, every built claim a check
    verify-functions.mjs      every function runs against fixtures
    verify-license.mjs        every function directory has a LICENSE
    verify-privacy.mjs        no real journal data anywhere in the tree
    shore-report.mjs          what changed, which sorries are touched

  .github/workflows/verify.yml
```

### Naming convention for entrypoints

Following the clearest pattern in the population: **entrypoints are named for the act, not the code.** Reading the target list should tell someone what the project claims and how it checks itself.

```
verify:docs        verify:ledger      verify:functions
verify:license     verify:privacy     verify:all
probe:capture      probe:report       probe:bundle       probe:join
shore:report
audit:self         run the loader's own functions against the loader's own journal
```

`audit:self` is not decoration. It is the tool applied to itself, and it is the cheapest available check that the abstraction holds.

---

## 3. The privacy gate

This is the one that cannot be added later.

The journal contains real reading history, share links carrying access capabilities, and referents to private documents. `verify:privacy` runs as a pre-commit hook and as the first CI job, and fails on:

- any file under `~/trellis-probe` paths or matching `journal-*`, `findings-*`, `report-*`
- any `claude.ai/share/`, Google Docs `/d/`, or `/s/` shortlink pattern in a committed file
- any fixture whose events lack a `synthetic: true` marker

Fixtures are hand-built or generated, never harvested from a real journal. A real export used once as a convenient test case is a permanent leak, because git history is not deletable in practice.

---

## 4. The workflow loop

Five stages, each with an artifact and a check. The loop is the point; no stage is a milestone.

```
   TRELLIS ────────► FUNCTION ────────► JOURNAL
   design            build              measure
      ▲                                    │
      │                                    ▼
   SHORE ◄──────────────────────────── VERIFY
   recalibrate                         check
```

**Design.** A job is stated in a trellis as a sorry: what it does, what its absence costs, direction of error, what would falsify it. Nothing is built from a job that has not been written down this way, because the falsifier is what makes the build informative.

**Build.** A function is written as a script over journal events. It gets a directory, a LICENSE, a README naming the job it fills, and a fixture it runs against. Its identity is the hash of its file.

**Measure.** The function runs against real use and appends to the journal. The journal is append-only and never rewritten, so a superseded finding stays visible beside its replacement.

**Verify.** The checks run. Every number in every document recomputes from fixtures. Every function executes. Every claim marked built has a check that proves it.

**Shore.** `shore:report` lists what changed since the last shore and which sorries the changes touch. The trellis is amended, the amendment is recorded with its date and its trigger, and the loop restarts.

### The rule that makes recalibration honest

**A finding may kill a design; a design may not suppress a finding.**

The probe has already overturned the first gate of the receiver-substrate child, two of my confident claims, and one of the design's central assumptions, inside a day. That is the loop working. It only keeps working if the trellis updates when the artifact contradicts it, rather than the artifact being adjusted to preserve the trellis.

`verify:docs` enforces part of this mechanically. It reads typed headers and checks the dependency graph in both directions, and it does not read cited figures at all, which the script says in its own closing output. Documents citing n=9 while the probe holds thirteen encountered objects across ten producers is drift, and it happened within one day of the document being written, and no check has caught it since. The same document also lists TikTok and Google Docs as absent from the corpus while the finding records both as measured, which is a stale coverage claim rather than only a stale number and reads as honesty rather than error. A check that recomputes cited numbers from fixtures would catch the first without anyone remembering to look. Nothing yet proposed catches the second.

---

## 5. What the first cycle looks like

Ordered by which step produces a disconfirming result soonest.

1. **Repository initialized** with the license segmentation, the privacy gate, and CI running `verify:privacy` and `verify:license` only. Both pass trivially and both fail loudly later, which is the point.
2. **The probe moves in**, with its history starting properly instead of accumulating as untracked copies in a downloads folder.
3. **The loader is built**, and `report`, `bundle`, `join`, `recent` become the first four functions. This is the refactor that tests the loader against real cases before anyone else writes one.
4. **Fixtures** covering each verdict, synthetic and marked as such.
5. **`verify:docs`** wired to the trellises and design documents. It will fail on first run, which is the finding.
6. **`audit:self`**: the loader runs its own functions over its own journal.
7. **Shore** on the parent and both children, against what steps 1 through 6 actually established rather than against intention.

The one thing to resist through all of it: writing more synthesis. The gap between what the documents describe and what runs is currently the widest it has been, and closing it slightly is worth more than describing it better.

---

## 6. What is deliberately not decided here

**Function distribution.** Local loading only. The moment functions travel between people, a contract vocabulary becomes unavoidable, and that vocabulary should be learned from the functions people actually write rather than designed in advance.

**Registry format.** Follows distribution.

**The self-governance tier.** The phone trellis governs an operator's policy over their own device, and the register's participant tier is entirely about other people. That is probably a sixth tier and it is optional, so it waits for the shore in step 7.

**Multi-repository split.** The layout above splits cleanly when there is a reason. There is not one yet.
