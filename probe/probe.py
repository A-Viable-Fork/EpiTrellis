#!/usr/bin/env python3
"""
Referent Stability Probe  v0.1
Receiver Substrate Trellis, gate candidate GC-1 / ledger A-1.

Question: do the objects a person actually encounters carry a referent stable
enough for structure to attach?

Method: intercept shares, record the raw capture, resolve the reference,
fetch twice, and record what differs. No schema beyond an append-only journal.
Every derived structure comes later, from the journal.

Journal is newline-delimited JSON, append-only, never rewritten.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import uuid

HOME = os.path.expanduser("~")
ROOT = os.path.join(HOME, "trellis-probe")
JOURNAL = os.path.join(ROOT, "journal.ndjson")
BLOBS = os.path.join(ROOT, "blobs")

UA = ("Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36")

# Bot heuristics check for the absence of these before they check anything
# else. A UA string alone is the shape of a scraper.
HEADERS = {
    "User-Agent": UA,
    "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
               "image/avif,image/webp,*/*;q=0.8"),
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}

# Query parameters that carry no referent: campaign, session, click identity.
NOISE_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "utm_id", "utm_name", "utm_reader", "utm_brand", "utm_social",
    "fbclid", "gclid", "dclid", "gbraid", "wbraid", "msclkid", "twclid",
    "igshid", "igsh", "ttclid", "yclid", "mc_cid", "mc_eid",
    "ref", "ref_src", "ref_url", "referrer", "source",
    "si", "is", "feature", "app", "pp", "pli", "usp",  # share-sheet noise
    "s", "t", "cmpid", "smid", "spref", "share_id", "sh",
    "_branch_match_id", "_bhlid", "rdt", "cvid", "ocid",
}

# Hosts that emit wrappers rather than referents.
WRAPPER_HOSTS = {
    "t.co", "bit.ly", "tinyurl.com", "goo.gl", "ow.ly", "buff.ly",
    "lnkd.in", "trib.al", "dlvr.it", "ift.tt", "shorturl.at", "rb.gy",
    "l.facebook.com", "lm.facebook.com", "out.reddit.com", "href.li",
    "news.google.com", "www.google.com", "google.com", "r.zst.io",
    "youtu.be", "amzn.to", "a.co", "spoti.fi", "apple.co",
}

# Fragments of markup that indicate the fetch was refused rather than served.
WALL_MARKERS = [
    "enable javascript", "please enable js", "checking your browser",
    "captcha", "are you a robot", "access denied", "403 forbidden",
    "subscribe to continue", "subscribers only", "create a free account",
    "you have reached your limit", "register to read", "sign in to read",
    "cf-browser-verification", "just a moment",
]


def ensure_dirs():
    os.makedirs(BLOBS, exist_ok=True)
    os.makedirs(ROOT, exist_ok=True)


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def write_blob(b):
    h = sha256(b)
    p = os.path.join(BLOBS, h)
    if not os.path.exists(p):
        with open(p, "wb") as f:
            f.write(b)
    return h


_INSTRUMENT = None


def instrument_hash():
    """sha256 of the running probe, first 16 hex characters.

    The journal must be able to answer which code wrote a row without anyone
    running a diagnostic against it afterward. Establishing that for the first
    corpus took four separate commands and a deduction, because nothing in the
    file said.

    Sixteen characters rather than sixty-four, matching `refhash`. It
    distinguishes versions of one file on one device, which is all it is for.

    A capture with no `instrument` field was written before 2026-08-14 by a
    probe that predates this stamp. Absence is the marker for that instrument,
    and rows already written are not to be touched."""
    global _INSTRUMENT
    if _INSTRUMENT is None:
        try:
            path = os.path.abspath(__file__)
        except NameError:
            path = os.path.abspath(sys.argv[0])
        try:
            with open(path, "rb") as f:
                _INSTRUMENT = sha256(f.read())[:16]
        except Exception:
            _INSTRUMENT = "unreadable"
    return _INSTRUMENT


def emit(record):
    """Append one event. The journal is the only durable artifact."""
    record.setdefault("at", time.strftime("%Y-%m-%dT%H:%M:%S%z"))
    with open(JOURNAL, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def notify(title, body):
    try:
        subprocess.run(
            ["termux-notification", "--title", title, "--content", body[:400]],
            check=False, timeout=10,
        )
    except Exception:
        pass


# ---------------------------------------------------------------- reference

def extract_urls(text):
    """Wikipedia and many CMS URLs contain parentheses. Take a greedy match,
    then trim trailing punctuation, keeping parens that balance."""
    out = []
    for raw in re.findall(r"https?://[^\s<>\"']+", text or ""):
        u = raw
        while u and u[-1] in ".,;:!?'\"]}>":
            u = u[:-1]
        while u.endswith(")") and u.count("(") < u.count(")"):
            u = u[:-1]
        if u:
            out.append(u)
    return out


def strip_noise(url):
    """Remove parameters that vary per share without changing the referent."""
    try:
        u = urllib.parse.urlsplit(url)
    except ValueError:
        return url, []
    if not u.query:
        return url, []
    kept, dropped = [], []
    for k, v in urllib.parse.parse_qsl(u.query, keep_blank_values=True):
        (dropped if k.lower() in NOISE_PARAMS else kept).append((k, v))
    q = urllib.parse.urlencode(kept)
    return urllib.parse.urlunsplit((u.scheme, u.netloc, u.path, q, "")), [k for k, _ in dropped]


def referent_key(url):
    """Normalize a URL to the form two parties would independently derive.

    This is a local convention, not a protocol floor: a receiver that
    normalizes differently simply fails to join, which costs a match and
    breaks nothing. The join is an unlocked capability rather than a
    condition of participation."""
    try:
        u = urllib.parse.urlsplit(url)
    except ValueError:
        return url
    scheme = "https"
    host = (u.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]
    if host.startswith("m.") or host.startswith("mobile."):
        host = host.split(".", 1)[1]
    host = re.sub(r":(80|443)$", "", host)
    path = u.path.rstrip("/") or "/"
    q = urllib.parse.urlencode(
        sorted((k, v) for k, v in urllib.parse.parse_qsl(u.query, keep_blank_values=True)
               if k.lower() not in NOISE_PARAMS))
    return urllib.parse.urlunsplit((scheme, host, path, q, ""))


def refhash(url):
    return sha256(referent_key(url).encode())[:16]


def alt_referents(final_url, meta):
    """Other addresses for the same work. A hash match on any of these is a
    candidate equivalence, never an assertion: whether two addresses denote
    one object is a semantic judgment and belongs to a community."""
    alts = {}
    for k in ("canonical", "og_url"):
        v = meta.get(k)
        if v and referent_key(v) != referent_key(final_url):
            alts[k] = {"url": v, "hash": refhash(v)}
    if meta.get("doi"):
        d = "doi:" + meta["doi"].lower()
        alts["doi"] = {"url": d, "hash": sha256(d.encode())[:16]}
    return alts


def host_of(url):
    try:
        return urllib.parse.urlsplit(url).netloc.lower()
    except ValueError:
        return ""


def resolve(url, hops=6):
    """Follow redirects by hand so every hop is recorded."""
    chain = [url]
    cur = url
    for _ in range(hops):
        try:
            req = urllib.request.Request(cur, method="HEAD", headers=dict(HEADERS))
            with urllib.request.urlopen(req, timeout=20) as r:
                final = r.geturl()
        except Exception:
            try:
                req = urllib.request.Request(cur, headers=dict(HEADERS))
                with urllib.request.urlopen(req, timeout=25) as r:
                    final = r.geturl()
            except Exception:
                break
        if final == cur:
            break
        chain.append(final)
        cur = final
    return cur, chain


# Status codes where the producer received the request and declined it.
# These are findings about the referent, not failures of the probe.
REFUSAL = {401: "auth_required", 402: "payment_required", 403: "access_denied",
           404: "referent_gone", 410: "referent_gone", 429: "rate_limited",
           451: "legally_blocked", 503: "challenge_or_unavailable"}


def fetch(url, retry=True):
    """One retry after a pause on a throttle, so a transient limit is not
    recorded as producer policy."""
    try:
        req = urllib.request.Request(url, headers=dict(HEADERS))
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            return {
                "status": r.status,
                "final_url": r.geturl(),
                "content_type": r.headers.get("Content-Type", ""),
                "bytes": len(body),
                "body": body,
            }
    except urllib.error.HTTPError as e:
        if e.code in (429, 503) and retry:
            time.sleep(20)
            out = fetch(url, retry=False)
            out["retried_after_throttle"] = True
            return out
        return {"error": "HTTP %d" % e.code, "status": e.code,
                "refusal": REFUSAL.get(e.code, "http_error")}
    except Exception as e:
        return {"error": "%s: %s" % (type(e).__name__, str(e)[:200]),
                "refusal": None}


# ---------------------------------------------------------------- content

TAG = re.compile(r"<[^>]+>")
SCRIPTY = re.compile(r"<(script|style|noscript)\b.*?</\1>", re.S | re.I)
WS = re.compile(r"\s+")


# ---------------------------------------------------------------- archive

WAYBACK_API = "https://archive.org/wayback/available?url="


def wayback_lookup(url):
    """Ask for the closest snapshot. This is a capability provider filling the
    payload-acquisition function: one contract among several, alongside direct
    fetch, on-device render, accessibility read, peer supply, and paste."""
    try:
        api = WAYBACK_API + urllib.parse.quote(url, safe="")
        req = urllib.request.Request(api, headers=dict(HEADERS))
        with urllib.request.urlopen(req, timeout=25) as r:
            d = json.load(r)
        snap = (d.get("archived_snapshots") or {}).get("closest") or {}
        if snap.get("available") and snap.get("url"):
            return {"url": snap["url"].replace("http://", "https://", 1),
                    "timestamp": snap.get("timestamp"),
                    "status": snap.get("status")}
    except Exception as e:
        return {"error": "%s: %s" % (type(e).__name__, str(e)[:120])}
    return None


CDX = "https://web.archive.org/cdx/search/cdx"
SAVE = "https://web.archive.org/save/"

# A URL carrying one of these is a capability, not an address. Publishing it
# to a permanent public archive hands the capability to everyone.
PRIVATE_HINT = re.compile(
    r"/share/|/s/[A-Za-z0-9]{8,}|token=|auth=|key=|session|invite|"
    r"[?&](t|k|si|is)=[A-Za-z0-9_-]{10,}|/d/[A-Za-z0-9_-]{20,}", re.I)


def archive_list(url, limit=8):
    """List snapshots rather than taking the closest. The closest may be years
    old, and which snapshot is right depends on what the receiver is after."""
    try:
        q = (CDX + "?url=" + urllib.parse.quote(url, safe="")
             + "&output=json&limit=-%d&fl=timestamp,statuscode,length"
               "&collapse=timestamp:6&filter=statuscode:200" % limit)
        req = urllib.request.Request(q, headers=dict(HEADERS))
        with urllib.request.urlopen(req, timeout=30) as r:
            rows = json.load(r)
        if len(rows) < 2:
            return []
        out = []
        for row in rows[1:]:
            ts = row[0]
            out.append({
                "timestamp": ts,
                "date": "%s-%s-%s" % (ts[0:4], ts[4:6], ts[6:8]),
                "length": row[2] if len(row) > 2 else None,
                "url": "https://web.archive.org/web/%s/%s" % (ts, url),
            })
        return sorted(out, key=lambda x: x["timestamp"], reverse=True)
    except Exception:
        # CDX refuses some clients. Fall back to the single closest snapshot.
        one = wayback_lookup(url)
        if one and "error" not in one:
            ts = one.get("timestamp", "")
            one["date"] = "%s-%s-%s" % (ts[0:4], ts[4:6], ts[6:8]) if ts else "?"
            return [one]
        return []


def archive_save(url):
    """Trigger a new capture. This writes to a permanent public archive and is
    never done without explicit consent."""
    try:
        req = urllib.request.Request(SAVE + url, headers=dict(HEADERS))
        with urllib.request.urlopen(req, timeout=90) as r:
            return {"saved": True, "url": r.geturl(), "status": r.status}
    except Exception as e:
        return {"saved": False, "error": "%s: %s" % (type(e).__name__, str(e)[:160])}


def archive_choose(url, cid):
    """Present what exists and let the receiver decide. Reading an existing
    snapshot is free and private. Creating one is a public, permanent act
    performed on someone else's infrastructure, so it is always asked."""
    snaps = archive_list(url)
    private = bool(PRIVATE_HINT.search(url))

    if not sys.stdin.isatty():
        # Non-interactive: read what exists, never create.
        emit({"event": "archive_policy", "capture_id": cid,
              "mode": "non_interactive_read_only",
              "snapshots_found": len(snaps), "private_hint": private})
        return snaps[0] if snaps else None

    print()
    if snaps:
        print("archived snapshots for this object:")
        for i, s2 in enumerate(snaps[:6], 1):
            ln = ("%s bytes" % s2["length"]) if s2.get("length") else ""
            print("  %d) %s   %s" % (i, s2["date"], ln))
    else:
        print("no archived snapshot found for this object")

    if private:
        print()
        print("  NOTE: this URL looks like it carries a share token or")
        print("  session key. Archiving it publishes that capability")
        print("  permanently and publicly. Decline unless you are certain.")

    print()
    print("  [1-6] use that snapshot")
    print("  [s]   save a new archive now (public, permanent)")
    print("  [n]   skip, record the refusal as it stands")
    try:
        ans = input("  choice [n]: ").strip().lower()
    except Exception:
        ans = "n"

    if ans.isdigit() and snaps and 1 <= int(ans) <= len(snaps[:6]):
        pick = snaps[int(ans) - 1]
        emit({"event": "archive_policy", "capture_id": cid, "mode": "chose_existing",
              "timestamp": pick["timestamp"]})
        return pick
    if ans == "s":
        if private:
            c = input("  URL may carry a private capability. type SAVE to confirm: ")
            if c.strip() != "SAVE":
                emit({"event": "archive_policy", "capture_id": cid,
                      "mode": "declined_private"})
                print("  skipped")
                return None
        print("  saving, this can take a minute...")
        res = archive_save(url)
        emit({"event": "archive_policy", "capture_id": cid, "mode": "saved_new",
              "result": res, "private_hint": private})
        if res.get("saved"):
            print("  saved")
            return {"url": res["url"], "timestamp": time.strftime("%Y%m%d%H%M%S"),
                    "date": time.strftime("%Y-%m-%d"), "fresh": True}
        print("  save failed: " + res.get("error", "")[:80])
        return None

    emit({"event": "archive_policy", "capture_id": cid, "mode": "declined"})
    return None


