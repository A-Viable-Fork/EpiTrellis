---
Type: specification
Purpose: "The function calling convention: an executable over stdin and stdout, identified by the hash of its file, discovered by presence."
Depends on: []
Depended on by: [README.md, CLAUDE.md, docs/corpus-index.md]
---

# The Function Contract

**License: CC0-1.0.** This is the waist. A format nobody can freely implement is not a waist.

---

## The whole thing

A function is an executable file. It reads newline-delimited JSON on stdin and writes newline-delimited JSON on stdout. Its identity is the SHA-256 of the file.

That is the contract. Everything below is consequence.

## Invocation

```
<executable> [args...] < events.ndjson > output.ndjson
```

The loader discovers functions by presence in a directory, not by registration. A directory containing an executable named `run` is a function. Its name is the directory name. Its identity is `sha256(run)`.

Exit status zero means the function completed. Non-zero means it did not, and its stdout is discarded.

## Input

Each line is one JSON object. The loader supplies the journal, or a filtered view of it, in the order the events were appended. A function that needs no input receives an empty stream and must tolerate it.

Functions must tolerate unknown fields and unknown event types. A function that fails on an event it does not recognize is broken, because the journal grows and functions do not update in lockstep.

## Output

Each line is one JSON object. A function that emits nothing is valid.

Output lines the loader appends to the journal must carry `"event"`. Output lines without `"event"` are treated as display and are not persisted.

## Identity

`sha256(run)` in lowercase hex. Any change to the file is a different function.

This is fork discipline, and it is deliberate. There is no same-function-different-version, because compression is total. Continuity across revisions, where it is wanted, comes from the version control system carrying the file, not from the identity of the file.

## What this contract does not specify

Deliberately, and each omission is load-bearing.

**Language.** Any executable.

**Manifest.** What a function declares about itself is a separate, forkable vocabulary. See `vocabulary.md`. A function with no manifest is valid and unlocks nothing that a manifest would unlock.

**Capability declaration.** Any sandbox is applied by the loader from outside. A declaration the loader enforces is true regardless of the author's honesty; a declaration nobody enforces is a producer assertion and worth nothing.

**Semantics.** Nothing here says a function does its job correctly. That is scrutiny, and scrutiny is not a format problem.

## Why subprocess

Two reasons, and the second was not the original one.

Isolation: a function that crashes, hangs, or misbehaves cannot corrupt the loader or another function.

Licensing: running a program as a subprocess creates no linking and no derivative-work relationship. GPL, MIT, proprietary, and unlicensed functions run side by side without contaminating each other or the host. Any design where functions link into the host process forces a single license across the whole ecosystem, which is the ontological hegemony this architecture exists to refuse.

## Purity, declared and unenforced

A function may be pure, deterministic, and total: same input, same output, no network, no clock, no filesystem beyond stdin and stdout. Such a function is **reproducible**, meaning anyone runs it and gets the identical answer while trusting nobody.

Most useful functions are not pure. One that fetches a URL or calls a model is **attested** at best: you can audit its code and not its inputs.

Purity is therefore a property that unlocks reproducibility, never a requirement. Requiring it would leave almost nothing.

## Type signatures

The cheapest useful thing a function can say about itself: which event types it consumes and which it emits. Mechanically checkable, no formalism commitment, and it is most of what a manifest needs.

A function that declares its signature unlocks composition checking, which is a loader knowing that A's output can feed B's input before running either. A function that declares nothing still runs.
