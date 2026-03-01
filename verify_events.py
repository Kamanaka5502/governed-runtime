#!/usr/bin/env python3
import json
import hashlib
import sys

EVENT_FILE = "events.jsonl"

def canonical_payload(rec):
    r = dict(rec)
    r.pop("hash", None)
    return json.dumps(r, sort_keys=True, separators=(",", ":"))

def legacy_hash(rec):
    payload = canonical_payload(rec)
    return hashlib.sha256(payload.encode()).hexdigest()

def verify():
    prev_expected = "0" * 64
    ok = True

    with open(EVENT_FILE, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                rec = json.loads(line)
            except Exception as e:
                print(f"JSON ERROR at line {idx}: {e}")
                ok = False
                break

            stored_hash = rec.get("hash")
            if not stored_hash:
                print(f"MISSING HASH at line {idx}")
                ok = False
                break

            prev = rec.get("prev")
            if prev != prev_expected:
                print(f"CHAIN BREAK at line {idx}")
                print(" expected prev:", prev_expected)
                print(" found prev   :", prev)
                ok = False
                break

            calc = legacy_hash(rec)
            if calc != stored_hash:
                print(f"HASH MISMATCH at line {idx}")
                print(" expected:", calc)
                print(" found   :", stored_hash)
                ok = False
                break

            prev_expected = stored_hash

    if ok:
        print("VERIFY OK")
        return 0
    return 1

if __name__ == "__main__":
    raise SystemExit(verify())
