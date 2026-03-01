#!/usr/bin/env python3

import json
import hashlib
from datetime import datetime, timezone

MAIN_FILE = "events.jsonl"
MAIN_HEAD_FILE = "events.head"

SAFE_FILE = "events.saferoom.jsonl"
SAFE_HEAD_FILE = "events.saferoom.head"


# -------------------------------------------------
# utils
# -------------------------------------------------

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def sha256_hex(payload: bytes):
    return hashlib.sha256(payload).hexdigest()

def canonical_payload(rec):
    clean = dict(rec)
    clean.pop("hash", None)
    return json.dumps(
        clean,
        sort_keys=True,
        separators=(",", ":")
    ).encode()

def read_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [json.loads(x) for x in f if x.strip()]
    except FileNotFoundError:
        return []

def write_lines(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, separators=(",", ":")) + "\n")

def load_head(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip() or None
    except FileNotFoundError:
        return None

def write_head(path, head):
    with open(path, "w", encoding="utf-8") as f:
        f.write(head or "")


# -------------------------------------------------
# promotion logic
# -------------------------------------------------

def promote():
    main = read_lines(MAIN_FILE)
    safe = read_lines(SAFE_FILE)

    main_head = load_head(MAIN_HEAD_FILE)

    print("=== PROMOTE SAFEROOM → MAIN ===")
    print("main_records:", len(main))
    print("safe_records:", len(safe))
    print("starting_main_head:", main_head)

    prev = main_head

    promoted = 0

    for r in safe:
        r = dict(r)

        # normalize chain linkage
        r.pop("prev_hash", None)
        r["prev"] = prev

        # mark provenance
        r["lane"] = "promoted_saferoom"
        r["promoted_ts"] = now_iso()

        payload = canonical_payload(r)
        h = sha256_hex(payload)

        r["hash"] = h
        prev = h

        main.append(r)
        promoted += 1

    write_lines(MAIN_FILE, main)
    write_head(MAIN_HEAD_FILE, prev)

    print("PROMOTION COMPLETE")
    print("promoted_records:", promoted)
    print("new_head:", prev)

    return 0


if __name__ == "__main__":
    raise SystemExit(promote())
