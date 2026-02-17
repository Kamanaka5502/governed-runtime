import uuid
import json
import time
from datetime import datetime

EVENT_LOG = "events.jsonl"


# ----------------------------
# PROBE
# ----------------------------

class Probe:
    def __init__(self, path):
        self.path = path
        self.eid = 0

    def event(self, actor, event_type, outcome, **kwargs):
        self.eid += 1
        record = {
            "eid": self.eid,
            "ts": time.time_ns(),
            "actor": actor,
            "type": event_type,
            "outcome": outcome,
        }
        record.update(kwargs)
        with open(self.path, "a") as f:
            f.write(json.dumps(record) + "\n")


# ----------------------------
# GOVERNED MEMORY (Minimal)
# ----------------------------

class GovernedMemory:
    def __init__(self):
        self.state = {}

    def commit(self, key, value, actor, probe):
        if key in self.state and self.state[key] != value:
            probe.event(
                actor=actor,
                event_type="conflict_detected",
                outcome="halted",
                key=key,
                existing=self.state[key],
                new=value
            )
            return False

        self.state[key] = value

        probe.event(
            actor=actor,
            event_type="memory_commit",
            outcome="success",
            key=key,
            value=value,
            timestamp=str(datetime.utcnow())
        )

        return True


# ----------------------------
# ROUTING ENGINE (HARDENED)
# ----------------------------

class RoutingEngine:
    def __init__(self):
        self.routes = {
            "default": {
                "allowed": True,
                "safety_level": "low",
                "validators": []
            },
            "blocked_keyword": {
                "allowed": False,
                "safety_level": "critical",
                "validators": []
            }
        }

    def classify(self, user_input):
        if "forbidden" in user_input.lower():
            route_name = "blocked_keyword"
        else:
            route_name = "default"

        if route_name not in self.routes:
            raise Exception("Undefined routing policy")

        return route_name, self.routes[route_name]


# ----------------------------
# ORCHESTRATOR
# ----------------------------

class GovernedRuntime:
    def __init__(self):
        self.probe = Probe(EVENT_LOG)
        self.memory = GovernedMemory()
        self.router = RoutingEngine()

    def process(self, user_input, session_id="default_session"):

        # Log request
        self.probe.event(
            actor=session_id,
            event_type="request_received",
            outcome="pending"
        )

        # Routing classification
        route_name, route = self.router.classify(user_input)

        self.probe.event(
            actor=session_id,
            event_type="routing_decision",
            outcome="allowed" if route["allowed"] else "blocked",
            policy=route_name,
            safety_level=route["safety_level"]
        )

        # Enforce routing
        if not route["allowed"]:
            self.probe.event(
                actor=session_id,
                event_type="request_blocked",
                outcome="policy_violation"
            )
            return "Request blocked by routing policy."

        # Simulated LLM call
        response = f"Echo: {user_input}"

        # Log response
        self.probe.event(
            actor=session_id,
            event_type="response_sent",
            outcome="success"
        )

        return response


# ----------------------------
# MAIN
# ----------------------------

if __name__ == "__main__":
    runtime = GovernedRuntime()

    print(runtime.process("Test request"))
    print(runtime.process("This contains forbidden content"))
