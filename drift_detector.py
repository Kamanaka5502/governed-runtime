#!/usr/bin/env python3
"""
DRIFT DETECTOR
--------------
Observes behavioral stability of governed runtime.

Outputs:
- event distribution
- transition entropy
- drift score vs baseline
"""

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

EVENT_FILE = "events.jsonl"
BASELINE_FILE = "drift_baseline.json"


# -----------------------------
# helpers
# -----------------------------

def load_events():
    p = Path(EVENT_FILE)
    if not p.exists():
        print("NO EVENTS FILE")
        return []

    events = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except Exception:
                continue
    return events


def event_types(events):
    return [e.get("type", "unknown") for e in events]


def transitions(seq):
    out = Counter()
    for i in range(len(seq) - 1):
        out[(seq[i], seq[i+1])] += 1
    return out


def normalize(counter):
    total = sum(counter.values())
    if total == 0:
        return {}
    return {k: v / total for k, v in counter.items()}


def entropy(dist):
    h = 0.0
    for p in dist.values():
        if p > 0:
            h -= p * math.log2(p)
    return h


# -----------------------------
# baseline logic
# -----------------------------

def save_baseline(stats):
    with open(BASELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


def load_baseline():
    p = Path(BASELINE_FILE)
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def drift_score(current, baseline):
    """
    Simple absolute distance measure.
    """
    keys = set(current.keys()) | set(baseline.keys())
    score = 0.0
    for k in keys:
        score += abs(current.get(k, 0.0) - baseline.get(k, 0.0))
    return score


# -----------------------------
# main analysis
# -----------------------------

def analyze(events):

    types = event_types(events)
    type_count = Counter(types)
    type_dist = normalize(type_count)

    trans_count = transitions(types)
    trans_dist = normalize(trans_count)

    trans_entropy = entropy(trans_dist)

    stats = {
        "total_events": len(events),
        "type_distribution": type_dist,
        "transition_distribution": {
            f"{a}->{b}": v for (a, b), v in trans_dist.items()
        },
        "transition_entropy": trans_entropy,
    }

    return stats


def pretty_print(stats, drift=None):

    print("="*60)
    print("DRIFT DETECTOR REPORT")
    print("="*60)
    print("total_events:", stats["total_events"])
    print()

    print("EVENT DISTRIBUTION")
    print("-"*60)
    for k, v in sorted(stats["type_distribution"].items()):
        print(f"{k:20s} {v:.4f}")
    print()

    print("TRANSITION ENTROPY:", f"{stats['transition_entropy']:.6f}")
    print()

    if drift is not None:
        print("DRIFT SCORE:", f"{drift:.6f}")
        if drift > 0.25:
            print("⚠ BEHAVIORAL DRIFT DETECTED")
        else:
            print("STABLE BEHAVIOR")


def main():

    events = load_events()

    if not events:
        print("No events found.")
        return 1

    current = analyze(events)
    baseline = load_baseline()

    if baseline is None:
        print("NO BASELINE FOUND — creating baseline.")
        save_baseline(current)
        pretty_print(current)
        print("\nBASELINE CREATED.")
        return 0

    drift = drift_score(
        current["type_distribution"],
        baseline.get("type_distribution", {})
    )

    pretty_print(current, drift)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

