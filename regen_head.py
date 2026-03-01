#!/usr/bin/env python3
import json, hashlib, sys, argparse

def canonical_payload(evt: dict) -> str:
    """
    Canonicalize the payload for hashing:
    - stable key order
    - compact separators
    - exclude 'hash' (and optionally allow 'prev' to remain)
    """
    d = dict(evt)
    d.pop("hash", None)
    return json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", default="events.jsonl")
    ap.add_argument("--head", default="events.head")
    ap.add_argument("--strict", action="store_true", help="fail if any line is invalid/chain breaks")
    args = ap.parse_args()

    last_hash = None
    line_no = 0

    with open(args.events, "r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            line_no += 1
            evt = json.loads(raw)

            stored = evt.get("hash")
            prev = evt.get("prev")

            calc = sha256_hex(canonical_payload(evt))

            if stored != calc:
                msg = f"HASH MISMATCH at line {line_no}\n  expected: {stored}\n  found   : {calc}"
                if args.strict:
                    print(msg, file=sys.stderr)
                    return 2
                else:
                    # stop at last good; treat remaining as non-canonical/noise
                    break

            if line_no == 1:
                # first record can have prev null/""/None
                pass
            else:
                if prev != last_hash:
                    msg = f"CHAIN BREAK at line {line_no}\n  prev field: {prev}\n  expected  : {last_hash}"
                    if args.strict:
                        print(msg, file=sys.stderr)
                        return 3
                    else:
                        break

            last_hash = stored

    if not last_hash:
        print("No valid events found; cannot write head.", file=sys.stderr)
        return 4

    with open(args.head, "w", encoding="utf-8") as out:
        out.write(last_hash + "\n")

    print("HEAD REGENERATED OK")
    print("head:", last_hash)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
