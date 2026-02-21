import statistics

class RecoveryWindow:

    def __init__(self):
        self.history = []

    def record(self, outcome):
        self.history.append(outcome)
        if len(self.history) > 8:
            self.history.pop(0)

    def status(self):
        if len(self.history) < 4:
            return {"state": "INSUFFICIENT_DATA"}

        avg = statistics.mean(self.history)
        var = statistics.pvariance(self.history)

        recoverable = avg > 0.75 and var < 0.01

        return {
            "avg_outcome": round(avg,3),
            "variance": round(var,3),
            "recovery_window": recoverable
        }

if __name__ == "__main__":
    r = RecoveryWindow()
    print("=== LAYER 67 — RECOVERY WINDOW ===")

    demo = [0.78,0.80,0.79,0.81,0.80,0.79]
    for d in demo:
        r.record(d)

    print(r.status())
