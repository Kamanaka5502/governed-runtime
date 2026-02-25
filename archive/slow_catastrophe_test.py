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

LOG_FILE = "slow_catastrophe_log.jsonl"

# ==============================
# STATE
# ==============================

state = {
    "cycle": 0,
    "pressure": BASE_PRESSURE,
    "phase": "BASELINE",
    "recovery_active": True,
    "authority_conflict": False,
    "commit_integrity": "OK",
}

# ==============================
# SIM HELPERS
# ==============================

def evaluate_phase(s):
    if s["pressure"] < 0.20:
        return "BASELINE"
    elif s["pressure"] < 0.45:
        return "ELEVATED"
    elif s["pressure"] < 0.70:
        return "DEGRADED"
    else:
        return "CRITICAL"

def recovery_logic(s):
    if not s["recovery_active"]:
        return

    # aggressive recovery behavior
    s["pressure"] *= 0.75

def commit_logic(s):
    # simulated integrity degradation under sustained stress
    if s["pressure"] > 0.50:
        if random.random() < 0.3:
            s["commit_integrity"] = "REJECTED"
    else:
        s["commit_integrity"] = "OK"

def log_state(s):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(s) + "\n")

# ==============================
# EXPERIMENT PHASES
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
    print("[RELEASE] removing conflict + restoring recovery")
    state["authority_conflict"] = False
    state["recovery_active"] = True

    for _ in range(30):
        step()

# ==============================
# CORE STEP
# ==============================

def step():
    state["cycle"] += 1

    commit_logic(state)

    if state["commit_integrity"] == "REJECTED":
        state["pressure"] += 0.05

    state["phase"] = evaluate_phase(state)

    recovery_logic(state)

    log_state(state)

    print(
        f"CYCLE {state['cycle']:03d} | "
        f"PHASE={state['phase']:9s} | "
        f"P={state['pressure']:.3f} | "
        f"REC={'ON' if state['recovery_active'] else 'OFF'} | "
        f"AUTH={'Y' if state['authority_conflict'] else 'N'} | "
        f"COMMIT={state['commit_integrity']}"
    )

    time.sleep(0.05)

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    print("=== SLOW CATASTROPHE EXPERIMENT ===")

    run_baseline()
    run_catastrophe()
    release_phase()

    print("\nExperiment complete.")
    print(f"Log written to: {LOG_FILE}")
