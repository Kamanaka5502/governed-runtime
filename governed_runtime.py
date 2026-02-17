import json
import time
import uuid
from datetime import datetime


EVENT_FILE = "events.jsonl"


# -----------------------------
# PROBE (Event Logger)
# -----------------------------

class Probe:
    def __init__(self, path):
        self.path = path
        self.eid = 0

    def log(self, actor, event_type, outcome=None, **extra):
        self.eid += 1
        event = {
            "eid": self.eid,
            "ts": time.time_ns(),
            "actor": actor,
            "type": event_type,
            "outcome": outcome
        }
        event.update(extra)

        with open(self.path, "a") as f:
            f.write(json.dumps(event) + "\n")


# -----------------------------
# ROUTING ENGINE
# -----------------------------

class RoutingEngine:

    def __init__(self):
        self.policies = [
            {
                "name": "blocked_keyword",
                "match": lambda text: "forbidden" in text.lower(),
                "decision": "block",
                "safety_level": "critical"
            },
            {
                "name": "default",
                "match": lambda text: True,
                "decision": "allow",
                "safety_level": "low"
            }
        ]

    def classify(self, text):
        for policy in self.policies:
            if policy["match"](text):
                return policy


# -----------------------------
# OUTPUT VALIDATOR (Stub)
# -----------------------------

class OutputValidator:

    def validate(self, response, safety_level):
        # Stub for future safety logic
        return {"passes": True}


# -----------------------------
# GOVERNED RUNTIME
# -----------------------------

class GovernedRuntime:

    def __init__(self):
        self.probe = Probe(EVENT_FILE)
        self.router = RoutingEngine()
        self.validator = OutputValidator()

    def process(self, user_input, session_id="default_session"):

        # 1. Log request
        self.probe.log(
            actor=session_id,
            event_type="request_received",
            outcome="pending"
        )

        # 2. Routing decision
        policy = self.router.classify(user_input)

        self.probe.log(
            actor=session_id,
            event_type="routing_decision",
            outcome=policy["decision"],
            policy=policy["name"],
            safety_level=policy["safety_level"]
        )

        # 3. Escalation slot (structural only)
        if policy["safety_level"] == "critical":
            self.probe.log(
                actor=session_id,
                event_type="escalation_required",
                outcome="true"
            )

        # 4. Block if necessary
        if policy["decision"] == "block":
            self.probe.log(
                actor=session_id,
                event_type="request_blocked",
                outcome="policy_violation"
            )
            return "Request blocked by routing policy."

        # 5. Simulated LLM call
        response = f"Echo: {user_input}"

        self.probe.log(
            actor=session_id,
            event_type="response_generated",
            outcome="success"
        )

        # 6. Output validation
        validation = self.validator.validate(response, policy["safety_level"])

        self.probe.log(
            actor=session_id,
            event_type="output_validated",
            outcome="passed" if validation["passes"] else "failed"
        )

        # 7. Send response
        self.probe.log(
            actor=session_id,
            event_type="response_sent",
            outcome="success"
        )

        return response


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    runtime = GovernedRuntime()

    print(runtime.process("Test request"))
    print(runtime.process("This contains forbidden content"))
