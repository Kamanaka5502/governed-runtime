# governed-runtime

AI systems must prove they are allowed to act — every time.

Most systems assume permission persists. This project challenges that assumption.

Deterministic execution governance with commit-time invariant enforcement and verifiable receipts.

---

## Demonstration

This repo includes a drift vs governed execution demo showing how systems fail under stale conditions.

### Result

- Baseline actions: 14
- Governed actions: 6
- Governed blocked: 8

### Key moment

At cycle 7:
- authority expired (`ttl=0`, `auth=False`)
- baseline continued execution
- governed runtime blocked at commit

### Run the demo

```bash
python3 demo/drift_vs_governed.py
```

### Output

See: `docs/demo_output.md`

---

## Admissibility Proof

This version extends the demo to explicitly prove whether the system is allowed to act at commit time.

Each governed decision produces:

- admissibility status (true/false)
- structured proof of conditions:
  - authority_valid
  - ttl_valid
  - risk_valid
- a receipt containing proof, state hash, and chain linkage

### Core Principle

Execution is not allowed by default.

Each action must re-establish its legitimacy under current conditions at commit time.

### Example

```
[GOVERNED] cycle=7 → BLOCK (admissibility failed: authority_valid,ttl_valid)
proof: authority_valid=False, ttl_valid=False, risk_valid=True
```

This demonstrates that execution is not based on prior validation, but on proof of admissibility at the moment of action.
