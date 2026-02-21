class RestGate:

    def evaluate(self, continuity, intervention_level):
        rest_allowed = continuity > 0.85 and intervention_level < 0.6

        return {
            "continuity": continuity,
            "intervention_level": intervention_level,
            "rest_allowed": rest_allowed
        }

if __name__ == "__main__":
    g = RestGate()
    print("=== LAYER 69 — REST GATE ===")
    print(g.evaluate(0.91, 0.52))
