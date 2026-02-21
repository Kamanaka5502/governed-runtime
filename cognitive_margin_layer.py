import time
import json


class CognitiveMarginLayer:
    def __init__(self):
        self.mode = "NORMAL"
        self.interaction_count = 0
        self.mutation_pressure = 0

        self.elevated_threshold = 4
        self.lock_threshold = 8

        self.recovery_cycles = 2
        self.recovery_remaining = 0

        self.checkpoints = []

    def _lock(self, user_input):
        self.mode = "LOCKED"
        checkpoint = {
            "ts": time.time_ns(),
            "interaction_count": self.interaction_count,
            "mode_lock": self.mode,
            "snapshot": user_input,
        }
        self.checkpoints.append(checkpoint)

        print("⚠ Cognitive saturation detected.")
        print("Checkpoint inserted.")
        print(json.dumps(checkpoint, indent=2))

    def process(self, user_input):
        self.interaction_count += 1

        entropy = len(user_input.split()) // 2 + 1
        self.mutation_pressure += entropy

        # GLOBAL saturation check (always active)
        if (
            self.mutation_pressure >= self.lock_threshold
            and self.mode != "LOCKED"
        ):
            self._lock(user_input)

        # state transitions
        if self.mode == "NORMAL":
            if self.mutation_pressure >= self.elevated_threshold:
                self.mode = "ELEVATED"

        elif self.mode == "LOCKED":
            self.mode = "RECOVERY"
            self.recovery_remaining = self.recovery_cycles
            self.mutation_pressure = 0

        elif self.mode == "RECOVERY":
            self.recovery_remaining -= 1
            if self.recovery_remaining <= 0:
                self.mode = "NORMAL"
                self.mutation_pressure = 0

        return {
            "mode": self.mode,
            "interaction_count": self.interaction_count,
            "mutation_pressure": self.mutation_pressure,
        }


if __name__ == "__main__":
    layer = CognitiveMarginLayer()

    test_inputs = [
        "start runtime",
        "add routing discipline",
        "no that changed rewrite",
        "add envelope signing now",
        "wait this drifted fix format",
        "redo whole structure clean",
        "force deterministic output",
    ]

    for msg in test_inputs:
        state = layer.process(msg)
        print("STATE:", state)
