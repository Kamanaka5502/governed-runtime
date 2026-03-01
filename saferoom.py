#!/usr/bin/env python3
"""
SAFEROOM v2
- lane=main: append SAFEROOM_* events into canonical events.jsonl and update events.head
- lane=isolated: append into events.saferoom.jsonl and events.saferoom.head

This script assumes verify_events.py defines:
  - canonical_payload(rec: dict) -> bytes
  - sha256_hex(payload: bytes) -> str

So the hash rules stay IDENTICAL to your verifier.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, UTC
from typing import Dict, Any, List, Optional

# --- canonical hashing: identical to verifier ---
try:
    from verify_events import canonical_payload, sha256_hex
except Exception as e:
    raise SystemExit(
        "Missing/failed import: verify_events.py must export canonical_payload and sha256_hex. "
        f"Import error: {e}"
    )

DEFAULT_EVENT_FILE_MAIN = "events.jsonl"
DEFAULT_HEAD_FILE_MAIN  = "events.head"

DEFAULT_EVENT_FILE_SAFE = "events.saferoom.jsonl"
DEFAULT_HEAD_FILE_SAFE  = "events.saferoom.head"


def now_iso() -> str:
    # UTC-aware; no deprecated utcnow()
    return datetime.now(UTC).isoformat()


def read_head(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            s = f.read().strip()
            return s or None
    except FileNotFoundError:
        return None


def write_head(path: str, h: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(h + "\n")


def append_jsonl(path: str, rec: Dict[str, Any]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, separators=(",", ":"), sort_keys=True) + "\n")


def make_event(event_type: str, cycle: int, prev: Optional[str], **fields: Any) -> Dict[str, Any]:
    rec: Dict[str, Any] = {
        "ts": now_iso(),
        "type": event_type,
        "cycle": cycle,
        "prev": prev,
        **fields,
    }
    payload = canonical_payload(rec)
    rec["hash"] = sha256_hex(payload)
    return rec


def open_saferoom(event_file: str, head_file: str, prev: Optional[str]) -> str:
    rec = make_event("SAFEROOM_OPEN", 0, prev)
    append_jsonl(event_file, rec)
    write_head(head_file, rec["hash"])
    return rec["hash"]


def saferoom_cycles(event_file: str, head_file: str, start_prev: str, n: int, sleep_s: float) -> str:
    prev = start_prev
    for i in range(1, n + 1):
        rec = make_event("SAFEROOM_CYCLE", i, prev)
        append_jsonl(event_file, rec)
        prev = rec["hash"]
        write_head(head_file, prev)
        print(f"[SAFE CYCLE {i}] -> {prev[:16]}...")
        if sleep_s > 0:
            time.sleep(sleep_s)
    return prev


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", choices=["main", "isolated"], default="isolated",
                    help="main=append into events.jsonl/events.head; isolated=separate saferoom ledger")
    ap.add_argument("--push", type=int, default=5, help="number of SAFEROOM_CYCLE events")
    ap.add_argument("--sleep", type=float, default=1.0, help="sleep seconds between cycles (0 disables)")
    args = ap.parse_args()

    if args.lane == "main":
        event_file = DEFAULT_EVENT_FILE_MAIN
        head_file  = DEFAULT_HEAD_FILE_MAIN
    else:
        event_file = DEFAULT_EVENT_FILE_SAFE
        head_file  = DEFAULT_HEAD_FILE_SAFE

    prev = read_head(head_file)

    print("SAFEROOM v2")
    print("lane:", args.lane)
    print("event_file:", event_file)
    print("head_file:", head_file)
    print("starting_head:", prev)

    # 1) open saferoom (writes SAFEROOM_OPEN)
    prev = open_saferoom(event_file, head_file, prev)
    print("(SAFEROOM OPENED)")

    # 2) push cycles
    print("Starting saferoom push")
    prev = saferoom_cycles(event_file, head_file, prev, args.push, args.sleep)
    print("SAFEROOM PUSH COMPLETE")
    print("final_head:", prev)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
