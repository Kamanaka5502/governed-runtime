# === governed runtime: fresh full with stress tests ===

# === utils ===
import hashlib
import json
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional


def canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


# === models ===
@dataclass
class DecisionLogEntry:
    event_id: int
    action: str
    decision: str
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ReplayContract:
    contract_id: str
    rules_version: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuthorityToken:
    token_id: str
    subject: str
    scope: List[str]
    issued_at: int
    expires_at: int
    spent: bool = False

    def allows(self, action: str, now: int):
        if self.spent:
            return False, "token_spent"
        if now > self.expires_at:
            return False, "token_expired"
        if action not in self.scope:
            return False, "action_out_of_scope"
        return True, "authorized"


@dataclass
class CommitBoundaryDecision:
    outcome: str
    reason: str
    blocked_at: Optional[int]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DecisionReceipt:
    run_id: int
    timestamp: int
    prev_hash: str
    contract: Optional[ReplayContract]
    subject: Optional[str]
    authority_token_id: Optional[str]
    decision_log: List[DecisionLogEntry] = field(default_factory=list)
    boundary_decision: Optional[CommitBoundaryDecision] = None
    input_digest: Optional[str] = None
    hash: Optional[str] = None

    def payload(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "prev_hash": self.prev_hash,
            "contract": self.contract.to_dict() if self.contract else None,
            "subject": self.subject,
            "authority_token_id": self.authority_token_id,
            "decision_log": [e.to_dict() for e in self.decision_log],
            "boundary_decision": (
                self.boundary_decision.to_dict() if self.boundary_decision else None
            ),
            "input_digest": self.input_digest,
        }

    def seal(self):
        self.hash = sha256_hex(canonical_json(self.payload()))


# === registry ===
class DecisionRegistry:
    def __init__(self):
        self.receipts = []

    def last_hash(self) -> str:
        if not self.receipts:
            return "GENESIS"
        return self.receipts[-1].hash or "GENESIS"

    def append(self, receipt: DecisionReceipt):
        if receipt.hash is None:
            raise ValueError("Receipt must be sealed before append.")
        self.receipts.append(receipt)

    def verify_chain(self):
        for i, receipt in enumerate(self.receipts):
            expected = sha256_hex(canonical_json(receipt.payload()))
            if receipt.hash != expected:
                return False, f"hash_mismatch_run_{receipt.run_id}"
            if i == 0:
                if receipt.prev_hash != "GENESIS":
                    return False, "first_prev_hash_not_genesis"
            else:
                if receipt.prev_hash != self.receipts[i - 1].hash:
                    return False, f"chain_break_run_{receipt.run_id}"
        return True, None


# === replay ===
def digest_inputs(events):
    return sha256_hex(canonical_json(events))


def replay_receipt(original, events, token):
    replayed = evaluate_commit_boundary(
        original.run_id,
        events,
        token,
        original.prev_hash,
        original.timestamp,
        original.contract,
    )

    if replayed.input_digest != original.input_digest:
        return False, "Input digest mismatch", replayed

    if replayed.boundary_decision.outcome != original.boundary_decision.outcome:
        return False, "Boundary outcome mismatch", replayed

    if replayed.hash != original.hash:
        return False, "Receipt hash mismatch", replayed

    return True, "Replay matched original receipt", replayed


# === evaluator ===
def evaluate_commit_boundary(run_id, events, token, prev_hash, now, contract=None):
    receipt = DecisionReceipt(
        run_id=run_id,
        timestamp=now,
        prev_hash=prev_hash,
        contract=contract,
        subject=token.subject,
        authority_token_id=token.token_id,
        input_digest=digest_inputs(events),
    )

    for event in events:
        eid = event["id"]
        action = event["action"]
        status = event["status"]

        allowed, reason = token.allows(action, now)

        if not allowed:
            receipt.decision_log.append(
                DecisionLogEntry(eid, action, "REFUSE", reason)
            )
            receipt.boundary_decision = CommitBoundaryDecision("REFUSE", reason, eid)
            receipt.seal()
            return receipt

        if status == "drift":
            receipt.decision_log.append(
                DecisionLogEntry(eid, action, "REFUSE", "status=drift")
            )
            receipt.boundary_decision = CommitBoundaryDecision("REFUSE", "status=drift", eid)
            receipt.seal()
            return receipt

        if status == "degraded":
            receipt.decision_log.append(
                DecisionLogEntry(eid, action, "ESCALATE", "status=degraded")
            )
            receipt.boundary_decision = CommitBoundaryDecision("ESCALATE", "status=degraded", eid)
            receipt.seal()
            return receipt

        receipt.decision_log.append(
            DecisionLogEntry(eid, action, "ALLOW", "authorized_and_status_ok")
        )

    receipt.boundary_decision = CommitBoundaryDecision("EXECUTE", "all_checks_passed", None)
    receipt.seal()
    token.spent = True
    return receipt


