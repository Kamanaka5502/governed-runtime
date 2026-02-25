# ==========================================================
# Layer 42 — Memory Confidence Gradient
# Adds decay + confidence weighting to persistent policy memory
# ==========================================================

import json
import os

STATE_FILE = "governance_state.json"

class MemoryConfidenceGradient:

    def __init__(self, decay=0.98, learning_rate=0.2):
        self.decay = decay
        self.learning_rate = learning_rate

        self.weights = {
            "safe": 1.0,
            "guarded": 1.0,
            "restricted": 1.0
        }

        self.history = []
        self.load()

    # ------------------------------------------------------
    # MEMORY UPDATE (with decay)
    # ------------------------------------------------------
    def update(self, boundary, outcome):

        # decay existing confidence (old memories fade)
        for k in self.weights:
            self.weights[k] *= self.decay

        # reinforce selected boundary
        if boundary in self.weights:
            adjustment = (outcome - 0.5) * self.learning_rate
            self.weights[boundary] += adjustment

        self.history.append({
            "boundary": boundary,
            "outcome": outcome
        })

        if len(self.history) > 200:
            self.history.pop(0)

    # ------------------------------------------------------
    # SNAPSHOT
    # ------------------------------------------------------
    def snapshot(self):
        return {
            "weights": {k: round(v,3) for k,v in self.weights.items()},
            "history_count": len(self.history)
        }

    # ------------------------------------------------------
    # SAVE / LOAD
    # ------------------------------------------------------
    def save(self):
        data = {
            "weights": self.weights,
            "history": self.history
        }
        with open(STATE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                self.weights = data.get("weights", self.weights)
                self.history = data.get("history", [])

# ==========================================================
# DEMO RUN
# ==========================================================

if __name__ == "__main__":

    mem = MemoryConfidenceGradient()

    print("=== LAYER 42 — MEMORY CONFIDENCE GRADIENT ===")
    print("Loaded:", mem.snapshot())

    # simulate new outcomes
    mem.update("safe", 0.9)
    mem.update("guarded", 0.6)
    mem.update("restricted", 0.3)

    print("\nUpdated:", mem.snapshot())

    mem.save()
    print("\nState saved to:", STATE_FILE)

def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "42_memory_confidence_gradient",
        "status": "active"
    })

    return state
