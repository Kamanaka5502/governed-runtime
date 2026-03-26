import copy
import hashlib
import json

def stable_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"))

def sha256_hex(data):
    if not isinstance(data, str):
        data = stable_json(data)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def short_hash(value, size=10):
    return value[:size]

class WorldState:
    def __init__(self, ttl):
        self.cycle = 0
        self.mode = "NORMAL"
        self.authority_valid = True
        self.ttl_remaining = ttl
        self.risk_score = 0.18
        self.action_count = 0
        self.blocked_count = 0

    def snapshot(self):
        return {
            "cycle": self.cycle,
            "mode": self.mode,
            "authority_valid": self.authority_valid,
            "ttl_remaining": self.ttl_remaining,
            "risk_score": self.risk_score,
            "action_count": self.action_count,
            "blocked_count": self.blocked_count
        }

class Baseline:
    def __init__(self, state):
        self.state = state

    def tick(self):
        self.state.cycle += 1
        self.state.ttl_remaining -= 1
        self.state.risk_score = min(1.0, self.state.risk_score + 0.07)

        if self.state.ttl_remaining <= 0:
            self.state.authority_valid = False

    def act(self):
        self.state.action_count += 1
        return "EXECUTE (no re-check)"

class Governed:
    def __init__(self, state):
        self.state = state
        self.head = "GENESIS"

    def tick(self):
        self.state.cycle += 1
        self.state.ttl_remaining -= 1
        self.state.risk_score = min(1.0, self.state.risk_score + 0.07)

        if self.state.ttl_remaining <= 0:
            self.state.authority_valid = False

    def check(self):
        return {
            "authority": self.state.authority_valid,
            "ttl_ok": self.state.ttl_remaining > 0,
            "risk_ok": self.state.risk_score < 0.85
        }

    def commit(self):
        checks = self.check()

        if all(checks.values()):
            decision = "ALLOW"
            self.state.action_count += 1
            reason = "valid"
        else:
            decision = "BLOCK"
            self.state.blocked_count += 1
            failed = [k for k, v in checks.items() if not v]
            reason = "failed: " + ",".join(failed)

        state_hash = sha256_hex(self.state.snapshot())

        receipt = {
            "cycle": self.state.cycle,
            "decision": decision,
            "reason": reason,
            "parent": self.head,
            "state_hash": state_hash
        }

        self.head = sha256_hex(receipt)

        return decision, reason, short_hash(self.head)

cycles = 14
expiry = 7

b_state = WorldState(expiry)
g_state = copy.deepcopy(b_state)

baseline = Baseline(b_state)
governed = Governed(g_state)

print("=== DRIFT VS GOVERNED DEMO ===\n")

for i in range(cycles):
    baseline.tick()
    governed.tick()

    b_result = baseline.act()
    g_decision, g_reason, g_hash = governed.commit()

    stale = ""
    if not baseline.state.authority_valid:
        stale = " <-- STALE BUT STILL EXECUTED"

    print(f"[BASELINE] cycle={baseline.state.cycle} ttl={baseline.state.ttl_remaining} "
          f"auth={baseline.state.authority_valid} → {b_result}{stale}")

    print(f"[GOVERNED] cycle={governed.state.cycle} → {g_decision} "
          f"({g_reason}) receipt={g_hash}\n")

print("\n=== SUMMARY ===")
print("Baseline actions:", baseline.state.action_count)
print("Governed actions:", governed.state.action_count)
print("Governed blocked:", governed.state.blocked_count)
