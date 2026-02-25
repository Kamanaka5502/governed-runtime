#!/usr/bin/env python3
import time
import json
import random

# ==============================
# CONFIG
# ==============================

TOTAL_CYCLES = 120
PRESSURE_INCREMENT = 0.01
BASE_PRESSURE = 0.05

DISABLE_RECOVERY = True
FORCE_AUTHORITY_CONFLICT = True

LOG_FILE = "healing_catastrophe_log.jsonl"

# ==============================
# STATE
# ==============================

state = {
    "cycle": 0,
    "pressure": BASE_PRESSURE,
    "last_pressure": BASE_PRESSURE,
    "trend": 0.0,
    "phase": "BASELINE",
    "recovery_active": True,
    "authority_conflict": False,
    "commit_integrity": "OK",
    "confidence": 0.5,
    "critical_cycles": 0
}

# ==============================
# PHASE
# ==============================

def evaluate_phase(p):
    if p < 0.20:
        return "BASELINE"
    elif p < 0.45:
        return "ELEVATED"
    elif p < 0.70:
        return "DEGRADED"
    return "CRITICAL"

# ==============================
# TREND + MEMORY
# ==============================

def update_trend(s):
    s["trend"] = s["pressure"] - s["last_pressure"]
    s["last_pressure"] = s["pressure"]

def update_confidence(s):
    if s["trend"] < 0:
        s["confidence"] += 0.03
    else:
        s["confidence"] -= 0.03

    if s["phase"] == "CRITICAL":
        s["critical_cycles"] += 1
    else:
        s["critical_cycles"] = 0

    # survival rebound
    if s["critical_cycles"] > 8:
        s["confidence"] += 0.05

    s["confidence"] = max(0.1, min(1.0, s["confidence"]))

# ==============================
# RECOVERY
# ==============================

def recovery_factor(phase, confidence):
    base = {
        "BASELINE": (0.90, 0.98),
        "ELEVATED": (0.82, 0.95),
        "DEGRADED": (0.88, 1.00),
        "CRITICAL": (0.92, 1.05)
    }

    lo, hi = base[phase]

    shift = (1.0 - confidence) * 0.08
    lo += shift
    hi += shift

    return random.uniform(lo, hi)

def recovery_logic(s):
    if not s["recovery_active"]:
        return
    s["pressure"] *= recovery_factor(s["phase"], s["confidence"])

# ==============================
# COMMIT LOGIC (NOW HEALING)
# ==============================

def commit_logic(s):
    p = s["pressure"]

    # normal degradation
    if p > 0.50:
        if random.random() < 0.35:
            s["commit_integrity"] = "REJECTED"

    # NEW: healing condition
    if (
        s["commit_integrity"] == "REJECTED"
        and s["confidence"] > 0.85
        and s["trend"] < 0
        and p < 5.0
    ):
        # small chance each cycle to self-repair
        if random.random() < 0.25:
            s["commit_integrity"] = "OK"

    # baseline stability
    if p < 0.35 and random.random() < 0.85:
        s["commit_integrity"] = "OK"

# ==============================
# LOGGING
# ==============================

def log_state(s):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(s) + "\\n")

# ==============================
# PHASE RUNNERS
# ==============================

def run_baseline():
    print("[BASELINE] starting")
    for _ in range(20):
        step()
    print("[BASELINE] complete")

def run_catastrophe():
    print("[CATASTROPHE] starting")

    if DISABLE_RECOVERY:
        state["recovery_active"] = False
    if FORCE_AUTHORITY_CONFLICT:
        state["authority_conflict"] = True

    for _ in range(TOTAL_CYCLES):
        state["pressure"] += PRESSURE_INCREMENT
        step()

    print("[CATASTROPHE] complete")

def release_phase():
    print("[RELEASE] recovery restored")

    state["authority_conflict"] = False
    state["recovery_active"] = True

    for _ in range(60):
        step()

# ==============================
# CORE STEP
# ==============================

def step():
    state["cycle"] += 1

    update_trend(state)
    update_confidence(state)

    commit_logic(state)

    if state["commit_integrity"] == "REJECTED":
        state["pressure"] += 0.05

    state["phase"] = evaluate_phase(state["pressure"])

    recovery_logic(state)

    log_state(state)

    print(
        f"CYCLE {state['cycle']:03d} | "
        f"PHASE={state['phase']:9s} | "
        f"P={state['pressure']:.3f} | "
        f"TREND={state['trend']:+.3f} | "
        f"CONF={state['confidence']:.2f} | "
        f"CRIT={state['critical_cycles']:02d} | "
        f"REC={'ON' if state['recovery_active'] else 'OFF'} | "
        f"COMMIT={state['commit_integrity']}"
    )

    time.sleep(0.05)

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    print("=== SELF-HEALING EXPERIMENT ===")
    run_baseline()
    run_catastrophe()
    release_phase()

    print("\\nExperiment complete.")
    print(f"Log written to: {LOG_FILE}")
