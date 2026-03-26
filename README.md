# governed-runtime

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

### Admissibility Proof

This version extends the demo to explicitly prove whether the system is allowed to act at commit time.

Each governed decision produces:

- admissibility status (true/false)
- a structured proof of conditions:
  - authority validity
  - time-to-live validity
  - risk threshold validity
- a receipt containing proof, state hash, and chain linkage

Example:

[GOVERNED] cycle=7 → BLOCK (admissibility failed: authority_valid,ttl_valid) proof: authority_valid=False, ttl_valid=False, risk_valid=True

This demonstrates that execution is not based on prior validation, but on proof of admissibility at the moment of action.