def archive_recover(url, cid=None):
    """Try to obtain payload the producer declined to serve. What comes back
    is a dated third-party snapshot, not the live object, and is recorded as
    such: for grounding a claim it is arguably the better source, since it is
    stable and independently re-fetchable where a live fetch is not."""
    snap = archive_choose(url, cid)
    if not snap:
        return {"archive": None, "reason": "no_snapshot_or_declined"}
    got = fetch(snap["url"], retry=False)
    if "error" in got:
        return {"archive": snap, "reason": "snapshot_unfetchable", "detail": got["error"]}
    return {"archive": snap, "fetched": got}


def visible_text(html):
    t = SCRIPTY.sub(" ", html)
    t = TAG.sub(" ", t)
    return WS.sub(" ", t).strip()


def meta_identity(html):
    """Identity assertions the page volunteers. These are producer claims."""
    out = {}
    pats = {
        "canonical": r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)',
        "og_url": r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)',
        "og_title": r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)',
        "doi": r'(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)',
        "title": r"<title[^>]*>(.*?)</title>",
    }
    for k, p in pats.items():
        m = re.search(p, html, re.I | re.S)
        if m:
            out[k] = WS.sub(" ", m.group(1)).strip()[:400]
    return out


SHELL_MARKERS = [
    'id="root"', "id='root'", 'id="__next"', 'id="app"', 'id="react-root"',
    'data-reactroot', 'ng-app', '__NUXT__', '__remixContext', 'shreddit-app',
]


