---
Type: specification
Purpose: "Standing rules binding on anyone or anything editing this repository, including the privacy gate, the append-only discipline, and what is deliberately deferred."
Depends on: [spec/function.md, docs/document-style-guide.md]
Depended on by: []
---

# CLAUDE.md

Standing context for Claude Code. Read this before touching anything.

## What this is

A receiver-owned substrate for things you encounter. Objects are addressed locally with no cooperation from whoever published them. Functions are executables that do something useful with those objects. Nothing is required; filling a function unlocks a capability and leaving it empty costs that capability and nothing else.

## Hard rules

**Never commit real capture data.** The journal holds reading history and URLs that carry access rather than merely address: `claude.ai/share/`, Google Docs `/d/` ids, Reddit `/s/` shortlinks, tokens in query strings. Git history is not deletable in practice, so one real export used once as a convenient fixture is permanent. Fixtures are generated and carry `"synthetic": true`. `scripts/verify-privacy.py` enforces this and runs first in CI. Do not weaken it to make a test pass.

**The journal is append-only, with one named exception.** Never rewrite, never delete, never reorder. A superseded finding stays visible beside its replacement. Several findings in the corpus are wrong and preserved on purpose, because the record of having been wrong is part of the evidence.

The exception is `probe.py purge`, added 2026-08-15, and it is the only code anywhere permitted to remove a row. It exists because an unlisted link is a capability rather than an address, so a journal holding one is the disclosure and excluding it from exports does not undo that. It deletes rows for named captures, appends a record saying a rewrite happened and how many rows went without saying what they were, requires a typed confirmation, and refuses to run non-interactively. The guarantee it preserves is not that nothing is removed but that nothing is removed without saying so. Do not add a second exception; extend that one or leave the rows alone. See entry 8a of `docs/compost-ledger.md`.

**Functions must tolerate unknown event types.** The journal grows and functions do not update in lockstep. A function that crashes on an event it does not recognize is broken. `verify-functions.py` tests this by feeding every function a synthetic unknown event.

**Do not add a manifest format, a registry, or a function vocabulary.** These are deliberately deferred. What a function should declare about itself will be learned from the functions people write, not designed in advance. If a task seems to require one, say so and stop rather than inventing one.

**Do not add dependencies.** Python standard library only, in the kernel, the functions, the probe, and the scripts. The probe runs in Termux on a phone, and every dependency is a reason it stops running there.

## The rule the project runs on

**A finding may kill a design; a design may not suppress a finding.**

The measuring instrument has already overturned the first gate of one research trellis, two confident claims, and one central design assumption. When the artifact contradicts a document, the document is wrong. Update it, keep the old claim visible with its date, and record what overturned it.

## Layout and licensing

Licensing is segmented by capture risk, not chosen once.

| Path | License | Why |
|---|---|---|
| `spec/` | CC0 | A format nobody can freely implement is not a waist |
| `kernel/`, `scripts/`, `probe/` | Apache-2.0 | Embeddable, with a patent grant |
| `functions/*/` | author's choice | A function is a separate work; the loader imposes nothing |
| `fixtures/` | CC-BY-4.0 | Data wants reuse with attribution |
| `trellises/`, `docs/` | CC-BY-SA-4.0 | Methodology should propagate and stay open |
| `app/` when it exists | AGPL-3.0 | The layer where a provider could host a closed fork |

Root `LICENSE` is Apache-2.0 and covers anything not otherwise marked. Every new function directory needs its own `LICENSE`; `verify-license.py` fails without it.

## The function contract

An executable named `run`, reading newline-delimited JSON on stdin, writing newline-delimited JSON on stdout. Identity is `sha256(run)`. Discovery is by presence in a directory. Full spec in `spec/function.md`.

Subprocess isolation is also the licensing answer: no linking, no derivative work, so GPL and MIT and proprietary functions coexist. Never change this to in-process loading.

## Checks

```sh
python3 scripts/verify-privacy.py           # first, always
for f in scripts/verify-*.py; do python3 "$f" || break; done
```

Every check in `scripts/` must pass before any commit. Privacy runs first because nothing else matters if real capture data has entered the tree.

This section names no count and lists no inventory on purpose. `scripts/` is the authority for which checks exist, and a copy of that list kept here went stale twice: once saying three after a fourth landed, and once asserting in the same document that `verify-docs.py` was required and that it did not exist. See entry 10 of `docs/compost-ledger.md`.

Privacy and functions each caught a real problem on their first run, which is the only reason to trust either.

## Naming

Entrypoints are named for the act, not the code. Reading the list of targets should tell someone what the project claims and how it checks itself. `verify:privacy`, `probe:capture`, `audit:self`.

## What is unfinished, deliberately

- Recomputing every number cited in `docs/` and `trellises/` from fixtures, so documents cannot drift from artifacts. `scripts/verify-docs.py` reads typed headers and dependency reciprocity and does not read cited figures, which it says in its own output. Number checking needs a findings pipeline nobody has built.
- Function distribution, registries, manifests. Local loading only for now.
- The self-governance tier: an operator's policy over their own device. Probably a sixth tier in the decomposition, currently unrecorded.

## Style

Prose over bullets in documents. No em dashes. Say what something is rather than what it is not. When something is dead, say it is dead; the credibility of every claim that works rests on the honesty of every claim that does not.
