import json
import sys
from typing import List

# 🔒 SINGLE SOURCE OF TRUTH
from verify_events import canonical_payload, sha256_hex

GENESIS = "0" * 64


def read_lines(path: str) -> List[dict]:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def write_lines(path: str, records: List[dict]):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, separators=(",", ":"), sort_keys=True) + "\n")


def main():
    if len(sys.argv) != 4:
        print("Usage: python rechain_events.py <in_events.jsonl> <out_events.jsonl> <head_file>")
        sys.exit(2)

    in_path = sys.argv[1]
    out_path = sys.argv[2]
    head_path = sys.argv[3]

    records_in = read_lines(in_path)

    out = []
    prev = GENESIS

    for r in records_in:
        r = dict(r)

        # normalize linkage
        r.pop("prev_hash", None)
        r["prev"] = prev

        # canonical hash (IDENTICAL to verifier)
        payload = canonical_payload(r)
        h = sha256_hex(payload)

        r["hash"] = h
        prev = h
        out.append(r)

    # write new ledger
    write_lines(out_path, out)

    # write head
    with open(head_path, "w", encoding="utf-8") as f:
        f.write(prev + "\n" if prev else "")

    print("RECHAIN OK")
    print("in_records:", len(records_in))
    print("out_records:", len(out))
    print("head:", prev)


if __name__ == "__main__":
    main()
