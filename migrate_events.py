#!/usr/bin/env python3
import json, sys, os, hashlib, hmac

"""
MIGRATE events.jsonl -> canonical chained log v2

What it does:
- Reads an existing events.jsonl (any mix of legacy fields)
- Normalizes chain linkage to a single field: "prev"
  * If record has "prev" use it
  * Else if it has "prev_hash" use that
  * Else genesis record gets prev="" (empty string)
- Recomputes sha256 "hash" over canonical JSON payload (excluding hash/hmac)
- Optionally recomputes HMAC-SHA256 over the same payload if HMAC_KEY is set
- Writes a new JSONL file with consistent schema + a new head file
"""

def canonical_payload(rec: dict) -> bytes:
    # hash/hmac must NOT be included in the payload that is hashed
    rc = dict(rec)
    rc.pop("hash", None)
    rc.pop("hmac", None)
    # stable serialization
    return json.dumps(rc, sort_keys=True, separators=(",", ":")).encode("utf-8")

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def hmac_hex(key: bytes, b: bytes) -> str:
    return hmac.new(key, b, hashlib.sha256).hexdigest()

def migrate(in_path: str, out_path: str, head_path: str):
    HMAC_KEY = os.environ.get("EVENT_HMAC_KEY", "").encode("utf-8")
    use_hmac = bool(HMAC_KEY)

    last_hash = ""  # genesis prev
    count = 0

    with open(in_path, "r", encoding="utf-8") as fin, open(out_path, "w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue

            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                # skip garbage lines, but do NOT silently succeed
                raise RuntimeError("Bad JSON line encountered in input log.")

            # --- normalize chain field ---
            if "prev" in rec and rec["prev"] is not None:
                prev = rec.get("prev", "")
            elif "prev_hash" in rec and rec["prev_hash"] is not None:
                prev = rec.get("prev_hash", "")
            else:
                prev = last_hash or ""

            rec["prev"] = prev
            rec.pop("prev_hash", None)

            # --- recompute hash/hmac deterministically ---
            payload = canonical_payload(rec)
            rec["hash"] = sha256_hex(payload)
            if use_hmac:
                rec["hmac"] = hmac_hex(HMAC_KEY, payload)
            else:
                rec.pop("hmac", None)

            fout.write(json.dumps(rec, separators=(",", ":")) + "\n")

            last_hash = rec["hash"]
            count += 1

    # write new head
    with open(head_path, "w", encoding="utf-8") as fh:
        fh.write(last_hash)

    print("MIGRATION OK")
    print("records:", count)
    print("head:", last_hash)
    print("hmac_enabled:", use_hmac)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python migrate_events.py <in_events.jsonl> <out_events.jsonl>")
        sys.exit(2)

    in_path = sys.argv[1]
    out_path = sys.argv[2]
    head_path = "events.head"

    migrate(in_path, out_path, head_path)
