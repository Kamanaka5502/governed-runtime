# layer71_instability_classifier.py
#
# Layer 71 — Instability Classification Engine
#
# Purpose:
# Move from "something is wrong" → "what kind of wrong is it?"
# This is the bridge between observability and adaptive intelligence.

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List
import time
import math


# -----------------------------
# INSTABILITY TYPES
# -----------------------------

class InstabilityType(Enum):
    STABLE = "stable"
    PRESSURE_RISE = "pressure_rise"
    STYLE_DRIFT = "style_drift"
    POLICY_CONFLICT = "policy_conflict"
    MARGIN_COLLAPSE = "margin_collapse"
    UNKNOWN = "unknown"


@dataclass
class InstabilitySignal:
    pressure: float
    margin: float
    style_variance: float
    policy_disagreement: float
    timestamp: int = field(default_factory=lambda: time.time_ns())


@dataclass
class InstabilityReport:
    classification: InstabilityType
    confidence: float
    reasons: List[str]
    signal_snapshot: Dict


# -----------------------------
# CLASSIFIER CORE
# -----------------------------

class InstabilityClassifier:

    def __init__(self):
        self.history: List[InstabilitySignal] = []

    def classify(self, signal: InstabilitySignal) -> InstabilityReport:
        self.history.append(signal)

        reasons = []
        confidence = 0.0
        classification = InstabilityType.UNKNOWN

        # ---- RULES (deterministic for now) ----

        if signal.margin < 0.25:
            classification = InstabilityType.MARGIN_COLLAPSE
            confidence = 0.90
            reasons.append("Operational margin below safe threshold")

        elif signal.policy_disagreement > 0.70:
            classification = InstabilityType.POLICY_CONFLICT
            confidence = 0.85
            reasons.append("High governance disagreement detected")

        elif signal.style_variance > 0.65:
            classification = InstabilityType.STYLE_DRIFT
            confidence = 0.80
            reasons.append("Style variance exceeding continuity limit")

        elif signal.pressure > 0.70:
            classification = InstabilityType.PRESSURE_RISE
            confidence = 0.75
            reasons.append("Interaction pressure trending upward")

        elif (
            signal.pressure < 0.40
            and signal.margin > 0.60
            and signal.style_variance < 0.30
        ):
            classification = InstabilityType.STABLE
            confidence = 0.95
            reasons.append("All stability indicators within range")

        else:
            reasons.append("No dominant instability pattern")

        return InstabilityReport(
            classification=classification,
            confidence=confidence,
            reasons=reasons,
            signal_snapshot=signal.__dict__,
        )


# -----------------------------
# DEMO RUN
# -----------------------------

if __name__ == "__main__":

    classifier = InstabilityClassifier()

    scenarios = [
        InstabilitySignal(
            pressure=0.25,
            margin=0.80,
            style_variance=0.10,
            policy_disagreement=0.05,
        ),
        InstabilitySignal(
            pressure=0.82,
            margin=0.55,
            style_variance=0.22,
            policy_disagreement=0.10,
        ),
        InstabilitySignal(
            pressure=0.55,
            margin=0.20,
            style_variance=0.40,
            policy_disagreement=0.25,
        ),
        InstabilitySignal(
            pressure=0.50,
            margin=0.50,
            style_variance=0.75,
            policy_disagreement=0.10,
        ),
        InstabilitySignal(
            pressure=0.60,
            margin=0.45,
            style_variance=0.25,
            policy_disagreement=0.85,
        ),
    ]

    print("\nLAYER 71 — INSTABILITY CLASSIFICATION\n")

    for i, s in enumerate(scenarios, 1):
        r = classifier.classify(s)
        print(f"[{i}] Classification: {r.classification.value}")
        print(f"    Confidence: {r.confidence:.2f}")
        print(f"    Reasons: {', '.join(r.reasons)}\n")

