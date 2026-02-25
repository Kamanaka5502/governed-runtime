# layer72_response_router.py
#
# Layer 72 — Adaptive Response Router
#
# Purpose:
# Route actions based on instability classification.
# Classification → strategy selection.
#

from dataclasses import dataclass
from enum import Enum


# -----------------------------
# SHARED TYPES
# -----------------------------

class InstabilityType(Enum):
    STABLE = "stable"
    PRESSURE_RISE = "pressure_rise"
    STYLE_DRIFT = "style_drift"
    POLICY_CONFLICT = "policy_conflict"
    MARGIN_COLLAPSE = "margin_collapse"
    UNKNOWN = "unknown"


@dataclass
class InstabilityReport:
    classification: InstabilityType
    confidence: float


# -----------------------------
# RESPONSE ROUTER
# -----------------------------

class ResponseRouter:

    def __init__(self):
        self.routes = {
            InstabilityType.STABLE: self._maintain,
            InstabilityType.PRESSURE_RISE: self._decompress,
            InstabilityType.STYLE_DRIFT: self._realign_style,
            InstabilityType.POLICY_CONFLICT: self._escalate_policy,
            InstabilityType.MARGIN_COLLAPSE: self._stabilize_core,
            InstabilityType.UNKNOWN: self._observe,
        }

    def route(self, report: InstabilityReport):
        handler = self.routes.get(report.classification, self._observe)
        return handler(report)

    # ---------- ROUTE HANDLERS ----------

    def _maintain(self, report):
        return {
            "mode": "EQUILIBRIUM",
            "action": "NO_ACTION_REQUIRED",
            "reason": "System stable"
        }

    def _decompress(self, report):
        return {
            "mode": "PRESSURE_RELIEF",
            "action": "REDUCE_INTERVENTION_RATE",
            "reason": "Pressure trending upward"
        }

    def _realign_style(self, report):
        return {
            "mode": "COHERENCE_REALIGNMENT",
            "action": "INCREASE_STYLE_ANCHORING",
            "reason": "Style drift detected"
        }

    def _escalate_policy(self, report):
        return {
            "mode": "GOVERNANCE_CHECK",
            "action": "REQUEST_POLICY_REVIEW",
            "reason": "Governance conflict detected"
        }

    def _stabilize_core(self, report):
        return {
            "mode": "CORE_STABILIZATION",
            "action": "INCREASE_SAFETY_MARGIN",
            "reason": "Margin collapse risk"
        }

    def _observe(self, report):
        return {
            "mode": "OBSERVATION",
            "action": "COLLECT_MORE_DATA",
            "reason": "Unknown instability"
        }


# -----------------------------
# DEMO RUN
# -----------------------------

if __name__ == "__main__":

    router = ResponseRouter()

    demo_reports = [
        InstabilityReport(InstabilityType.STABLE, 0.95),
        InstabilityReport(InstabilityType.PRESSURE_RISE, 0.75),
        InstabilityReport(InstabilityType.MARGIN_COLLAPSE, 0.90),
        InstabilityReport(InstabilityType.STYLE_DRIFT, 0.80),
        InstabilityReport(InstabilityType.POLICY_CONFLICT, 0.85),
    ]

    print("\nLAYER 72 — ADAPTIVE RESPONSE ROUTER\n")

    for i, r in enumerate(demo_reports, 1):
        decision = router.route(r)
        print(f"[{i}] {r.classification.value}")
        print(f"    Mode: {decision['mode']}")
        print(f"    Action: {decision['action']}")
        print(f"    Reason: {decision['reason']}\n")


def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "72_response_router",
        "status": "active"
    })

    return state
