import time
import json
from pathlib import Path


# ---------------------------
# ROUTING ENGINE (Layer 3)
# ---------------------------

class RoutingEngine:

    def classify(self, user_input: str) -> dict:
        """
        Minimal routing logic.
        Extend later with real rules.
        """
        return {
            "blocked": False,
            "requires_escalation": False,
            "constraints": {}
        }


# ---------------------------
# SIMPLE PROBE (observability)
# ---------------------------

class Probe:

    def __init__(self, path: str):
        self.path = Path(path)
        self.eid = 0

    def event(self, actor: str, event_type: str, outcome: str):
        self.eid += 1
        record = {
            "eid": self.eid,
            "ts": time.time_ns(),
            "actor": actor,
            "type": event_type,
            "outcome": outcome
        }

        with self.path.open("a") as f:
            f.write(json.dumps(record) + "\n")


# ---------------------------
# GOVERNED RUNTIME (Spine)
# ---------------------------

class GovernedRuntime:

    def __init__(self, event_log="events.jsonl"):
        self.router = RoutingEngine()
        self.probe = Probe(event_log)

    def process(self, user_input: str, session_id: str = "default_session"):

        self.probe.event(session_id, "request_received", "pending")

        route = self.router.classify(user_input)

        if route["blocked"]:
            self.probe.event(session_id, "routing_decision", "blocked")
            return "Blocked by routing policy"

        self.probe.event(session_id, "routing_decision", "allowed")

        # Mock LLM call (stateless placeholder)
        response = f"Echo: {user_input}"

        self.probe.event(session_id, "response_sent", "success")

        return response


# ---------------------------
# CLI ENTRY
# ---------------------------

if __name__ == "__main__":
    runtime = GovernedRuntime()
    result = runtime.process("Test request")
    print(result)