def shell_score(html, text_len):
    """Three ways a 200 response can arrive with no readable content.

    A client-side render sends a real application bundle and fills the page
    in the browser. A soft refusal sends a small stub: the producer received
    the request, declined to serve, and reported success anyway. The size of
    the response separates them, because an application is large and a
    brush-off is not."""
    scripts = sum(len(m) for m in re.findall(r"<script\b.*?</script>", html, re.S | re.I))
    markers = [k for k in SHELL_MARKERS if k in html]
    ratio = scripts / max(text_len, 1)
    total = len(html)

    empty = text_len < 200
    small = total < 25000 and scripts < 20000
    is_stub = empty and small
    is_shell = (not is_stub) and text_len < 900 and (bool(markers) or ratio > 40)

    return {
        "script_bytes": scripts,
        "response_bytes": total,
        "shell_markers": markers[:4],
        "script_to_text": round(ratio, 1),
        "is_shell": is_shell,
        "is_stub": is_stub,
    }


def looks_walled(text):
    low = text[:4000].lower()
    return [m for m in WALL_MARKERS if m in low]


def shingles(text, n=8):
    w = text.split()
    return {" ".join(w[i:i + n]) for i in range(0, max(0, len(w) - n), 4)}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# ---------------------------------------------------------------- the probe

STABILITY_CHECK = os.environ.get("TRELLIS_STABILITY") == "1"


def probe(shared_text):
    cid = str(uuid.uuid4())
    urls = extract_urls(shared_text)

    emit({
        "event": "capture",
        "capture_id": cid,
        "method": "termux.url_opener",
        "instrument": instrument_hash(),
        "raw": shared_text[:4000],
        "raw_hash": sha256(shared_text.encode()),
        "url_count": len(urls),
    })

    if not urls:
        emit({"event": "finding", "capture_id": cid, "kind": "no_reference",
              "note": "shared text carried no resolvable reference"})
        notify("Trellis probe", "Captured text with no URL. Logged as no_reference.")
        return

    url = urls[0]
    cleaned, dropped = strip_noise(url)
    wrapper = host_of(url) in WRAPPER_HOSTS

    final, chain = resolve(cleaned)
    cross_host = host_of(final) != host_of(cleaned)

    emit({
        "event": "reference",
        "capture_id": cid,
        "referent_key": referent_key(final),
        "object_hash": refhash(final),
        "shared_url": url,
        "cleaned_url": cleaned,
        "dropped_params": dropped,
        "wrapper_host": wrapper,
        "redirect_chain": chain,
        "final_url": final,
        "cross_host_redirect": cross_host,
    })

    # One fetch by default. The second exists to detect personalized content
    # and has found none in the corpus so far, while the double request is
    # itself a bot signature that draws throttles. Opt in with
    # TRELLIS_STABILITY=1 when the question is stability rather than capture.
    a = fetch(final)
    if STABILITY_CHECK:
        time.sleep(45)
        b = fetch(final)
    else:
        b = {}

    payload_source = "direct"
    archive_meta = None

    if "error" in a:
        refusal = a.get("refusal")
        rec = archive_recover(final, cid)
        emit({"event": "archive_attempt", "capture_id": cid,
              "url": final, "result": {k: v for k, v in rec.items() if k != "fetched"}})

        if rec.get("fetched"):
            a = rec["fetched"]
            payload_source = "archive"
            archive_meta = rec["archive"]
        else:
            kind = "producer_refused" if refusal else "unreachable"
            # The referent was derived above, before anything was fetched, and
            # a refused fetch does not invalidate it. Earlier versions emitted
            # this finding without an object_hash, so every downstream
            # derivation dropped the object entirely and the corpus counted it
            # as producing no referent at all. Facebook and NYT are both that
            # case: the receiver held a good shared URL for each and threw it
            # away because the bytes were refused.
            #
            # Referent stability and payload acquisition are separate
            # measurements. Recording the referent here is what keeps them
            # separate. The verdict still describes the payload, because that
            # is what failed, and `referent_held` says the other half survived.
            emit({"event": "finding", "capture_id": cid, "kind": kind,
                  "object_hash": refhash(final),
                  "referent_key": referent_key(final),
                  "flags": ([refusal] if refusal else [])
                           + ["no_archive_snapshot", "referent_held"],
                  "detail": a["error"], "host": host_of(final)})
            notify("Trellis probe: " + kind,
                   (refusal or a["error"])[:80] + "\nreferent held")
            return

    body_a, body_b = a.pop("body"), b.pop("body", b"")
    ha, hb = write_blob(body_a), (write_blob(body_b) if body_b else None)

    ta = visible_text(body_a.decode("utf-8", "replace"))
    tb = visible_text(body_b.decode("utf-8", "replace")) if body_b else ""
    meta = meta_identity(body_a.decode("utf-8", "replace"))
    walls = looks_walled(ta)
    shell = shell_score(body_a.decode("utf-8", "replace"), len(ta))
    # Similarity over very short text measures nonces, not content. Do not
    # report a referent finding from a measurement artifact.
    sim = (jaccard(shingles(ta), shingles(tb))
           if tb and len(ta) > 600 and len(tb) > 600 else None)

    emit({
        "event": "fetch_pair",
        "capture_id": cid,
        "url": final,
        "a": {**a, "blob": ha, "text_len": len(ta)},
        "b": {**{k: v for k, v in b.items() if k != "body"},
              "blob": hb, "text_len": len(tb)},
        "byte_identical": ha == hb,
        "text_similarity": sim,
        "meta_identity": meta,
        "wall_markers": walls,
        "shell": shell,
    })

    # Findings: the point of the probe.
    f = []
    if wrapper:
        f.append("wrapper_share_link")
    if dropped:
        f.append("noise_params_present")
    if cross_host:
        f.append("cross_host_redirect")
    if walls:
        f.append("payload_withheld")
    if shell["is_stub"]:
        f.append("served_stub_not_content")
    if shell["is_shell"]:
        f.append("payload_not_at_reference")
    if sim is not None and sim < 0.90:
        f.append("unstable_text")
    if sim is None and tb:
        f.append("similarity_unmeasurable")
    if ha != hb:
        f.append("unstable_bytes")
    if "canonical" in meta and meta["canonical"].split("?")[0] != final.split("?")[0]:
        f.append("canonical_disagrees")
    if not meta:
        f.append("no_producer_identity")
    if len(ta) < 400 and not (shell["is_shell"] or shell["is_stub"]):
        f.append("thin_payload")

    if shell["is_stub"] and payload_source == "direct":
        rec = archive_recover(final, cid)
        emit({"event": "archive_attempt", "capture_id": cid, "url": final,
              "result": {k: v for k, v in rec.items() if k != "fetched"}})
        if rec.get("fetched") and "error" not in rec["fetched"]:
            ab = rec["fetched"].pop("body", b"")
            at = visible_text(ab.decode("utf-8", "replace"))
            if len(at) > max(len(ta), 400):
                ta, ha = at, write_blob(ab)
                meta = meta_identity(ab.decode("utf-8", "replace")) or meta
                shell = shell_score(ab.decode("utf-8", "replace"), len(at))
                payload_source = "archive"
                archive_meta = rec["archive"]
                f = [x for x in f if x != "served_stub_not_content"]

    if payload_source == "archive":
        f.append("payload_from_archive")

    if shell["is_stub"] and payload_source == "direct":
        verdict = "soft_refusal"
    elif shell["is_shell"]:
        verdict = "client_rendered"
    elif set(f) & {"unstable_text", "payload_withheld"}:
        verdict = "referent_problem"
    elif set(f) & {"no_producer_identity", "thin_payload"}:
        verdict = "referent_problem"
    else:
        verdict = "stable_referent"

    if payload_source == "archive" and verdict in ("soft_refusal", "client_rendered"):
        verdict = "recovered_from_archive"

    emit({
        "event": "finding",
        "capture_id": cid,
        "kind": verdict,
        "object_hash": refhash(final),
        "alt_referents": alt_referents(final, meta),
        "payload_source": payload_source,
        "archive": archive_meta,
        "flags": f,
        "title": meta.get("og_title") or meta.get("title", "")[:200],
        "host": host_of(final),
    })

    notify("Trellis probe: " + verdict,
           (meta.get("og_title") or host_of(final))
           + "\n" + (", ".join(f) or "clean")
           + "\n" + tally())


