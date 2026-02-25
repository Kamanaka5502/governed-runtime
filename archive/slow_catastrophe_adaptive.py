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

LOG_FILE = "adaptive_catastrophe_log.jsonl"

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
# PHASE LOGIC
# ==============================

def evaluate_phase(s):
    p = s["pressure"]
    if p < 0.20:
        return "BASELINE"
    elif p < 0.45:
        return "ELEVATED"
    elif p < 0.70:
        return "DEGRADED"
    else:
        return "CRITICAL"

# ==============================
# ADAPTIVE RECOVERY (THE MAGIC)
# ==============================

def adaptive_recovery_factor(phase):
    """
    Recovery is now uncertain + phase-aware.
    High stress = weaker, less certain correction.
    """

    if phase == "BASELINE":
        return random.uniform(0.85, 0.95)   # gentle
    elif phase == "ELEVATED":
        return random.uniform(0.75, 0.90)   # moderate
    elif phase == "DEGRADED":
        return random.uniform(0.80, 0.98)   # hesitant
    else:  # CRITICAL
        return random.uniform(0.88, 1.02)   # may barely help (or fail)

def recovery_logic(s):
    if not s["recovery_active"]:
        return

    factor = adaptive_recovery_factor(s["phase"])
    s["pressure"] *= factor

# ==============================
# COMMIT LOGIC
# ==============================

def commit_logic(s):
    p = s["pressure"]

    if p > 0.50:
        if random.random() < 0.35:
            s["commit_integrity"] = "REJECTED"
    else:
        if random.random() < 0.85:
            s["commit_integrity"] = "OK"

# ==============================
# LOGGING
# ==============================

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
    print("[RELEASE] restoring recovery + removing conflict")

    state["authority_conflict"] = False
    state["recovery_active"] = True

    for _ in range(40):
        step()

# ==============================
# CORE LOOP
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
    print("=== ADAPTIVE RECOVERY EXPERIMENT ===")
    run_baseline()
    run_catastrophe()
    release_phase()

    print("\\nExperiment complete.")
    print(f"Log written to: {LOG_FILE}")
