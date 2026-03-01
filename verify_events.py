#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any, Dict, Iterable, Tuple

# Stable exports used by other modules
def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def canonical_payload(rec: Dict[str, Any]) -> bytes:
    r = dict(rec)
    r.pop("hash", None)
    r.pop("prev_hash", None)
    return json.dumps(
        r,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")

def legacy_hash(rec: Dict[str, Any]) -> str:
    return sha256_hex(canonical_payload(rec))

def iter_jsonl(path: str) -> Iterable[Tuple[int, Dict[str, Any]]]:
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            yield idx, json.loads(line)

def verify(event_file: str, head_file: str = "events.head") -> int:
    ok = True
    expected_head = None

    try:
        with open(head_file, "r", encoding="utf-8") as hf:
            expected_head = hf.read().strip() or None
    except FileNotFoundError:
        expected_head = None

    prev_expected = "0" * 64
    last_hash = None

    for idx, rec in iter_jsonl(event_file):
        stored_hash = rec.get("hash")
        if not stored_hash:
            print(f"MISSING HASH at line {idx}")
            ok = False
            break

        prev = rec.get("prev", rec.get("prev_hash"))
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
        last_hash = stored_hash

    if ok and expected_head and last_hash and expected_head != last_hash:
        print("HEAD MISMATCH")
        print(" expected head:", expected_head)
        print(" found head   :", last_hash)
        ok = False

    if ok:
        print("VERIFY OK")
        return 0
    return 1

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("event_file", nargs="?", default="events.jsonl")
    ap.add_argument("--head", dest="head_file", default="events.head")
    args = ap.parse_args()
    return verify(args.event_file, args.head_file)

if __name__ == "__main__":
    raise SystemExit(main())