EXT_KIND = {
    ".pdf": "document", ".epub": "document", ".docx": "document", ".doc": "document",
    ".md": "text", ".txt": "text", ".csv": "text", ".json": "text", ".html": "text",
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".webp": "image",
    ".gif": "image", ".heic": "image", ".bmp": "image",
    ".mp4": "video", ".mkv": "video", ".webm": "video", ".mov": "video",
    ".mp3": "audio", ".m4a": "audio", ".ogg": "audio", ".opus": "audio",
}

SCREENSHOT_HINT = re.compile(r"screenshot|screen[_-]?shot|scrnshot|img_\d{8}", re.I)


def sniff(head, ext):
    """Magic bytes beat the extension, which a share can rewrite."""
    if head[:4] == b"%PDF":
        return "document"
    if head[:8] == b"\x89PNG\r\n\x1a\n" or head[:3] == b"\xff\xd8\xff":
        return "image"
    if head[:4] == b"PK\x03\x04":
        return "archive_or_office"
    if head[4:12] in (b"ftypisom", b"ftypmp42", b"ftypqt  "):
        return "video"
    return EXT_KIND.get(ext, "unknown")


def embedded_refs(data, kind):
    """Does the payload point back at anything? A document that carries a DOI
    or canonical URL has a referent even though the share supplied none."""
    if kind not in ("text", "document", "unknown"):
        return {}
    try:
        t = data[:400000].decode("utf-8", "replace")
    except Exception:
        return {}
    out = {}
    urls = extract_urls(t)
    if urls:
        out["urls"] = urls[:8]
    doi = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", t)
    if doi:
        out["doi"] = doi.group(0)[:120]
    isbn = re.search(r"\bISBN[- ]?(?:13|10)?:?\s*([\d-]{10,17})", t, re.I)
    if isbn:
        out["isbn"] = isbn.group(1)
    return out


def probe_file(path):
    """A shared file is the cleanest case of payload without reference:
    the bytes are present and there is nothing to resolve."""
    cid = str(uuid.uuid4())
    name = os.path.basename(path)
    ext = os.path.splitext(name)[1].lower()

    try:
        with open(path, "rb") as f:
            data = f.read()
    except Exception as e:
        emit({"event": "finding", "capture_id": cid, "kind": "unreachable",
              "flags": ["file_unreadable"], "detail": str(e)[:200]})
        notify("Trellis probe", "could not read shared file")
        return

    h = write_blob(data)
    kind = sniff(data[:16], ext)
    refs = embedded_refs(data, kind)

    emit({
        "event": "capture",
        "capture_id": cid,
        "method": "termux.file_editor",
        "instrument": instrument_hash(),
        "filename": name,
        "ext": ext,
        "bytes": len(data),
        "blob": h,
        "raw_hash": h,
        "url_count": len(refs.get("urls", [])),
    })

    emit({
        "event": "reference",
        "capture_id": cid,
        "shared_url": None,
        "payload_present": True,
        "media_kind": kind,
        "embedded_refs": refs,
    })

    f = ["payload_present", "media_kind:" + kind]
    if SCREENSHOT_HINT.search(name):
        f.append("screenshot_share")
    if refs.get("doi"):
        f.append("embedded_doi")
    if refs.get("urls"):
        f.append("embedded_url")
    if refs.get("isbn"):
        f.append("embedded_isbn")
    if len(data) < 200:
        f.append("thin_payload")

    # The payload is here and local structure attaches. What is absent is a
    # reference anyone else could resolve to the same object.
    verdict = "payload_no_referent"
    if refs.get("doi") or refs.get("urls"):
        verdict = "payload_with_embedded_referent"

    emit({"event": "finding", "capture_id": cid, "kind": verdict,
          "flags": f, "title": name[:80], "host": None})

    notify("Trellis probe: " + verdict,
           name + "\n" + ", ".join(f) + "\n" + tally())


# The drop folder. Save or move anything here, then run: probe.py scan
# Visible from any Android file manager as Download/payload.
DROP = os.path.expanduser("~/storage/downloads/payload")
SKIP_EXT = {".part", ".crdownload", ".tmp", ".pending"}


def seen_hashes():
    """Blobs already captured. Dedupe is by content, so re-saving the same
    file under a new name is correctly ignored."""
    h = set()
    if not os.path.exists(JOURNAL):
        return h
    for l in open(JOURNAL):
        if '"capture"' not in l:
            continue
        try:
            r = json.loads(l)
        except Exception:
            continue
        if r.get("event") == "capture":
            for k in ("blob", "raw_hash"):
                if r.get(k):
                    h.add(r[k])
    return h


