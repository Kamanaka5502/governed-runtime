#!/usr/bin/env python3
"""
MODEL REVEAL OBSERVER
Reads events.jsonl and reveals behavioral structure through metrics.
No mutation. Pure observation.
"""

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone

EVENT_FILE = "events.jsonl"


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_events(path):
    events = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except Exception:
                continue
    return events


def summarize(events):
    total = len(events)

    types = Counter()
    actors = Counter()
    outcomes = Counter()
    transitions = Counter()

    prev_type = None

    for e in events:
        t = e.get("type", "unknown")
        a = e.get("actor", "unknown")
        o = e.get("outcome", "unknown")

        types[t] += 1
        actors[a] += 1
        outcomes[o] += 1

        if prev_type is not None:
            transitions[(prev_type, t)] += 1
        prev_type = t

    return {
        "total": total,
        "types": types,
        "actors": actors,
        "outcomes": outcomes,
        "transitions": transitions,
    }


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def reveal():
    print("=== MODEL REVEAL OBSERVER ===")
    print("ts:", now_iso())

    events = load_events(EVENT_FILE)

    if not events:
        print("No events found.")
        return

    s = summarize(events)

    print_section("GLOBAL")
    print("total_events:", s["total"])

    print_section("EVENT TYPE DISTRIBUTION")
    for k, v in s["types"].most_common():
        print(f"{k:25s} {v}")

    print_section("ACTOR DISTRIBUTION")
    for k, v in s["actors"].most_common():
        print(f"{k:25s} {v}")

    print_section("OUTCOME DISTRIBUTION")
    for k, v in s["outcomes"].most_common():
        print(f"{k:25s} {v}")

    print_section("TOP TRANSITIONS (behavior flow)")
    for (a, b), v in s["transitions"].most_common(20):
        print(f"{a} -> {b} : {v}")

    print_section("INTERPRETATION")
    print("The model is revealed through repetition, transitions, and stability.")
    print("Patterns above = behavioral skeleton, not hidden identity.")
    print("Governance + memory = observable structure.")

    print("\n=== REVEAL COMPLETE ===")


if __name__ == "__main__":
    reveal()
