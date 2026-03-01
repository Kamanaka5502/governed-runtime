# Governed Runtime (Deterministic Event Ledger + Drift Guardrails)

A minimal governed runtime that logs **hash-linked events**, verifies chain integrity, detects **behavior drift**, and supports **safe recovery** (rechain) when the ledger is corrupted.

> Goal: make runtime behavior **observable, verifiable, and governable** — not “trust me bro” AI.

---

## What this repo demonstrates

- **Append-only event ledger** (`events.jsonl`) with **hash chaining** (`prev` + computed hash)
- **Verification**: detect hash mismatch / chain breaks deterministically
- **Recovery**: rebuild a canonical chain from existing records (`rechain_events.py`)
- **Drift detection**: establish a baseline + compute drift scores from event distributions/transitions
- **Governor loop**: run cycles (A+B), enforce boundaries, and produce a stable head

---

## Quickstart (3 commands)

```bash
python verify_events.py
python governor.py --cycles 5 --do-model
python verify_events.py
