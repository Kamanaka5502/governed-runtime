# governed-runtime
**Hash-chained event ledger + drift baseline + governor loop (A+B) with rechain recovery**

<<<<<<< HEAD
Execution-time governance framework for controlled, deterministic system behavior.

---

## Overview

VERIFY OK

DRIFT SCORE: 0.000000  

STABLE BEHAVIOR

Governed Runtime is a deterministic execution framework designed to:

- enforce runtime constraints
- prevent uncontrolled state drift
- verify execution integrity via signed receipts
- support recoverable, observable execution flows

This repository focuses on execution governance, not model behavior itself.

---

## Core Concepts

### Execution-Time Governance
Actions are validated at runtime against defined rules before commit.

### Deterministic Execution
Identical input conditions produce repeatable state transitions.

### Receipt Ledger
All execution stages are append-only and verifiable.

### Adaptive Intent Gate
Execution passes through staged validation before irreversible actions.

---

## Architecture

High-level flow:

intent → validation → governed executor → receipt ledger → state commit

### Components

- `governed_executor.py`
- `receipt_ledger.py`
- `events.head`
- validation / recovery tools

---

## What This Project IS

- Runtime governance layer
- Deterministic execution control
- Auditability and replay verification
- Execution safety boundary

---

## What This Project IS NOT

- AI model training system
- Autonomous agent framework
- Blockchain replacement
- General orchestration layer

---

## Verification

Example:

```bash
python3 governed_executor.py
python3 receipt_ledger.py verify
```

Expected output:

```text
{'ok': True, 'count': N}
```

---

## Design Principles

- Fail closed
- Explicit state transitions
- Signed execution stages
- Observable system behavior

---

## Status

Active development.

Current focus:

- receipt validation hardening
- canonical chain reconstruction
- execution integrity testing

---

## Author

Samantha Revita-Wagner  
Independent Systems Engineer
=======
This repo is a minimal, *verifiable* governed runtime:
- writes events as an **append-only JSONL ledger** (hash-linked)
- **verifies** integrity (detects chain breaks deterministically)
- **rebuilds** the chain when corrupted (rechain)
- **detects drift** via baseline + transition entropy
- runs a **governor loop** that advances state only inside operational boundaries

If you’ve ever had an “AI system” where nobody can prove what happened: this is the opposite of that.

---

## What you can prove (properties)

✅ **Tamper evidence:** mutate any record → `verify_events.py` fails with line number  
✅ **Chain integrity:** each record carries `prev` and a deterministic `hash`  
✅ **Recovery:** `rechain_events.py` reconstructs a consistent chain → verify passes again  
✅ **Drift tracking:** `drift_detector.py` creates/loads a baseline and reports drift  
✅ **Governed cycles:** `governor.py` runs cycles (A+B), updates head, and gates promotion by drift threshold

---

## Quickstart (clean run)

```bash
python verify_events.py
python governor.py --cycles 5 --do-model
python verify_events.py

```

## Origin & Authorship

Initial architecture and implementation by
Samantha Revita-Wagner.
Development began: March 2026.
This repository tracks the evolution of a deterministic execution-governance runtime with verifiable receipts.
