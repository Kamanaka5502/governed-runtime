# ============================================================
# Layer 22 — Adaptive Boundary Memory
# ============================================================

class AdaptiveBoundaryMemory:
    def __init__(self):
        self.state = "stable"
        self.history = []

    def observe(self, signal):
        pressure = signal.get("pressure", 0)

        # store history
        self.history.append(pressure)
        if len(self.history) > 5:
            self.history.pop(0)

        # simple rolling average memory
        avg_pressure = sum(self.history) / len(self.history)

        # adaptive thresholds based on recent memory
        if avg_pressure < 0.4:
            self.state = "stable"
            action = "normal_flow"
        elif avg_pressure < 0.7:
            self.state = "watch"
            action = "soft_guard"
        else:
            self.state = "boundary_lock"
            action = "hard_guard"

        return {
            "state": self.state,
            "action": action,
            "pressure": pressure,
            "avg_pressure": round(avg_pressure, 3),
            "history": list(self.history),
        }


if __name__ == "__main__":
    guard = AdaptiveBoundaryMemory()

    demo = [
        {"pressure": 0.2},
        {"pressure": 0.5},
        {"pressure": 0.9},
        {"pressure": 0.6},
        {"pressure": 0.3},
    ]

    print("=== Layer 22 — Adaptive Boundary Memory ===")
    for s in demo:
        result = guard.observe(s)
        print(result)
