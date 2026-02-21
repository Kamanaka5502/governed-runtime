# layer75_adaptive_memory.py
#
# Layer 75 — Adaptive Memory Selector
#
# Chooses preferred strategy based on historical ranking.

class AdaptiveMemory:

    def __init__(self):
        self.best_action = None
        self.best_score = 0.0

    def update(self, ranked_list):
        if not ranked_list:
            return {"status": "NO_DATA"}

        action, score = ranked_list[0]

        if score > self.best_score:
            self.best_action = action
            self.best_score = score
            state = "UPDATED"
        else:
            state = "UNCHANGED"

        return {
            "state": state,
            "preferred_action": self.best_action,
            "score": round(self.best_score, 3)
        }


# DEMO
if __name__ == "__main__":

    memory = AdaptiveMemory()

    ranked = [
        ("INCREASE_SAFETY_MARGIN", 0.81),
        ("REDUCE_INTERVENTION_RATE", 0.80),
        ("INCREASE_STYLE_ANCHORING", 0.70),
    ]

    print("\n=== LAYER 75 — ADAPTIVE MEMORY ===\n")
    print(memory.update(ranked))
