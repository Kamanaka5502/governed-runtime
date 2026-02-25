#!/usr/bin/env python3
import time
import json
import random

TOTAL_CYCLES = 120
PRESSURE_INCREMENT = 0.01
BASE_PRESSURE = 0.05

DISABLE_RECOVERY = True
FORCE_AUTHORITY_CONFLICT = True

LOG_FILE = "learning_catastrophe_log.jsonl"

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
    "critical_cycles": 0,
    "healing_skill": 0.25
}

def evaluate_phase(p):
    if p < 0.20: return "BASELINE"
    if p < 0.45: return "ELEVATED"
    if p < 0.70: return "DEGRADED"
    return "CRITICAL"

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

    if s["critical_cycles"] > 8:
        s["confidence"] += 0.05

    s["confidence"] = max(0.1, min(1.0, s["confidence"]))

def recovery_factor(phase, confidence):
    base = {
        "BASELINE": (0.90,0.98),
        "ELEVATED": (0.82,0.95),
        "DEGRADED": (0.88,1.00),
        "CRITICAL": (0.92,1.05)
    }
    lo,hi = base[phase]
    shift = (1-confidence)*0.08
    return random.uniform(lo+shift, hi+shift)

def recovery_logic(s):
    if not s["recovery_active"]:
        return
    s["pressure"] *= recovery_factor(s["phase"], s["confidence"])

def commit_logic(s):
    p = s["pressure"]

    if p > 0.50:
        if random.random() < 0.35:
            s["commit_integrity"] = "REJECTED"

    # adaptive healing
    if (
        s["commit_integrity"] == "REJECTED"
        and s["confidence"] > 0.85
        and s["trend"] < 0
        and p < 5.0
    ):
        if random.random() < s["healing_skill"]:
            s["commit_integrity"] = "OK"
            s["healing_skill"] += 0.02   # success reinforces
        else:
            s["healing_skill"] -= 0.01   # failure discourages

    s["healing_skill"] = max(0.05, min(0.80, s["healing_skill"]))

    if p < 0.35 and random.random() < 0.85:
        s["commit_integrity"] = "OK"

def log_state(s):
    with open(LOG_FILE,"a") as f:
        f.write(json.dumps(s)+"\\n")

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
        f"HSK={state['healing_skill']:.2f} | "
        f"COMMIT={state['commit_integrity']}"
    )

    time.sleep(0.05)

def run_baseline():
    print("[BASELINE]")
    for _ in range(20): step()

def run_catastrophe():
    print("[CATASTROPHE]")
    state["recovery_active"]=False
    state["authority_conflict"]=True
    for _ in range(TOTAL_CYCLES):
        state["pressure"] += PRESSURE_INCREMENT
        step()

def release():
    print("[RELEASE]")
    state["recovery_active"]=True
    state["authority_conflict"]=False
    for _ in range(60): step()

if __name__=="__main__":
    print("=== LEARNING HEALING EXPERIMENT ===")
    run_baseline()
    run_catastrophe()
    release()
    print("\\nDone.")