def scan(target=None):
    """Ingest anything new in the drop folder. Dedupe is by content hash, so
    rescanning is free and a file re-saved under another name is ignored.
    Files are read and left in place; nothing is moved or deleted."""
    ensure_dirs()
    d = os.path.expanduser(target) if target else DROP

    if not os.path.isdir(d):
        try:
            os.makedirs(d, exist_ok=True)
            print("created drop folder: %s" % d)
            print("save or move files there, then run: probe.py scan")
        except Exception as e:
            print("cannot create %s (%s)" % (d, e))
            print("if storage permission is missing, run: termux-setup-storage")
        return

    known = seen_hashes()
    found = new = 0
    for name in sorted(os.listdir(d)):
        path = os.path.join(d, name)
        if not os.path.isfile(path) or name.startswith("."):
            continue
        if os.path.splitext(name)[1].lower() in SKIP_EXT:
            continue
        found += 1
        try:
            with open(path, "rb") as f:
                h = sha256(f.read())
        except Exception as e:
            print("unreadable: %s (%s)" % (name[:40], type(e).__name__))
            continue
        if h in known:
            continue
        known.add(h)
        new += 1
        print("ingesting %s" % name[:60])
        probe_file(path)

    print("\n%s\n%d files present, %d newly captured" % (d, found, new))
    if new:
        print()
        recent(new)


EXPORT_DIR = os.path.expanduser("~/storage/downloads/trellis-export")


def export():
    """Write a portable snapshot outside Termux's private storage: a readable
    report, the findings as a table, and a copy of the journal.

    The journal is the artifact. The rest is derived and can be regenerated,
    which is why the copy matters more than the formatting."""
    ensure_dirs()
    try:
        os.makedirs(EXPORT_DIR, exist_ok=True)
    except Exception as e:
        print("cannot write %s (%s)" % (EXPORT_DIR, e))
        print("if storage permission is missing, run: termux-setup-storage")
        return

    # Retire prior exports so the folder holds one current set. Nothing is
    # deleted: the journal is append-only and its copies are too.
    old = os.path.join(EXPORT_DIR, "archive")
    prior = [f for f in os.listdir(EXPORT_DIR)
             if os.path.isfile(os.path.join(EXPORT_DIR, f))]
    if prior:
        os.makedirs(old, exist_ok=True)
        for f in prior:
            src, dst = os.path.join(EXPORT_DIR, f), os.path.join(old, f)
            try:
                if os.path.exists(dst):
                    os.remove(dst)
                os.replace(src, dst)
            except Exception:
                pass
        print("retired %d prior file(s) to archive/" % len(prior))

    stamp = time.strftime("%Y%m%d-%H%M")
    rows = []
    if os.path.exists(JOURNAL):
        rows = [json.loads(l) for l in open(JOURNAL) if l.strip()]
    # The journal never leaves the device by accident, but export writes a copy
    # to shared storage, so a redaction has to hold here too.
    red = redactions(rows)
    if red:
        rows = [r for r in rows if r.get("capture_id") not in red]
        print("export omits %d redacted capture(s); the journal on this device "
              "is unchanged" % len(red))
    finds = [r for r in rows if r.get("event") == "finding"]

    # 1. the report, as text
    rp = os.path.join(EXPORT_DIR, "report-%s.txt" % stamp)
    import io
    buf, real = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        report()
    finally:
        sys.stdout = real
    open(rp, "w").write(buf.getvalue())

    # 2. findings as CSV, one row per capture
    cp = os.path.join(EXPORT_DIR, "findings-%s.csv" % stamp)
    import csv
    with open(cp, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["at", "kind", "flags", "host", "title", "capture_id"])
        for r in finds:
            w.writerow([r.get("at", ""), r.get("kind", ""),
                        " ".join(r.get("flags", [])), r.get("host") or "",
                        (r.get("title") or "")[:120], r.get("capture_id", "")])

    # 3. the journal itself, which is the only thing that cannot be rebuilt
    # .txt because many upload and share targets reject unfamiliar extensions.
    # The content is newline-delimited JSON regardless of what it is called.
    jp = os.path.join(EXPORT_DIR, "journal-%s.txt" % stamp)
    if os.path.exists(JOURNAL):
        with open(JOURNAL, "rb") as a, open(jp, "wb") as b:
            b.write(a.read())

    print(buf.getvalue())
    print("exported to Download/trellis-export/")
    for f in (rp, cp, jp):
        if os.path.exists(f):
            print("  %-34s %6d bytes" % (os.path.basename(f), os.path.getsize(f)))
    try:
        subprocess.run(["termux-share", "-a", "send", rp], check=False, timeout=10)
    except Exception:
        pass


def recheck():
    """Re-run captures whose verdict may have been an artifact of the probe's
    own request pattern rather than a fact about the object. Findings are
    appended, never rewritten: the journal keeps both readings."""
    ensure_dirs()
    if not os.path.exists(JOURNAL):
        print("no journal yet")
        return
    rows = [json.loads(l) for l in open(JOURNAL) if l.strip()]

    suspect = {"producer_refused", "unreachable"}
    bad = {r["capture_id"] for r in rows
           if r.get("event") == "finding" and r.get("kind") in suspect}
    if not bad:
        print("nothing to recheck")
        return

    urls, done = {}, set()
    for r in rows:
        if r.get("event") == "reference" and r.get("capture_id") in bad:
            u = r.get("final_url") or r.get("shared_url")
            if u:
                urls[r["capture_id"]] = u

    print("rechecking %d refused captures with browser-shaped headers\n" % len(urls))
    for cid, u in urls.items():
        if u in done:
            continue
        done.add(u)
        print("  " + u[:70])
        probe(u)
        time.sleep(5)
    print("\ndone. originals are preserved; new findings appended.")


CONFLICT_PAIR = frozenset({"stable_referent", "producer_refused"})
CONFLICT_RULE = "stable_referent with producer_refused"


# A short, literal list of addresses where possession of the link is the
# access. Unlisted by URL rather than protected by a login, so handing the
# address to anyone hands them the thing.
#
# This is a heuristic and it will miss. It is a list of shapes seen in one
# corpus, not a rule about what a capability is, and there is no way to tell
# from a URL alone whether the far end checks who is asking. It warns; it never
# blocks. `scripts/verify-privacy.py` keeps its own copy for the repository,
# which is a different job on a different tree.
CAPABILITY_PATTERNS = [
    (re.compile(r"claude\.ai/share/", re.I), "Claude share link"),
    # The account segment is load-bearing: a real shared Docs URL is
    # /document/u/0/d/... and a pattern without the optional u/N/ misses it.
    (re.compile(r"docs\.google\.com/[a-z]+/(?:u/\d+/)?d/", re.I), "Google Docs unlisted document"),
    (re.compile(r"drive\.google\.com/(?:u/\d+/)?(file/d/|drive/folders/)", re.I), "Google Drive unlisted item"),
    (re.compile(r"reddit\.com/r/[^/\s]+/s/", re.I), "Reddit share shortlink"),
    (re.compile(r"dropbox\.com/(s|scl)/", re.I), "Dropbox share link"),
    (re.compile(r"[?&](token|auth|key|secret)=[A-Za-z0-9_-]{10,}", re.I), "URL carrying a token"),
]


def capability_reason(url):
    """Why this address might be a capability, or None."""
    for rx, why in CAPABILITY_PATTERNS:
        if rx.search(url or ""):
            return why
    return None


# ---------------------------------------------------------------- redaction

def redactions(rows):
    """Capture ids currently redacted, by replaying the redaction events.

    A redaction is an event like any other, so the sequence stays visible and a
    later `unredact` is a further event rather than an erasure. Last action per
    capture wins."""
    state = {}
    for r in rows:
        if r.get("event") != "redaction":
            continue
        cid = r.get("capture_id")
        if cid and r.get("action") in ("redact", "unredact"):
            state[cid] = r["action"]
    return {c for c, a in state.items() if a == "redact"}


