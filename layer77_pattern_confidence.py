import statistics


class PatternConfidenceEngine:
    """
    Layer 77 — Pattern Confidence Engine

    Determines whether stability is structural
    or temporarily maintained through interventions.
    """

    def __init__(self, window=8):
        self.window = window
        self.history = []

    def record(self, stability_score, intervention_level):
        """Record a new observation."""
        self.history.append({
            "stability": stability_score,
            "intervention": intervention_level
        })

        if len(self.history) > self.window:
            self.history.pop(0)

    def evaluate(self):
        """Evaluate pattern confidence."""

        if len(self.history) < 4:
            return {"status": "INSUFFICIENT_DATA"}

        stability_vals = [h["stability"] for h in self.history]
        intervention_vals = [h["intervention"] for h in self.history]

        avg_stability = statistics.mean(stability_vals)
        stability_var = statistics.pvariance(stability_vals)
        avg_intervention = statistics.mean(intervention_vals)

        # Low variance = stable pattern
        pattern_confidence = max(0.0, 1.0 - stability_var)

        if avg_stability > 0.8 and avg_intervention < 0.5:
            mode = "STRUCTURAL_STABILITY"
        elif avg_stability > 0.8:
            mode = "TEMPORARY_STABILITY"
        else:
            mode = "UNSTABLE_PATTERN"

        return {
            "pattern_confidence": round(pattern_confidence, 3),
            "avg_stability": round(avg_stability, 3),
            "avg_intervention": round(avg_intervention, 3),
            "mode": mode
        }


if __name__ == "__main__":
    engine = PatternConfidenceEngine()

    demo_data = [
        (0.82, 0.60),
        (0.84, 0.55),
        (0.86, 0.50),
        (0.87, 0.45),
        (0.88, 0.40),
        (0.89, 0.35),
    ]

    for s, i in demo_data:
        engine.record(s, i)

    print("=== LAYER 77 — PATTERN CONFIDENCE ===")
    print(engine.evaluate())
