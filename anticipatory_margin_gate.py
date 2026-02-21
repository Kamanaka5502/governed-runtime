import time
from collections import deque

class AnticipatoryMarginGate:

    def __init__(self):
        self.mode = "NORMAL"
        self.interaction_count = 0
        self.mutation_pressure = 0

        # ---- new memory layer ----
        self.history_window = deque(maxlen=5)
        self.preemptive_threshold = 5
        self.lock_threshold = 7

    def process(self, entropy):
        self.interaction_count += 1
        self.mutation_pressure += entropy

        # store recent pressure history
        self.history_window.append(self.mutation_pressure)

        avg_pressure = sum(self.history_window) / len(self.history_window)

        # --- anticipatory logic ---
        if avg_pressure >= self.preemptive_threshold and self.mode == "NORMAL":
            self.mode = "PREEMPTIVE_CAUTION"

        if self.mutation_pressure >= self.lock_threshold:
            self.mode = "LOCKED"
            print("⚠ Saturation reached — execution blocked")
            self.mutation_pressure = 0

        elif self.mode == "LOCKED":
            self.mode = "RECOVERY"

        elif self.mode == "RECOVERY":
            self.mode = "NORMAL"

        return {
            "mode": self.mode,
            "interaction_count": self.interaction_count,
            "mutation_pressure": self.mutation_pressure,
            "avg_pressure": round(avg_pressure, 2)
        }


if __name__ == "__main__":

    gate = AnticipatoryMarginGate()

    test_inputs = [2,2,3,2,3,2,1]

    for e in test_inputs:
        state = gate.process(e)
        print("STATE:", state)
