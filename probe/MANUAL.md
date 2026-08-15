# Referent Stability Probe — Operator Manual

**Version 0.2 · Receiver Substrate Trellis, gate candidate GC-1 / ledger A-1**

---

## What this is testing

One question: **do the objects you actually encounter carry a referent stable enough for structure to attach?**

The receiver-substrate hypothesis says a receiver can locally instantiate anything it encounters with no cooperation from the producer. The producer may be unaware of the substrate, hostile to it, or gone. That claim is either true about the real object population or it isn't, and no amount of architecture settles it.

The known break is the personalized feed. If two people see different bytes at the same nominal location, or if an object emits no durable reference at all, then there is nothing for structure to attach to and the design shrinks. This probe finds out.

**Scope.** This tests instantiation and referent stability only. It tests nothing about crossing, community overlays, capability providers, or residue. Those need more than one party.

---

## What it is deliberately not

It stores no schema. Four event types in an append-only journal: what arrived, what reference it resolved to, what two fetches returned, and what that means. Everything else is derived at read time.

That is not minimalism for its own sake. The receiver interchange format is the single most consequential decision in the whole program, and defining it before there is evidence is exactly the premature compile the trellis exists to prevent. A format that others adopt becomes unkillable by adoption rather than by being right. So: journal now, schema later, once the data says what the schema needs to hold.

---

## Install

### 1. Storage access

```sh
termux-setup-storage
```

Accept the permission dialog. This gives Termux access to `~/storage/downloads`.

### 2. Packages

```sh
pkg update -y && pkg install -y python termux-api
```

`termux-api` is the bridge. The **Termux:API** app must also be installed from the same source as Termux itself (F-Droid Termux needs F-Droid Termux:API). It supplies notifications only. Everything works without it; you just lose the running tally on each capture.

### 3. The probe

```sh
mkdir -p ~/bin
cp ~/storage/downloads/probe.py ~/bin/probe.py
chmod +x ~/bin/probe.py
```

### 4. The share hook

```sh
cat > ~/bin/termux-url-opener <<'HOOK'
#!/data/data/com.termux/files/usr/bin/sh
exec python3 ~/bin/probe.py "$1"
HOOK
chmod +x ~/bin/termux-url-opener
```

`termux-url-opener` is Termux's built-in share receiver. Any URL shared to Termux from any app is passed to it as `$1`. No platform integration, no producer cooperation, no permission beyond the share sheet.

### 5. The drop folder

Sharing a *file* is supposed to reach a second Termux hook, `termux-file-editor`. On some devices Termux ignores it and offers to save the file instead. Rather than fight that, use the save dialog as the capture path.

```sh
mkdir -p ~/storage/downloads/payload
```

This appears in any Android file manager as **Download/payload**. Share a file, choose Termux, save it there. Or move files in with any file manager. Then:

```sh
python3 ~/bin/probe.py scan
```

Everything new gets captured. Dedupe is by content hash, so rescanning costs nothing and the same file saved twice under different names is ignored once. Files are read and left in place; nothing is moved or deleted.

To scan somewhere else instead:

```sh
python3 ~/bin/probe.py scan ~/storage/shared/Documents
```

If the file hook *does* work on your device, it is one line and files capture on share with no scan step:

```sh
printf '#!/data/data/com.termux/files/usr/bin/sh\nexec python3 ~/bin/probe.py file "$1"\n' > ~/bin/termux-file-editor
chmod +x ~/bin/termux-file-editor
```

### 6. Verify

```sh
python3 ~/bin/probe.py "https://arxiv.org/abs/1706.03762"
python3 ~/bin/probe.py report
```

One capture, one finding, and a notification if Termux:API is granted permission.

---

## Daily use

**To capture a link: share.** Read normally in whatever app. When you encounter something, hit the share button, pick Termux. That is the entire interaction. The probe fetches twice, eight seconds apart, and records what differed.

**To capture a file: drop and scan.** Save or move it into `Download/payload`, then run `python3 ~/bin/probe.py scan`. Batch as many as you like; scanning is idempotent.

**To check: the notification.** Every capture ends with a running tally, like `n=47 stable_refer 62% client_rende 21%`. Glance at it. That is the current state of the gate.

**For the full read:**

```sh
python3 ~/bin/probe.py report
python3 ~/bin/probe.py recent
python3 ~/bin/probe.py scan
python3 ~/bin/probe.py export
```

## Getting results out of Termux

```sh
python3 ~/bin/probe.py export
```

