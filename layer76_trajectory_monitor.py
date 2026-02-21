import statistics

class TrajectoryMonitor:
    """
    LAYER 76 — TRAJECTORY MONITOR
    Detects early directional drift before instability forms.
    """

    def __init__(self, window=6):
        self.window = window
        self.history = []

    def record(self, pressure, margin, intervention_level):
        entry = {
            "pressure": pressure,
            "margin": margin,
            "intervention": intervention_level
        }
        self.history.append(entry)

        if len(self.history) > self.window:
            self.history.pop(0)

    def _slope(self, values):
        if len(values) < 2:
            return 0.0
        deltas = [
            values[i] - values[i - 1]
            for i in range(1, len(values))
        ]
        return round(statistics.mean(deltas), 3)

    def evaluate(self):
        if len(self.history) < 3:
            return {"status": "INSUFFICIENT_DATA"}

        pressures = [e["pressure"] for e in self.history]
        margins = [e["margin"] for e in self.history]
        interventions = [e["intervention"] for e in self.history]

        p_slope = self._slope(pressures)
        m_slope = self._slope(margins)
        i_slope = self._slope(interventions)

        signals = []

        # Early warning logic
        if p_slope > 0.03:
            signals.append("PRESSURE_RISING")
        if m_slope < -0.02:
            signals.append("MARGIN_SHRINKING")
        if i_slope > 0.02:
            signals.append("INTERVENTION_ESCALATING")

        if len(signals) >= 2:
            status = "PRE_DRIFT_WARNING"
        elif len(signals) == 1:
            status = "WATCH"
        else:
            status = "STABLE"

        return {
            "status": status,
            "pressure_slope": p_slope,
            "margin_slope": m_slope,
            "intervention_slope": i_slope,
            "signals": signals
        }


# ==============================
# DEMO RUN
# ==============================
if __name__ == "__main__":
    t = TrajectoryMonitor()

    demo = [
        (0.52, 0.78, 0.40),
        (0.56, 0.75, 0.45),
        (0.60, 0.72, 0.50),
        (0.63, 0.69, 0.55),
        (0.66, 0.65, 0.58),
    ]

    for p, m, i in demo:
        t.record(p, m, i)

    print("=== LAYER 76 — TRAJECTORY MONITOR ===")
    print(t.evaluate())
