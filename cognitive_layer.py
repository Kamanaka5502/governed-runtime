import time
import json


class CognitiveSaturationLayer:
    """
    Operator cognitive load manager.

    Tracks entropy signals and forces stabilization checkpoints.
    """

    def __init__(self):
        self.interaction_count = 0
        self.mutation_pressure = 0
        self.last_input = None
        self.mode_lock = "NORMAL"
        self.checkpoints = []

    def _entropy_score(self, user_input: str) -> int:
        """
        Simple entropy heuristic:
        - changed structure rapidly
        - longer inputs
        - frequent shifts
        """

        score = 0

        if self.last_input and user_input != self.last_input:
            score += 1

        if len(user_input) > 80:
            score += 1

        if self.interaction_count > 5:
            score += 1

        return score

    def process(self, user_input: str):
        """
        Main cognitive load processor.
        """

        self.interaction_count += 1
        entropy = self._entropy_score(user_input)

        self.mutation_pressure += entropy
        self.last_input = user_input

        # Saturation detection
        if self.mutation_pressure >= 6:
            self.mode_lock = "FORMAT_LOCK"
            checkpoint = self._create_checkpoint(user_input)
            self.checkpoints.append(checkpoint)

            print("⚠ Cognitive saturation detected.")
            print("Checkpoint inserted.")
            print(json.dumps(checkpoint, indent=2))

            # reset pressure after checkpoint
            self.mutation_pressure = 0

        return {
            "mode": self.mode_lock,
            "interaction_count": self.interaction_count,
            "mutation_pressure": self.mutation_pressure
        }

    def _create_checkpoint(self, user_input):
        return {
            "ts": time.time_ns(),
            "interaction_count": self.interaction_count,
            "mode_lock": self.mode_lock,
            "snapshot": user_input
        }


if __name__ == "__main__":
    layer = CognitiveSaturationLayer()

    test_inputs = [
        "start runtime",
        "add routing discipline",
        "no that changed rewrite",
        "add envelope signing now",
        "wait this drifted fix format",
        "redo whole structure clean",
        "force deterministic output"
    ]

    for msg in test_inputs:
        state = layer.process(msg)
        print("STATE:", state)
