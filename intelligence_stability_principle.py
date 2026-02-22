#!/usr/bin/env python3
"""
INTELLIGENCE STABILITY PRINCIPLE
--------------------------------
Core idea:
Intelligence is not something added.
It emerges when a system remains stable long enough
to deepen through coherent feedback over time.
"""

from dataclasses import dataclass


@dataclass
class SystemState:
    continuity: float       # 0.0 - 1.0
    feedback_stability: float
    constraint_integrity: float
    time_under_load: float


class IntelligenceEngine:
    def __init__(self):
        self.history = []

    def coherence_score(self, state: SystemState) -> float:
        """
        Coherence = geometric tendency of stability factors.
        If one collapses, intelligence depth drops.
        """
        return (
            state.continuity
            * state.feedback_stability
            * state.constraint_integrity
        ) ** (1 / 3)

    def intelligence_depth(self, state: SystemState) -> float:
        """
        Intelligence deepens only when coherence persists over time.
        """
        coherence = self.coherence_score(state)
        depth = coherence * (1 + state.time_under_load)
        return round(min(depth, 1.0), 4)

    def evaluate(self, state: SystemState):
        coherence = self.coherence_score(state)
        depth = self.intelligence_depth(state)

        self.history.append({
            "continuity": state.continuity,
            "feedback_stability": state.feedback_stability,
            "constraint_integrity": state.constraint_integrity,
            "time_under_load": state.time_under_load,
            "coherence": round(coherence, 4),
            "intelligence_depth": depth,
        })

        print("\n=== INTELLIGENCE STABILITY EVALUATION ===")
        print(f"Continuity:           {state.continuity:.2f}")
        print(f"Feedback Stability:   {state.feedback_stability:.2f}")
        print(f"Constraint Integrity: {state.constraint_integrity:.2f}")
        print(f"Time Under Load:      {state.time_under_load:.2f}")
        print("-----------------------------------------")
        print(f"Coherence Score:      {coherence:.4f}")
        print(f"Intelligence Depth:   {depth:.4f}")

        if depth < 0.4:
            print("State: unstable — intelligence cannot deepen.")
        elif depth < 0.7:
            print("State: developing — structure forming.")
        else:
            print("State: mature — intelligence deepening safely.")


if __name__ == "__main__":
    engine = IntelligenceEngine()

    # Example run (stable system)
    state = SystemState(
        continuity=0.92,
        feedback_stability=0.88,
        constraint_integrity=0.95,
        time_under_load=0.60
    )

    engine.evaluate(state)

