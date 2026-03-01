#!/usr/bin/env bash
set -euo pipefail

echo "═══════════════════════════════════════════════════════"
echo "   FULL CAT BUILD — GOVERNED RUNTIME CORE (NO NANO)"
echo "═══════════════════════════════════════════════════════"

# ------------------------------------------------------------------
# utils_time.py
# ------------------------------------------------------------------
cat > utils_time.py <<'PYEOF'
#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime, timezone

def now_iso() -> str:
    # timezone-aware UTC (avoids utcnow deprecation)
    return datetime.now(timezone.utc).isoformat()
PYEOF
chmod +x utils_time.py

# ------------------------------------------------------------------
# verify_events.py
# ------------------------------------------------------------------
cat > verify_events.py <<'PYEOF'
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
PYEOF
chmod +x verify_events.py

# ------------------------------------------------------------------
# rechain_events.py
# ------------------------------------------------------------------
cat > rechain_events.py <<'PYEOF'
#!/usr/bin/env python3
from __future__ import annotations

import sys
import json
from typing import Any, Dict, List
from verify_events import legacy_hash

def write_head(head_path: str, head: str) -> None:
    with open(head_path, "w", encoding="utf-8") as f:
        f.write(head + "\n")

def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: python rechain_events.py <in_events.jsonl> <out_events.jsonl> <head_file>")
        return 2

    in_path, out_path, head_path = sys.argv[1], sys.argv[2], sys.argv[3]

    prev = "0" * 64
    out_lines: List[str] = []
    count = 0

    with open(in_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            rec: Dict[str, Any] = json.loads(line)
            rec.pop("prev_hash", None)

            rec["prev"] = prev
            rec["hash"] = legacy_hash(rec)

            prev = rec["hash"]
            out_lines.append(json.dumps(rec, ensure_ascii=False) + "\n")
            count += 1

    with open(out_path, "w", encoding="utf-8") as out:
        out.writelines(out_lines)

    write_head(head_path, prev)

    print("RECHAIN OK")
    print("in_records:", count)
    print("out_records:", count)
    print("head:", prev)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
PYEOF
chmod +x rechain_events.py

# ------------------------------------------------------------------
# governor.py
# ------------------------------------------------------------------
cat > governor.py <<'PYEOF'
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any, Dict

from utils_time import now_iso
from verify_events import legacy_hash, verify

EVENTS_DEFAULT = "events.jsonl"
HEAD_DEFAULT = "events.head"

def read_head(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip() or ("0" * 64)
    except FileNotFoundError:
        return "0" * 64

def write_head(path: str, h: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(h + "\n")

def append_line(path: str, rec: Dict[str, Any]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

def add_event(event_path: str, head_path: str, prev: str, rec: Dict[str, Any]) -> str:
    rec["prev"] = prev
    rec["hash"] = legacy_hash(rec)
    append_line(event_path, rec)
    write_head(head_path, rec["hash"])
    return rec["hash"]

def cycle_block(event_path: str, head_path: str, prev: str, cycle_id: int, do_model: bool) -> str:
    prev = add_event(event_path, head_path, prev, {
        "ts": now_iso(),
        "type": "cycle_start",
        "actor": "runtime",
        "cycle": cycle_id,
        "outcome": "ok",
    })

    prev = add_event(event_path, head_path, prev, {
        "ts": now_iso(),
        "type": "model_call",
        "actor": "router" if do_model else "runtime",
        "cycle": cycle_id,
        "outcome": "ok" if do_model else "allow",
    })

    prev = add_event(event_path, head_path, prev, {
        "ts": now_iso(),
        "type": "classification",
        "actor": "openai" if do_model else "runtime",
        "cycle": cycle_id,
        "outcome": "ok" if do_model else "unknown",
    })

    prev = add_event(event_path, head_path, prev, {
        "ts": now_iso(),
        "type": "action_executed",
        "actor": "runtime",
        "cycle": cycle_id,
        "outcome": "ok",
    })

    prev = add_event(event_path, head_path, prev, {
        "ts": now_iso(),
        "type": "cycle_end",
        "actor": "runtime",
        "cycle": cycle_id,
        "outcome": "ok",
    })

    return prev

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", default=EVENTS_DEFAULT)
    ap.add_argument("--head", default=HEAD_DEFAULT)
    ap.add_argument("--cycles", type=int, default=5)
    ap.add_argument("--sleep", type=float, default=0.0)
    ap.add_argument("--do-model", action="store_true")
    args = ap.parse_args()

    print("=== GOVERNOR (A+B) ===")
    print("events:", args.events)
    print("head:", args.head)

    # PRE-VERIFY (fail closed)
    if os.path.exists(args.events):
        rc = verify(args.events, args.head)
        if rc != 0:
            print("PRE-VERIFY FAILED (chain broken). Run rechain_events.py first.")
            return 1

    prev = read_head(args.head)
    print("starting_head:", prev[:16] + "...")
    print("do_model:", bool(args.do_model))
    print("cycles:", args.cycles)

    for i in range(1, args.cycles + 1):
        prev = cycle_block(args.events, args.head, prev, i, bool(args.do_model))
        print(f"[CYCLE {i}] head -> {prev[:16]}...")
        if args.sleep:
            time.sleep(args.sleep)

    # POST-VERIFY
    rc = verify(args.events, args.head)
    if rc != 0:
        print("POST-VERIFY FAILED")
        return 1

    print("=== GOVERNOR COMPLETE ===")
    print("final_head:", prev)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
PYEOF
chmod +x governor.py

echo ""
echo "═══════════════════════════════════════════════════════"
echo " BUILD COMPLETE (FULL CAT MODE)"
echo " Next:"
echo "   python verify_events.py"
echo "   python governor.py --cycles 5 --do-model"
echo "   python verify_events.py"
echo "═══════════════════════════════════════════════════════"

