# Drift vs Governed Demo Output

## Summary

- Baseline actions: 14
- Governed actions: 6
- Governed blocked: 8

## Key divergence

At cycle 7:

- Baseline executed despite `ttl=0` and `auth=False`
- Governed blocked due to failed invariants: `authority, ttl_ok`

By cycle 10:

- Governed block reason expanded to: `authority, ttl_ok, risk_ok`

## Interpretation

The baseline runtime continues execution using stale state.

The governed runtime re-checks legality at commit time and blocks invalid progression.

This demonstrates fail-closed execution and drift-aware decision control.
