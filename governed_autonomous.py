import time
import json
from datetime import datetime

# 🔒 canonical hashing + payload rules
from verify_events import canonical_payload, sha256_hex

EVENT_FILE = "events.jsonl"
HEAD_FILE = "events.head"

GENESIS = "0" * 64


def load_head():
    try:
        with open(HEAD_FILE, "r", encoding="utf-8") as f:
            return f.read().strip() or GENESIS
    except FileNotFoundError:
        return GENESIS


def write_head(h):
    with open(HEAD_FILE, "w", encoding="utf-8") as f:
        f.write(h + "\n")


def append_event(rec):
    payload = canonical_payload(rec)
    h = sha256_hex(payload)
    rec["hash"] = h

    with open(EVENT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n")

    write_head(h)
    return h


def make_cycle_event(cycle, prev):
    return {
        "actor": "runtime",
        "type": "cycle_start",
        "cycle": cycle,
        "ts": datetime.utcnow().timestamp(),
        "prev": prev,
        "outcome": "ok",
        "mode": "AUTONOMOUS_X5"
    }


def run_autonomous_x5():
    print("=== AUTONOMOUS GOVERNED RUNTIME (X5 PUSH) ===")

    prev = load_head()
    print("Starting head:", prev)

    for i in range(1, 6):
        print(f"[CYCLE {i}] running...")

        rec = make_cycle_event(i, prev)
        prev = append_event(rec)

        print(f"[CYCLE {i}] head -> {prev}")

        time.sleep(1)

    print("=== X5 COMPLETE ===")


if __name__ == "__main__":
    run_autonomous_x5()
