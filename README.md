---
Type: reference
Purpose: "Entry point. What EpiTrellis is as a design, how its parts fit, and where to find the source of truth for any claim, including what is built and what has been measured."
Depends on: [docs/corpus-index.md, docs/status-ledger.md, docs/findings/probe-referent-stability.md, docs/departure-from-epistack.md, spec/function.md]
Depended on by: []
---

# Epitrellis

Your phone's apps each hold your stuff in their own walled garden: your reading, your notes, and what other people thought about the same article all live in separate boxes that don't talk to each other. This turns that around. The things you encounter belong to you, on your own device, and anyone can add a tool that does something useful with them, without needing permission from the app it came from.

The bet is that if that works well enough, the phone stops being a set of apps you visit and starts being something that holds your world.

EpiTrellis is the substrate for that: a calling convention for functions that read and write a journal of encounters kept on the device, a loader that discovers functions by presence and identifies each by the hash of its file, an instrument that captures what the person meets through the share sheet, and a research structure that names the jobs a federated commons performs and what is still open about each.

The machinery is general. A person's journal is instance data: it lives on their device and never enters this tree, which holds only synthetic fixtures. A function is anyone's executable, dropped into a directory. Swapping either changes what the system knows and does, and leaves the convention as it is.

The state of the system against this design, what runs, what has been measured and what remains open, is in [`docs/status-ledger.md`](docs/status-ledger.md). The calling convention is [`spec/function.md`](spec/function.md); the measurements are in `docs/findings/`, led by [`docs/findings/probe-referent-stability.md`](docs/findings/probe-referent-stability.md); how this grew out of the EpiStack competition field is [`docs/departure-from-epistack.md`](docs/departure-from-epistack.md); [`docs/corpus-index.md`](docs/corpus-index.md) lists every document and what it is for.

## Repository

```
spec/          CC0        the calling convention. The waist.
kernel/        Apache-2.0 the loader: discovery, hashing, invocation
functions/     per-fn     jobs, each an executable over stdin/stdout
probe/         Apache-2.0 the measuring instrument
fixtures/      CC-BY-4.0  synthetic journals. Never harvested.
trellises/     CC-BY-SA   the research structure and its open questions
docs/          CC-BY-SA   design and findings
scripts/       Apache-2.0 the checks
```

Licensing is segmented by capture risk. The spec is CC0 because a format nobody can freely implement is not a waist. An application layer is AGPL, because that is where a provider could host a closed fork.

## Try it

```sh
python3 kernel/loader.py
cat fixtures/synthetic/journal.ndjson | functions/report/run
python3 scripts/verify-functions.py
```

The probe runs on Android under Termux with no app, no signing key, and no store. See `probe/MANUAL.md`.

## A function

An executable that reads newline-delimited JSON on stdin and writes it on stdout. Its identity is the SHA-256 of the file. Discovery is by presence in a directory: there is no registry to petition and no gatekeeper to satisfy.

Nothing is required. Filling a function unlocks a capability, and leaving it empty costs that capability and nothing else. A claim with no type participates fully and grounds nothing.

Subprocess isolation is also the licensing answer: running a program as a subprocess creates no linking and no derivative work, so GPL, MIT, proprietary, and unlicensed functions run side by side without contaminating each other.

## The checks

```sh
python3 scripts/verify-privacy.py           # first, always
for f in scripts/verify-*.py; do python3 "$f" || break; done
```

`scripts/` is the authority for which checks exist; each states what it checks in its own docstring. Between them they keep real capture data out of the tree, require a license per function, run every function against the fixtures (including an event type it does not know), hold every document's typed header and dependency graph consistent, keep vendored foreign code at the bytes it was vendored with, test that paths named in documents agree with the tree, and pin the two deliberate copies of `referent_key` and the capability list to shared fixtures.

Privacy runs first and alone. The journal holds reading history and share links that carry access rather than merely address; git history is not deletable in practice, so one real export used once as a convenient fixture is permanent. Fixtures are generated and carry a `synthetic` marker.

## Findings over design

`trellises/` holds the research structure: what jobs exist, what varies between implementations, and what is still open. `docs/findings/` holds what the instrument has established, with dates.

The rule the whole thing runs on: **a finding may kill a design; a design may not suppress a finding.**