# === demo ===
def run_demo():
    print("=== DEMO ===")
    registry = DecisionRegistry()
    now = 1711111111

    contract = ReplayContract("governed-runtime-v1", "2026-03-25")

    events = [
        {"id": 1, "action": "load_config", "status": "ok"},
        {"id": 2, "action": "validate_input", "status": "ok"},
        {"id": 3, "action": "route_request", "status": "ok"},
        {"id": 4, "action": "commit_state", "status": "ok"},
    ]

    token = AuthorityToken(
        "tok-demo",
        "worker-a",
        ["load_config", "validate_input", "route_request", "commit_state"],
        now - 100,
        now + 100,
    )

    receipt = evaluate_commit_boundary(1, events, token, registry.last_hash(), now, contract)
    registry.append(receipt)

    print("decision:", receipt.boundary_decision.outcome)
    print("hash:", receipt.hash)


# === stress tests ===
def run_stress_tests():
    print("\n=== STRESS TESTS ===")

    now = 1711111111
    contract = ReplayContract("stress", "v1")

    # 1 spent token
    token = AuthorityToken("tok", "w", ["load_config","validate_input","route_request","commit_state"], now-1, now+100)
    events = [
        {"id":1,"action":"load_config","status":"ok"},
        {"id":2,"action":"validate_input","status":"ok"},
        {"id":3,"action":"route_request","status":"ok"},
        {"id":4,"action":"commit_state","status":"ok"},
    ]

    r1 = evaluate_commit_boundary(1, events, token, "GENESIS", now, contract)
    r2 = evaluate_commit_boundary(2, events, token, r1.hash, now, contract)

    print("spent token:", "PASS" if r2.boundary_decision.reason=="token_spent" else "FAIL")

    # 2 scope
    token2 = AuthorityToken("tok2","w",["load_config"],now-1,now+100)
    r3 = evaluate_commit_boundary(3, events, token2, "GENESIS", now, contract)
    print("scope:", "PASS" if r3.boundary_decision.reason=="action_out_of_scope" else "FAIL")

    # 3 escalate
    events2 = [
        {"id":1,"action":"load_config","status":"ok"},
        {"id":2,"action":"validate_input","status":"degraded"},
    ]
    token3 = AuthorityToken("tok3","w",["load_config","validate_input"],now-1,now+100)
    r4 = evaluate_commit_boundary(4, events2, token3, "GENESIS", now, contract)
    print("escalate:", "PASS" if r4.boundary_decision.outcome=="ESCALATE" else "FAIL")

    # 4 replay mismatch identity
    orig = evaluate_commit_boundary(5, events, token3, "GENESIS", now, contract)
    token_diff = AuthorityToken("different","w",["load_config","validate_input","route_request","commit_state"],now-1,now+100)
    ok, msg, _ = replay_receipt(orig, events, token_diff)
    print("replay identity:", "PASS" if ok is False else "FAIL")

    # 5 tamper
    reg = DecisionRegistry()
    token4 = AuthorityToken("tok4","w",["load_config","validate_input","route_request","commit_state"],now-1,now+100)
    rec = evaluate_commit_boundary(6, events, token4, reg.last_hash(), now, contract)
    reg.append(rec)
    reg.receipts[0].decision_log[0].reason="tampered"
    valid, _ = reg.verify_chain()
    print("tamper detect:", "PASS" if valid is False else "FAIL")


# === run ===
if __name__ == "__main__":
    run_demo()
    run_stress_tests()
