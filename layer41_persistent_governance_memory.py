# =====================================================
# Layer 41 — Persistent Governance Memory
# Saves / loads governance learning across runs
# =====================================================

import json
import os

STATE_FILE = "governance_state.json"


class PersistentMemory:

    def __init__(self):
        self.weights = {
            "safe": 1.0,
            "guarded": 1.0,
            "restricted": 1.0
        }
        self.history = []
        self.load()

    # -----------------------------
    # UPDATE MEMORY
    # -----------------------------
    def update(self, boundary, outcome):
        if boundary in self.weights:
            self.weights[boundary] += (outcome - 0.5) * 0.2

        self.history.append({
            "boundary": boundary,
            "outcome": outcome
        })

        if len(self.history) > 100:
            self.history.pop(0)

    # -----------------------------
    # SAVE TO DISK
    # -----------------------------
    def save(self):
        data = {
            "weights": self.weights,
            "history": self.history
        }
        with open(STATE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    # -----------------------------
    # LOAD FROM DISK
    # -----------------------------
    def load(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                self.weights = data.get("weights", self.weights)
                self.history = data.get("history", [])

    # -----------------------------
    # SNAPSHOT
    # -----------------------------
    def snapshot(self):
        return {
            "weights": self.weights,
            "history_count": len(self.history)
        }


# =====================================================
# DEMO RUN
# =====================================================

if __name__ == "__main__":

    mem = PersistentMemory()

    print("=== LAYER 41 — PERSISTENT MEMORY ===")
    print("Loaded:", mem.snapshot())

    # Simulated decisions
    mem.update("safe", 0.9)
    mem.update("guarded", 0.6)
    mem.update("restricted", 0.3)

    print("\nUpdated:", mem.snapshot())

    mem.save()
    print("\nState saved to:", STATE_FILE)
