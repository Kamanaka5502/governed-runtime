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
