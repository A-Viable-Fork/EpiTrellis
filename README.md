# Epitrellis

Your phone's apps each hold your stuff in their own walled garden: your reading, your notes, and what other people thought about the same article all live in separate boxes that don't talk to each other. This turns that around. The things you encounter belong to you, on your own device, and anyone can add a tool that does something useful with them, without needing permission from the app it came from.

The bet is that if that works well enough, the phone stops being a set of apps you visit and starts being something that holds your world.

## Status

Early. One measuring instrument runs, four functions run, three checks pass. Everything else is design.

What has actually been established, as of August 2026:

- **Referents are stable.** Across thirteen objects encountered in ordinary reading, every one produced a resolvable, normalized address derived locally with no cooperation from the producer. LessWrong, Substack, arXiv, X, Google Docs, YouTube, TikTok, Reddit. This was the thing most likely to break the whole idea, and it did not.
- **Payload is the real problem, and it splits three ways.** Not text at all (video). Withheld by the producer (Reddit serves a six-character stub, NYT refuses outright, the Internet Archive cannot rescue a paywall). Behind a client-side render.
- **Two parties who never coordinated join by hash.** Independently derived referents match across different URL forms. Set intersection, no agreement required.
- **What travels is small.** Roughly 210 bytes per object. At that size, publishing to five hosts costs nothing, which is why no gradient pulls anyone toward a single one.

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

Licensing is segmented by capture risk. The spec is CC0 because a format nobody can freely implement is not a waist. The application layer, when it exists, is AGPL because that is where a provider could host a closed fork.

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
python3 scripts/verify-privacy.py     # no real capture data in the tree
python3 scripts/verify-license.py     # every function declares one
python3 scripts/verify-functions.py   # every function runs, and tolerates events it does not know
```

Privacy runs first and alone. The journal holds reading history and share links that carry access rather than merely address; git history is not deletable in practice, so one real export used once as a convenient fixture is permanent. Fixtures are generated and carry a `synthetic` marker.

Both checks caught real problems on their first run, which is the only reason to trust either.

## Where this came from

The FLF EpiStack competition, mid-2026. Twenty-two public repositories, built independently, most of which turn out to be components of one thing nobody was coordinating. Sixteen of them shipped with no license at all, which under default copyright makes a field organized around compounding legally uncompoundable.

`trellises/` holds the research structure: what jobs exist, what varies between implementations, and what is still open. `docs/findings/` holds what the instrument has established, with dates.

The rule the whole thing runs on: **a finding may kill a design; a design may not suppress a finding.**
