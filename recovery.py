import json
from atomic_state import CanonicalState


class RecoveryEngine:
    """
    Deterministic reconstruction of canonical state from WAL.
    Schema-tolerant recovery.
    """

    def __init__(self, wal_path="wal.log"):
        self.wal_path = wal_path

    def recover(self) -> CanonicalState:
        state = CanonicalState(self.wal_path)

        entries = state.wal.read_all()

        committed = set()
        transitions = {}

        # First pass: classify entries
        for entry in entries:
            status = entry.get("status")

            if status == "pending":
                transitions[entry["seq"]] = entry

            elif status == "committed":
                committed.add(entry["seq"])

            elif status == "failed":
                transitions.pop(entry["seq"], None)

        # Second pass: apply only committed transitions
        for seq in sorted(committed):
            if seq not in transitions:
                continue

            transition_block = transitions[seq].get("transition", {})

            # Schema-tolerant extraction
            if isinstance(transition_block, dict):
                event = transition_block.get("event", transition_block)
            else:
                continue

            state.data = state.apply_transition(event)
            state.version += 1

        return state
