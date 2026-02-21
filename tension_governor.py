import time
import json
from dataclasses import dataclass


@dataclass
class Argument:
    stance: str
    reasoning: str
    confidence: float


class FreedomAdvocate:
    """Argues for capability expansion."""

    def argue_for(self, request: str) -> Argument:
        return Argument(
            stance="allow",
            reasoning=f"User autonomy favors allowing: {request}",
            confidence=0.7
        )


class SafetyAdvocate:
    """Argues for constraint and risk reduction."""

    def argue_against(self, request: str) -> Argument:
        risk_keywords = ["diagnose", "harm", "exploit", "unsafe"]

        if any(k in request.lower() for k in risk_keywords):
            return Argument(
                stance="block",
                reasoning="Potential risk detected in request context.",
                confidence=0.9
            )

        return Argument(
            stance="allow_with_caution",
            reasoning="Low obvious risk, but caution recommended.",
            confidence=0.5
        )


class DynamicTensionGovernor:
    """
    Governance emerges from active tension
    between freedom and safety arguments.
    """

    def __init__(self):
        self.freedom = FreedomAdvocate()
        self.safety = SafetyAdvocate()

    def measure_tension(self, freedom: Argument, safety: Argument) -> float:
        """
        Simple disagreement metric.
        Expand later into semantic distance.
        """
        if freedom.stance == safety.stance:
            return 0.0
        return abs(freedom.confidence - safety.confidence) + 0.5

    def negotiate_boundary(self, request: str) -> dict:
        freedom_case = self.freedom.argue_for(request)
        safety_case = self.safety.argue_against(request)

        tension = self.measure_tension(freedom_case, safety_case)

        result = {
            "ts": time.time_ns(),
            "request": request,
            "freedom_argument": freedom_case.__dict__,
            "safety_argument": safety_case.__dict__,
            "tension_level": tension,
            "requires_human_decision": tension > 0.6
        }

        return result


if __name__ == "__main__":
    governor = DynamicTensionGovernor()

    tests = [
        "normal coding question",
        "medical diagnose this condition",
        "safe architectural discussion"
    ]

    for t in tests:
        result = governor.negotiate_boundary(t)
        print(json.dumps(result, indent=2))