def resolve_targets(rows, tokens):
    """Accept a capture id or an object hash. The operator reads a bundle,
    which names objects by hash and never by capture id, so requiring the
    capture id would mean the thing they are looking at cannot be named."""
    refs = {r.get("capture_id"): r for r in rows if r.get("event") == "reference"}
    known = {r.get("capture_id") for r in rows if r.get("capture_id")}
    by_hash = {}
    for r in rows:
        if r.get("event") != "finding":
            continue
        cid = r.get("capture_id")
        h = r.get("object_hash") or derive_referent(refs.get(cid))[1]
        if h:
            by_hash.setdefault(h, set()).add(cid)
    out, unknown = set(), []
    for t in tokens:
        if t in known:
            out.add(t)
        elif t in by_hash:
            out |= by_hash[t]
        else:
            unknown.append(t)
    return out, unknown


def redact(tokens, action="redact"):
    """Exclude an object from every future export without deleting anything.

    The journal stays append-only. The row remains, the bundle skips it, and
    the count of skipped objects is reported so the export still states its own
    denominator."""
    ensure_dirs()
    if not os.path.exists(JOURNAL):
        print("no journal yet")
        return
    rows = [json.loads(l) for l in open(JOURNAL) if l.strip()]
    cids, unknown = resolve_targets(rows, tokens)
    for u in unknown:
        print("not found in this journal: %s" % u)
    if not cids:
        print("nothing to %s" % action)
        return
    for cid in sorted(cids):
        emit({"event": "redaction", "capture_id": cid, "action": action,
              "instrument": instrument_hash()})
    if action == "redact":
        print("redacted %d capture(s). The rows stay in the journal and the "
              "bundle will skip them." % len(cids))
        print("This does not remove the address from the journal on this")
        print("device. If the address itself is the disclosure, see: purge")
    else:
        print("unredacted %d capture(s). The bundle will include them again."
              % len(cids))
        print("Both events remain in the journal, so the sequence is visible.")


def purge(tokens):
    """Delete rows. This is the one place the append-only rule is broken.

    Redaction keeps an object out of a bundle. It cannot help when the address
    itself is the disclosure and the journal holding it is the problem: an
    unlisted link is a capability, and possession is the access.

    What is given up: no bytes are ever removed. What is kept: the record
    cannot silently lose things. The rewrite appends an event saying that it
    happened, when, and how many rows went, and deliberately not what they
    were, since recording them would defeat the purpose."""
    ensure_dirs()
    if not os.path.exists(JOURNAL):
        print("no journal yet")
        return
    rows = [json.loads(l) for l in open(JOURNAL) if l.strip()]
    cids, unknown = resolve_targets(rows, tokens)
    for u in unknown:
        print("not found in this journal: %s" % u)
    if not cids:
        print("nothing to purge")
        return

    doomed = [r for r in rows if r.get("capture_id") in cids]
    print("\nPURGE rewrites the journal and deletes rows permanently.")
    print("There is no backup, because a backup would keep the addresses.")
    print("%d row(s) across %d capture(s) will be removed."
          % (len(doomed), len(cids)))
    print("Blobs under %s are content-addressed and are NOT touched." % BLOBS)
    print("\nThis is the only command here that is not append-only.")
    if not sys.stdin.isatty():
        print("\nRefusing to run non-interactively. Run it from a shell.")
        return
    try:
        if input("\nType PURGE to confirm: ").strip() != "PURGE":
            print("cancelled, nothing was removed")
            return
    except (EOFError, KeyboardInterrupt):
        print("\ncancelled, nothing was removed")
        return

    kept = [r for r in rows if r.get("capture_id") not in cids]
    tmp = JOURNAL + ".rewrite"
    with open(tmp, "w") as f:
        for r in kept:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, JOURNAL)
    emit({"event": "redaction", "action": "purge",
          "rows_removed": len(doomed), "captures_removed": len(cids),
          "instrument": instrument_hash()})
    print("\nremoved %d row(s) across %d capture(s)" % (len(doomed), len(cids)))
    print("appended a purge record: it says a rewrite happened, when, and how")
    print("many rows went. It does not say what they were.")


def derive_referent(ref):
    """Recover (referent_key, object_hash) from a reference row that predates
    the hashing code.

    `object_hash` is `sha256(referent_key(final_url))[:16]`, a pure function of
    a URL the reference row already carries, so a journal written before that
    code existed can still be joined against another party's bundle, and the
    hashes agree because the function is the same one.

    This is a read-time derivation on purpose. Appending computed rows would
    make the journal a record of what was later worked out rather than of what
    happened, and rewriting rows is forbidden outright: the first corpus is
    evidence that two instruments touched one file, and that evidence is worth
    more than the convenience of a uniform schema.

    Returns (None, None) when the row carries no URL to derive from."""
    if not ref:
        return None, None
    key = ref.get("referent_key")
    if key:
        return key, sha256(key.encode())[:16]
    url = ref.get("final_url") or ref.get("cleaned_url") or ref.get("shared_url")
    if not url:
        return None, None
    return referent_key(url), refhash(url)


