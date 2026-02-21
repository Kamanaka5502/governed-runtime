# ============================================
# Layer 21 — Runtime Boundary Guard
# ============================================

class RuntimeBoundaryGuard:
    def __init__(self):
        self.state = "stable"

    def observe(self, signal):
        pressure = signal.get("pressure", 0)

        if pressure < 0.4:
            self.state = "stable"
            action = "normal_flow"
        elif pressure < 0.7:
            self.state = "watch"
            action = "soft_guard"
        else:
            self.state = "boundary_lock"
            action = "hard_guard"

        return {
            "state": self.state,
            "action": action,
            "pressure": pressure
        }


if __name__ == "__main__":
    guard = RuntimeBoundaryGuard()

    demo = [
        {"pressure": 0.2},
        {"pressure": 0.5},
        {"pressure": 0.9},
    ]

    print("=== Layer 21 — Runtime Boundary Guard ===")
    for s in demo:
        result = guard.observe(s)
        print(result)
