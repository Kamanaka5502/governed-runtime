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