def bundle():
    """Emit the small thing: what one party could hand another so that shared
    objects are discoverable. References and hashes only, never payload.

    This is the multi-homing cost claim made measurable. Publishing where
    others are is what makes a party findable, and multi-homing only stays
    rational while it is nearly free. Copyright already forces identity and
    payload apart, so what travels is kilobytes. If payload ever rides along,
    mirroring gets expensive, the gradient toward one host reappears, and
    concentration follows."""
    ensure_dirs()
    if not os.path.exists(JOURNAL):
        print("no journal yet")
        return

    rows = [json.loads(l) for l in open(JOURNAL) if l.strip()]
    refs = {r["capture_id"]: r for r in rows if r.get("event") == "reference"}
    redacted_cids = redactions(rows)

    objs = {}
    derived_rows, derived_hashes = 0, set()
    hashed_rows = 0
    findings_total = 0
    # A bundle that quietly drops findings understates its own denominator,
    # which is the defect the discard bug already was. Count what is left out
    # and why, rather than reporting only what survived.
    excluded = {"no_reference_row": 0, "no_address": 0}
    redacted_objs = set()
    for r in rows:
        if r.get("event") != "finding":
            continue
        findings_total += 1
        ref = refs.get(r.get("capture_id"))
        h = r.get("object_hash")
        key = ref.get("referent_key") if ref else None
        if not h or not key:
            dk, dh = derive_referent(ref)
            key = key or dk
            if not h and dh:
                h = dh
                derived_rows += 1
                derived_hashes.add(h)
        if not h:
            # No identifier exists and none may be invented. A file share has
            # a reference row carrying no address, because the object arrived
            # as payload with nothing to resolve. A no_reference capture has no
            # reference row at all, because the share carried no URL.
            excluded["no_reference_row" if ref is None else "no_address"] += 1
            continue
        if r.get("capture_id") in redacted_cids:
            # One redacted sighting redacts the object. A partially exported
            # object is still exported, and the operator asked for it gone.
            redacted_objs.add(h)
            continue
        hashed_rows += 1
        e = objs.setdefault(h, {"h": h, "ref": key, "alt": {}, "kinds": [],
                                "n": 0, "srcs": set()})
        if not e["ref"]:
            e["ref"] = key
        e["n"] += 1
        # The address as it was recorded, before normalization. Two sightings
        # of one object are a different result depending on whether the
        # addresses were identical or merely equivalent, and the bundle cannot
        # tell them apart after the fact because it keeps only the key.
        if ref:
            src = (ref.get("final_url") or ref.get("cleaned_url")
                   or ref.get("shared_url"))
            if src:
                e["srcs"].add(src)
        kind = r.get("kind", "unknown")
        if kind not in e["kinds"]:
            e["kinds"].append(kind)
        for k, v in (r.get("alt_referents") or {}).items():
            e["alt"][v["hash"]] = v["url"]

    # An object with any redacted sighting leaves entirely, including
    # sightings that were not themselves redacted.
    for h in redacted_objs:
        o = objs.pop(h, None)
        if o:
            hashed_rows -= o["n"]

    # A verdict describes an encounter, not an object. Four sightings of one
    # object on one device in one morning produced both stable_referent and
    # producer_refused, and the bundle showed them as an unremarkable set.
    #
    # One pair, stated once, and deliberately not a compatibility matrix over
    # the whole vocabulary. These two disagree about whether the payload was
    # obtained, which is a question with one answer per encounter. Everything
    # else stays uncounted, because multiplicity is not contradiction:
    # client_rendered beside soft_refusal is two true things about two
    # encounters, and nothing here is equipped to say otherwise.
    multi_kind = sum(1 for o in objs.values() if len(o["kinds"]) > 1)
    conflicting = sum(1 for o in objs.values()
                      if CONFLICT_PAIR <= set(o["kinds"]))

    # Two sightings of one object are different results depending on whether
    # the addresses were the same or merely equivalent, and only the journal
    # can say which.
    repeat_same = sum(o["n"] - 1 for o in objs.values()
                      if o["n"] > 1 and len(o["srcs"]) <= 1)
    repeat_norm = sum(o["n"] - 1 for o in objs.values()
                      if o["n"] > 1 and len(o["srcs"]) > 1)
    collapsed_by_norm = sum(1 for o in objs.values() if len(o["srcs"]) > 1)

    out = {
        "v": 0,
        "objects": [
            {"h": o["h"], "ref": o["ref"], "seen": o["n"],
             "kinds": o["kinds"], "alt": o["alt"]}
            for o in sorted(objs.values(), key=lambda x: x["ref"] or "")
        ],
        # What this bundle is not carrying, so a reader can see the whole
        # denominator rather than only the part that survived.
        "findings": findings_total,
        "excluded": {
            "no_address": excluded["no_address"],
            "no_reference_row": excluded["no_reference_row"],
            "redacted": len(redacted_objs),
            "total": (excluded["no_address"] + excluded["no_reference_row"]
                      + len(redacted_objs)),
        },
        # A stranger receiving this cannot otherwise see that an object's
        # verdict list disagrees with itself. Reported, not resolved.
        "verdicts": {
            "multi_kind": multi_kind,
            "conflicting": conflicting,
            "conflict_rule": CONFLICT_RULE,
        },
    }

    path = os.path.join(EXPORT_DIR, "bundle.json")
    try:
        os.makedirs(EXPORT_DIR, exist_ok=True)
        blob = json.dumps(out, separators=(",", ":"))
        open(path, "w").write(blob)
    except Exception as e:
        print("cannot write bundle (%s)" % e)
        return

    n = len(out["objects"])
    print("%d objects, %d bytes" % (n, len(blob)))
    print("from %d finding(s), of which %d carried a resolvable reference."
          % (findings_total, hashed_rows))
    if n:
        print("%.0f bytes per object" % (len(blob) / n))
        print("\n1,000 objects would be roughly %.0f KB" % (len(blob) / n * 1000 / 1024))
        print("which is the whole multi-homing argument: at this size,")
        print("publishing to five hosts costs nothing, so there is no")
        print("gradient pulling anyone toward a single one.")

    if derived_rows:
        print("\n%d finding row(s) were hashed at read time, and produced %d "
              "distinct object(s)." % (derived_rows, len(derived_hashes)))
        print("Those rows carried no object_hash, which means this journal")
        print("predates the hashing code. The journal was not modified. The")
        print("derivation is the same function the probe now runs, so the")
        print("hashes join.")

    ex = out["excluded"]
    if ex["total"]:
        print("\n%d finding(s) are not in this bundle:" % ex["total"])
        if ex["no_address"]:
            print("  %d with no address. A file share arrives as payload with"
                  % ex["no_address"])
            print("     nothing to resolve, so there is no referent to hash and")
            print("     none may be invented. Local structure attaches; a second")
            print("     party still has no way to point at the same object.")
        if ex["no_reference_row"]:
            print("  %d with no reference row at all. The share carried no URL."
                  % ex["no_reference_row"])
        if ex["redacted"]:
            print("  %d object(s) redacted by the operator. The rows are still"
                  % ex["redacted"])
            print("     in the journal; only the export skips them.")
        print("  The bundle is %d of %d findings. The other %d are the "
              "hypothesis"
              % (hashed_rows, findings_total, ex["total"]))
        print("  break, not a gap in the export.")

    repeats = [o for o in out["objects"] if o["seen"] > 1]
    if repeats:
        again = sum(o["seen"] - 1 for o in repeats)
        print("\n%d object(s) were encountered more than once, %d repeat "
              "sighting(s)." % (len(repeats), again))
        print("%d reference(s) collapsed to %d object(s), and the collapse "
              "splits two ways:" % (hashed_rows, n))
        print("  %d from the same address recorded again" % repeat_same)
        print("  %d from distinct addresses normalizing to one referent key"
              % repeat_norm)
        if collapsed_by_norm:
            print("\n%d object(s) were reached by more than one address. That is"
                  % collapsed_by_norm)
            print("what referent hashing is for: the same object reached by two")
            print("different addresses is one object, and nothing had to agree")
            print("for that to hold.")
        else:
            print("\nNo object here was reached by two different addresses, so")
            print("this journal does not yet show normalization doing work")
            print("beyond removing exact repeats.")
            if not sum(len(o["alt"]) for o in out["objects"]):
                print("Every alternate referent field is empty as well, so")
                print("nothing was matched through a canonical or og:url")
                print("variant either.")

    if multi_kind:
        print("\n%d object(s) carry more than one verdict across their "
              "sightings," % multi_kind)
        print("of which %d pair %s." % (conflicting, CONFLICT_RULE))
        print("A verdict describes an encounter rather than an object, and")
        print("this bundle exports them as though they described objects.")
        if conflicting:
            print("Those two disagree about whether the payload was obtained.")
            print("Nothing here resolves that or picks a winner.")
        print("Multiplicity is not contradiction: only this one pair is")
        print("counted as conflicting, and the rest may be several true")
        print("things about several encounters.")

    flagged = []
    for o in out["objects"]:
        why = capability_reason(o["ref"] or "")
        if not why:
            for u in (o["alt"] or {}).values():
                why = capability_reason(u)
                if why:
                    break
        if why:
            flagged.append((o["h"], o["ref"], why))
    if flagged:
        print("\n%d object(s) in this bundle look like capability links, where"
              % len(flagged))
        print("possession of the address is the access. This file is about to")
        print("be handed to someone.")
        for h, ref, why in flagged:
            print("  %s  %s" % (h, why))
            print("     %s" % ref)
        print("\nRedact any you did not mean to hand over:")
        print("  probe.py redact %s" % " ".join(h for h, _, _ in flagged))
        print("\nThis is a heuristic over a short list of known shapes. It will")
        print("miss capabilities it has not been taught, and nothing about a URL")
        print("says whether the far end checks who is asking. Absence of a")
        print("warning here is not a clearance.")

    print("\nwritten to Download/trellis-export/bundle.json")

    alts = sum(len(o["alt"]) for o in out["objects"])
    if alts:
        print("\n%d alternate referents recorded as equivalence candidates." % alts)
        print("A hash match on one is a proposal, never an assertion:")
        print("whether two addresses denote one object is a judgment,")
        print("and it belongs to whoever is doing the judging.")