Writes three files to **Download/trellis-export/**, readable by any app:

- `report-<stamp>.txt` — the report as text
- `findings-<stamp>.csv` — one row per capture: time, verdict, flags, host, title
- `journal-<stamp>.txt` — a copy of the journal

The journal is written as `.txt` rather than `.ndjson` because many upload and share targets reject unfamiliar extensions. The content is newline-delimited JSON regardless of the name.

Each export retires the previous set into `trellis-export/archive/`, so the top level always holds exactly one current set of three files. Nothing is deleted.

The journal is the artifact. The other two are derived from it and can be regenerated at any time, which is why the copy is the part that matters.

Export also opens the Android share sheet with the report, so it can go straight to a notes app, a chat, or cloud storage without touching the file manager.

### Second widget button

```sh
printf '#!/data/data/com.termux/files/usr/bin/sh\npython3 ~/bin/probe.py scan\necho\npython3 ~/bin/probe.py export\necho\nprintf "enter to close"\nread x\n' > ~/.shortcuts/trellis-export
chmod +x ~/.shortcuts/trellis-export
```

Remove and re-add the home screen widget for the new entry to appear; Termux:Widget caches the list.

---

## Optional: home screen button

Install **Termux:Widget** from the same source as Termux.

If `~/.shortcuts` already exists and is owned by root (this happens on rooted devices, usually from a restore or backup tool), take ownership first. Replace `10356` with your own uid from `id`:

```sh
ls -ld ~/.shortcuts
su -c "chown -R 10356:10356 /data/data/com.termux/files/home/.shortcuts"
su -c "chmod 700 /data/data/com.termux/files/home/.shortcuts"
```

Otherwise just:

```sh
mkdir -p ~/.shortcuts && chmod 700 ~/.shortcuts
```

Then write the shortcut:

```sh
cat > ~/.shortcuts/trellis-report <<'SHORTCUT'
#!/data/data/com.termux/files/usr/bin/sh
python3 ~/bin/probe.py report
echo
echo "--- recent ---"
python3 ~/bin/probe.py scan
python3 ~/bin/probe.py recent
echo
printf "enter to close"
read x
SHORTCUT
chmod +x ~/.shortcuts/trellis-report
sh ~/.shortcuts/trellis-report
```

Long-press the home screen, add a Termux:Widget widget, tap `trellis-report`.

---

## What it records

`~/trellis-probe/journal.ndjson` — append-only, never rewritten.

| Event | Contents |
|---|---|
| `capture` | what arrived, hashed, before any interpretation, plus `instrument` |
| `reference` | share URL, cleaned URL, dropped tracking params, redirect chain, resolved final URL |
| `fetch_pair` | both fetches, byte hashes, text similarity, shell detection, and the identity the page volunteers about itself (canonical, og:url, DOI, title) |
| `finding` | the verdict and its flags |

`~/trellis-probe/blobs/` — content-addressed bodies. Delete freely; the journal survives without them.

### Which code wrote a row

Every `capture` carries `instrument`, the SHA-256 of the running `probe.py`, **first 16 hex characters**, the same width `object_hash` uses. Read it back with:

```sh
grep -o '"instrument": *"[^"]*"' ~/trellis-probe/journal.ndjson | sort | uniq -c
```

Compare that against the probe you have installed:

```sh
python3 -c "import hashlib;print(hashlib.sha256(open('$HOME/bin/probe.py','rb').read()).hexdigest()[:16])"
```

If they differ, the journal was written by a version you no longer have, and that is exactly what the field exists to tell you.

**A capture with no `instrument` field predates 2026-08-14.** Rows already written are not stamped and are not to be touched. Absence is the marker for the older instrument, and it is a reliable one: no version that emits the field can produce a capture without it.

That matters for the first corpus. Every row written on 2026-08-13 came from a probe that predates the referent-hashing code, which is why its `reference` rows carry no `referent_key` and its `finding` rows carry no `object_hash`. Establishing that took four separate diagnostic commands and a deduction, because nothing in the file said. It now says.

### Reading a journal that predates the hashing code

`probe.py bundle` handles this without touching the file. `object_hash` is `sha256(referent_key(final_url))[:16]`, a pure function of a URL those old `reference` rows already carry, so the bundle derives the missing hashes at read time using the same function the probe runs now. The hashes therefore join against another party's bundle exactly as freshly written ones would.

The derivation happens on read and nothing is appended. When it fires, `bundle` says how many finding rows were hashed that way and how many distinct objects those rows produced. Those two numbers differing is the interesting part: on the first corpus, 19 rows produced 16 objects. A recorded `object_hash` always wins; derivation only fills absences, so a current journal is unaffected.

### What the bundle leaves out, and why it says so

A bundle carries only objects that have a referent to hash. Two populations never can:

A **file share** has a reference row carrying no address, because the payload arrived with nothing to resolve. A **no_reference** capture has no reference row at all, because the share carried no URL. Neither has an identifier and neither may be given one, since inventing an address for an addressless object is the one move that would make the export look complete while being false.

`bundle` prints both counts and records them in `bundle.json` under `excluded`, alongside `findings`, the total it was working from. On the first corpus that reads 19 of 28, with 7 excluded for having no address and 2 for having no reference row. Those 9 are the hypothesis break the probe exists to measure, not a gap in the export, and a bundle that dropped them silently would understate its own denominator.

### Keeping an object out of an export

The journal is private and stays on the device. Bundles leave. Two commands, and
the difference between them matters.

**`probe.py redact <capture_id|object_hash> ...`** excludes an object from every
future `bundle` and `export`. Nothing is deleted. A `redaction` event is
appended, the rows stay where they are, and the bundle reports the count of
redacted objects alongside the other exclusions, because an export has to state
its own denominator. `probe.py unredact ...` reverses it with a further event,
so the sequence stays visible rather than the earlier decision disappearing.

Either a capture id or an object hash works. A bundle names objects by hash and
never by capture id, so requiring the capture id would mean the thing you are
looking at cannot be named.

One redacted sighting redacts the whole object, including sightings that were
not themselves redacted. A partially exported object is still exported.

**`probe.py purge <capture_id|object_hash> ...`** deletes rows. This is the one
place the append-only rule is broken, and it is broken on purpose.

Redaction cannot help when the address itself is the disclosure. An unlisted
link is a capability: a `claude.ai/share/` URL, a Google Docs `/d/` id, a
Dropbox share link. Possession of the address is the access, so a journal
holding one is the problem, not merely an export of it.

Purge rewrites the journal without the named captures and appends a record
saying that a rewrite happened, when, and how many rows went. It does not record
what they were, because recording them would defeat the purpose. **There is no
backup**, for the same reason.

What is given up is that no bytes are ever removed. What is kept is that the
record cannot silently lose things.

It asks for `PURGE` typed in full and refuses to run non-interactively, so a
widget or a batch script cannot trigger it.

**Blobs are not touched.** Bodies under `~/trellis-probe/blobs/` are
content-addressed and shared, and purge does not remove them. If a payload
rather than an address is the concern, delete the blob yourself; the journal
survives without it.

### Repeat encounters

`bundle` reports how many objects were seen more than once and how many references collapsed into how many objects. That collapse is what referent hashing is for: the same object reached twice by different addresses is one object, and nothing had to agree for that to hold.

The journal stays a record of what happened rather than a record of what was later worked out. That the first corpus was written by one instrument and read by another is evidence, and rewriting rows would destroy it.

---

## Verdicts

| Verdict | Meaning | Consequence for the design |
|---|---|---|
| `stable_referent` | fetched, held still, volunteered an identity | the gate. structure attaches |
| `client_rendered` | reference is fine, server returned a real application bundle, content renders client-side | fetch problem, known workarounds |
| `soft_refusal` | 200 OK with a small stub: the producer received the request, declined to serve, and reported success | a refusal that does not announce itself |
| `recovered_from_archive` | the producer declined, and an archived snapshot supplied the payload | dated third-party evidence, arguably better than a live fetch |

## When a producer declines

Some producers serve their content to their own application and refuse it to a script. The probe then asks whether to look in the Internet Archive.

It lists what snapshots exist, with dates, and offers three choices: use one of them, save a new archive, or skip. **Creating an archive is never automatic.** It writes to a permanent public record on someone else's infrastructure, and that is a decision for the receiver rather than the tool.

If the URL looks like it carries a share token, session key, or document id, the prompt says so and requires typing `SAVE` to confirm. A `claude.ai/share/` link, a Google Docs `/d/` id, and a Reddit `/s/` shortlink are all capabilities rather than addresses: publishing one to a permanent public archive hands that capability to everyone forever.

When the probe runs non-interactively, from the widget or a batch scan, it reads existing snapshots and never creates new ones.

### A refused fetch no longer discards the referent

Changed 2026-08-14. The referent is derived before anything is fetched, and a producer refusing to serve bytes does not invalidate the address that was already resolved. Earlier versions emitted the `producer_refused` and `unreachable` findings with no `object_hash`, so every derivation downstream dropped the object and the corpus counted it as producing no referent at all.

Facebook and NYT in the first corpus are both that case. The receiver held a good shared URL for each and threw it away because the bytes were refused.

Now the finding for a refused fetch carries `object_hash`, `referent_key`, and the flag `referent_held`. The verdict still names the payload outcome, `producer_refused` or `unreachable`, because the payload is what failed. No new verdict was added, because the existing ones already describe the payload correctly; what was missing was the other half of the measurement.

Referent stability and payload acquisition are separate measurements. The instrument used to conflate them by discarding the first whenever the second failed.

### Why the archive may be the better source

A live fetch is unreproducible. You cannot later prove what was there, and the bytes move between requests. An archived snapshot is dated, stable, third-party held, and re-fetchable by anyone. For grounding a claim in what a source said, that is stronger evidence, not a fallback.
| `producer_refused` | producer received the request and declined: paywall, bot block, geo, gone. The referent is kept and recorded | copyright and access question, already anticipated |
| `referent_problem` | fetched, and something about the referent did not hold | the interesting middle |
| `unreachable` | network failure, no producer response | probe noise, not a finding |
| `no_reference` | the share carried no resolvable reference at all | **the hypothesis break** |
| `payload_no_referent` | a file arrived: bytes present, nothing to resolve | **the hypothesis break, cleanest form** |
| `payload_with_embedded_referent` | a file arrived carrying a DOI or URL inside it | the escape hatch |

### The two share paths

A **URL share** supplies a reference and no payload. The probe resolves it, fetches twice, and tests whether the referent holds still.

A **file share** supplies a payload and no reference. There is nothing to resolve and nothing to re-fetch. Local structure attaches perfectly; what is absent is any way for a second party to point at the same object.

That asymmetry is the finding this probe exists to measure. The receiver-substrate hypothesis is strongest where references are stable and weakest where payload arrives naked, and the ratio between those two on your real reading is the number that decides how much of the design survives.

The probe checks shared files for embedded references anyway: a DOI, a canonical URL, an ISBN. A PDF of a paper usually carries its own identity even when the share does not. That is the escape hatch, and how often it fires is worth watching separately.

---

## Flags

`wrapper_share_link` · `noise_params_present` · `cross_host_redirect` · `payload_withheld` · `payload_not_at_reference` · `unstable_text` · `unstable_bytes` · `canonical_disagrees` · `no_producer_identity` · `thin_payload` · `similarity_unmeasurable` · `referent_held` · `no_archive_snapshot`

Two notes. `unstable_bytes` fires on nearly everything including Wikipedia and is not itself a problem: bytes move, text holds, referent stable. `unstable_text` is the one that matters. And `similarity_unmeasurable` is a statement about the measurement rather than about the object, since similarity over a few hundred characters of scaffolding measures session nonces.

---

## What to feed it

Read normally, and deliberately include the hostile cases:

- a link from a personalized feed
- a paywalled article
- a YouTube video
- a Discord or WhatsApp message
- a Google search result
- a PDF opened in a reader
- **something from an app that offers no share-as-link at all, only a screenshot**

That last category is the one to watch. If it is large, receiver-side instantiation needs a capture path that does not depend on the producer emitting a reference, and that reshapes the child trellis rather than merely inconveniencing it.

Run for a week across real reading. Sample size matters more than curation: the point is the population you actually encounter, not the population you would choose.

---

## Reading the result

The report splits four ways because the failure modes have different consequences.

The first line is the gate: how often structure can attach. The second is solvable. The third is a known question with known answers. **The fourth is the one that would shrink the design**, because an object that emits no reference cannot be instantiated by a receiver acting alone, which is the hypothesis.

If the first line is high, the design's premise holds against the real population. If the fourth is high, the interesting question becomes which apps produce it and whether a non-reference capture path exists.

---

## A note on the rooted device

While setting this up, a root-owned directory turned up inside Termux's home that Termux itself could not read or modify. That is the root safety boundary arriving as a live example: **a rooted device is a single trust envelope, not a boundary against the device owner or anything granted root.**

The probe's journal lives in `~/trellis-probe/`. On a rooted device that is not private from privileged processes. Fine for this experiment, which captures only what you deliberately share. Worth remembering before anything sensitive accumulates there.
