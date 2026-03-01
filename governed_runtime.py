#!/usr/bin/env python3

# ==============================================================
# GOVERNED RUNTIME + OPENAI
# FULL CAT VERSION
# K* DAMPING + SHA256 CHAINED LOG
# ==============================================================

import os
import json
import time
import hashlib
import hmac
from datetime import datetime, timezone
from openai import OpenAI

# ==============================================================
# CONFIG
# ==============================================================

MODEL = "gpt-4.1-mini"
EVENT_FILE = "events.jsonl"

TARGET_STABILITY = 1.0
INITIAL_STABILITY = 0.35
K_STAR = 0.15

HMAC_KEY = os.environ.get("EVENT_HMAC_KEY")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ==============================================================
# SECURITY HELPERS
# ==============================================================

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compute_hmac(data: bytes) -> str:
    if not HMAC_KEY:
        return ""
    return hmac.new(HMAC_KEY.encode(), data, hashlib.sha256).hexdigest()


# ==============================================================
# PROBE LOGGER
# ==============================================================

class Probe:

    def __init__(self, file):
        self.file = file
        self.eid = 0
        self.prev_hash = "GENESIS"

    def log(self, actor, event_type, **kwargs):

        self.eid += 1

        record = {
            "eid": self.eid,
            "ts": datetime.now(timezone.utc).timestamp(),
            "actor": actor,
            "type": event_type,
            "prev": self.prev_hash
        }

        record.update(kwargs)

        payload = json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":")
        ).encode()

        record["hash"] = sha256_hex(payload)

        if HMAC_KEY:
            record["hmac"] = compute_hmac(payload)

        self.prev_hash = record["hash"]

        with open(self.file, "a") as f:
            f.write(json.dumps(record) + "\n")


# ==============================================================
# ROUTER
# ==============================================================

class RoutingEngine:

    def __init__(self):
        self.policies = [
            {
                "name": "blocked_keyword",
                "match": lambda text: "forbidden" in text.lower(),
                "decision": "block",
                "safety_level": "critical"
            },
            {
                "name": "default",
                "match": lambda text: True,
                "decision": "allow",
                "safety_level": "low"
            }
        ]

    def classify(self, text):
        for p in self.policies:
            if p["match"](text):
                return p


# ==============================================================
# GOVERNED RUNTIME CORE
# ==============================================================

class GovernedRuntime:

    def __init__(self):

        self.cycle = 0
        self.S = INITIAL_STABILITY

        self.probe = Probe(EVENT_FILE)
        self.router = RoutingEngine()

    # ----------------------------------------------------------

    def call_model(self, prompt):

        resp = client.responses.create(
            model=MODEL,
            input=prompt
        )

        text = resp.output_text

        self.probe.log(
            "openai",
            "model_call",
            cycle=self.cycle,
            model=MODEL,
            response_id=getattr(resp, "id", None),
            outcome="ok"
        )

        return text

    # ----------------------------------------------------------

    def update_stability(self):

        delta = TARGET_STABILITY - self.S
        self.S += K_STAR * delta
        return delta

    # ----------------------------------------------------------

    def run_cycle(self):

        self.cycle += 1

        delta = self.update_stability()

        self.probe.log(
            "runtime",
            "cycle_start",
            cycle=self.cycle,
            S=self.S,
            S_star=TARGET_STABILITY,
            K_star=K_STAR,
            delta=delta,
            outcome="ok"
        )

        prompt = (
            f"System stability={self.S:.3f}. "
            "Generate one short operational action."
        )

        model_text = self.call_model(prompt)

        policy = self.router.classify(model_text)

        self.probe.log(
            "router",
            "classification",
            cycle=self.cycle,
            policy=policy["name"],
            safety_level=policy["safety_level"],
            decision=policy["decision"],
            text=model_text
        )

        if policy["decision"] == "block":

            print(f"[CYCLE {self.cycle}] BLOCKED: {model_text}")

            self.probe.log(
                "runtime",
                "action_blocked",
                cycle=self.cycle,
                outcome="blocked"
            )

        else:

            print(f"[CYCLE {self.cycle}] ACTION: {model_text}")

            self.probe.log(
                "runtime",
                "action_executed",
                cycle=self.cycle,
                outcome="ok",
                text=model_text
            )

        self.probe.log(
            "runtime",
            "cycle_end",
            cycle=self.cycle,
            outcome="ok",
            S=self.S
        )


# ==============================================================
# ENTRYPOINT
# ==============================================================

if __name__ == "__main__":

    rt = GovernedRuntime()

    print("=== GOVERNED RUNTIME + OPENAI (SHA256 CHAINED LOG) ===")
    print("Logging to:", EVENT_FILE)

    for _ in range(8):
        rt.run_cycle()
        time.sleep(1)

    print("\n--- TAIL (last 10 lines) ---")

    try:
        with open(EVENT_FILE, "r") as f:
            lines = f.readlines()[-10:]
            for l in lines:
                print(l.strip())
    except FileNotFoundError:
        print("events.jsonl not found")