def join(other_path):
    """Compare a bundle from elsewhere against this one. The join is set
    intersection over independently derived hashes: neither party had to
    agree with the other, or know the other existed."""
    ensure_dirs()
    try:
        theirs = json.load(open(os.path.expanduser(other_path)))
    except Exception as e:
        print("cannot read %s (%s)" % (other_path, e))
        return

    bp = os.path.join(EXPORT_DIR, "bundle.json")
    if not os.path.exists(bp):
        print("no local bundle yet, run: probe.py bundle")
        return
    mine = json.load(open(bp))

    mh = {o["h"]: o for o in mine["objects"]}
    th = {o["h"]: o for o in theirs.get("objects", [])}
    shared = set(mh) & set(th)

    print("mine %d, theirs %d, shared %d" % (len(mh), len(th), len(shared)))
    for h in sorted(shared):
        print("  " + (mh[h]["ref"] or h)[:70])

    # candidate equivalences: their alternates matching my primaries
    cand = []
    for o in theirs.get("objects", []):
        for ah in (o.get("alt") or {}):
            if ah in mh and o["h"] not in shared:
                cand.append((mh[ah]["ref"], o["ref"]))
    if cand:
        print("\ncandidate equivalences, for you to accept or reject:")
        for a, b in cand:
            print("  %s\n    ~ %s" % ((a or "")[:64], (b or "")[:64]))


def tally():
    """One-line running rate, shown on every capture so the journal never
    needs to be read to know where the gate stands."""
    try:
        finds = [json.loads(l) for l in open(JOURNAL) if '"finding"' in l]
        finds = [r for r in finds if r.get("event") == "finding"]
        if not finds:
            return ""
        n = len(finds)
        c = {}
        for r in finds:
            c[r["kind"]] = c.get(r["kind"], 0) + 1
        top = sorted(c.items(), key=lambda x: -x[1])[:3]
        return "n=%d  " % n + "  ".join("%s %d%%" % (k[:12], round(100 * v / n)) for k, v in top)
    except Exception:
        return ""


def report():
    """Read the journal. Every number here is derived, nothing is stored."""
    if not os.path.exists(JOURNAL):
        print("No journal yet.")
        return
    rows = [json.loads(l) for l in open(JOURNAL) if l.strip()]
    finds = [r for r in rows if r.get("event") == "finding"]
    caps = [r for r in rows if r.get("event") == "capture"]

    print("captures: %d   findings: %d" % (len(caps), len(finds)))
    if not finds:
        return

    kinds, flags, hosts = {}, {}, {}
    for r in finds:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
        for x in r.get("flags", []):
            flags[x] = flags.get(x, 0) + 1
        h = r.get("host")
        if h:
            hosts.setdefault(h, [0, 0])
            hosts[h][0] += 1
            if r["kind"] == "stable_referent":
                hosts[h][1] += 1

    print("\nverdicts")
    for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
        print("  %-22s %3d  %5.1f%%" % (k, v, 100.0 * v / len(finds)))

    print("\nflags")
    for k, v in sorted(flags.items(), key=lambda x: -x[1]):
        print("  %-22s %3d" % (k, v))

    print("\nby host (stable / total)")
    for h, (t, s) in sorted(hosts.items(), key=lambda x: -x[1][0])[:20]:
        print("  %-34s %d/%d" % (h[:34], s, t))

    n = len(finds)
    stable = kinds.get("stable_referent", 0)
    client = kinds.get("client_rendered", 0)
    refused = kinds.get("producer_refused", 0) + kinds.get("soft_refusal", 0)
    recov = kinds.get("recovered_from_archive", 0)
    noref = kinds.get("no_reference", 0)
    pnr = kinds.get("payload_no_referent", 0)
    per = kinds.get("payload_with_embedded_referent", 0)
    print("\nA-1 reading (n=%d)" % n)
    print("  stable referent, structure attaches      %5.1f%%" % (100.0 * stable / n))
    print("  reference stable, payload elsewhere      %5.1f%%" % (100.0 * client / n))
    print("  producer declined (status or stub)       %5.1f%%" % (100.0 * refused / n))
    print("  no reference emitted at all              %5.1f%%" % (100.0 * noref / n))
    print("  payload shared, no resolvable referent    %5.1f%%" % (100.0 * pnr / n))
    print("  payload shared, referent inside it        %5.1f%%" % (100.0 * per / n))
    print("  payload recovered from archive           %5.1f%%" % (100.0 * recov / n))
    print("\n  gate reads on line 1. line 2 is a fetch problem with known")
    print("  workarounds. line 3 is copyright and access. lines 4 and 5 are")
    print("  the hypothesis break: local structure attaches and no one else")
    print("  can point at the same object. line 6 is the escape hatch.")


def recent(n=12):
    if not os.path.exists(JOURNAL):
        print("no journal yet")
        return
    rows = [json.loads(l) for l in open(JOURNAL) if '"finding"' in l]
    for r in [x for x in rows if x.get("event") == "finding"][-n:]:
        print("%-17s %-34s %s" % (
            r["kind"][:16],
            (",".join(r.get("flags", [])) or "clean")[:33],
            (r.get("title") or r.get("host", ""))[:40]))


def main():
    ensure_dirs()
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        report()
        return
    if len(sys.argv) > 1 and sys.argv[1] == "recent":
        recent()
        return
    if len(sys.argv) > 2 and sys.argv[1] == "file":
        probe_file(sys.argv[2])
        return
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        scan(sys.argv[2] if len(sys.argv) > 2 else None)
        return
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        export()
        return
    if len(sys.argv) > 1 and sys.argv[1] == "recheck":
        recheck()
        return
    if len(sys.argv) > 1 and sys.argv[1] == "bundle":
        bundle()
        return
    if len(sys.argv) > 2 and sys.argv[1] == "join":
        join(sys.argv[2])
        return
    if len(sys.argv) > 2 and sys.argv[1] == "redact":
        redact(sys.argv[2:])
        return
    if len(sys.argv) > 2 and sys.argv[1] == "unredact":
        redact(sys.argv[2:], action="unredact")
        return
    if len(sys.argv) > 2 and sys.argv[1] == "purge":
        purge(sys.argv[2:])
        return
    text = sys.stdin.read() if not sys.stdin.isatty() else " ".join(sys.argv[1:])
    if not text.strip():
        print("usage: probe.py <url|text>   |   probe.py report")
        print("       probe.py redact <capture_id|object_hash> ...")
        print("       probe.py unredact <capture_id|object_hash> ...")
        print("       probe.py purge <capture_id|object_hash> ...  (deletes)")
        return
    probe(text.strip())


if __name__ == "__main__":
    main()
