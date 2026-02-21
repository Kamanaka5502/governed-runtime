from cognitive_margin_layer import CognitiveMarginLayer

class ExecutionGate:
    def __init__(self):
        self.margin = CognitiveMarginLayer()

    def request_execution(self, input_event):
        state = self.margin.process(input_event)

        mode = state["mode"]

        if mode in ["LOCKED", "RECOVERY"]:
            print("⛔ EXECUTION BLOCKED — margin unsafe")
            print("state:", state)
            return False

        print("✅ EXECUTION ALLOWED")
        print("state:", state)
        return True


if __name__ == "__main__":
    gate = ExecutionGate()

    test_inputs = [
        "start runtime",
        "add routing discipline",
        "no that changed rewrite",
        "add envelope signing now",
        "redo whole structure clean",
        "force deterministic output",
    ]

    for msg in test_inputs:
        print("\nINPUT:", msg)
        gate.request_execution(msg)
