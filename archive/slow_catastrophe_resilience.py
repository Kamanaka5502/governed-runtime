#!/usr/bin/env python3
import time, json, random

TOTAL_CYCLES = 120
PRESSURE_INCREMENT = 0.01
BASE_PRESSURE = 0.05

LOG_FILE = "resilience_catastrophe_log.jsonl"

state = {
    "cycle":0,
    "pressure":BASE_PRESSURE,
    "last_pressure":BASE_PRESSURE,
    "trend":0.0,
    "phase":"BASELINE",
    "confidence":0.5,
    "commit_integrity":"OK",
    "critical_cycles":0,
    "healing_skill":0.25,
    "failed_heals":0,
    "adaptive_mode":False,
    "recovery_active":True
}

def phase(p):
    if p < 0.20: return "BASELINE"
    if p < 0.45: return "ELEVATED"
    if p < 0.70: return "DEGRADED"
    return "CRITICAL"

def trend(s):
    s["trend"] = s["pressure"] - s["last_pressure"]
    s["last_pressure"] = s["pressure"]

def confidence(s):
    if s["trend"] < 0: s["confidence"] += 0.03
    else: s["confidence"] -= 0.03

    if s["phase"] == "CRITICAL":
        s["critical_cycles"] += 1
    else:
        s["critical_cycles"] = 0

    if s["critical_cycles"] > 8:
        s["confidence"] += 0.05

    s["confidence"] = max(0.1,min(1.0,s["confidence"]))

def recovery_multiplier(s):
    lo,hi = {
        "BASELINE":(0.90,0.98),
        "ELEVATED":(0.82,0.95),
        "DEGRADED":(0.88,1.00),
        "CRITICAL":(0.92,1.05)
    }[s["phase"]]

    # adaptive boost
    if s["adaptive_mode"]:
        lo -= 0.10
        hi -= 0.05

    return random.uniform(lo,hi)

def recovery(s):
    if s["recovery_active"]:
        s["pressure"] *= recovery_multiplier(s)

def commit_logic(s):
    p=s["pressure"]

    if p>0.50 and random.random()<0.35:
        s["commit_integrity"]="REJECTED"

    if (
        s["commit_integrity"]=="REJECTED"
        and s["confidence"]>0.85
        and s["trend"]<0
    ):
        chance=s["healing_skill"]

        if s["adaptive_mode"]:
            chance += 0.20

        if random.random()<chance:
            s["commit_integrity"]="OK"
            s["healing_skill"] += 0.02
            s["failed_heals"]=0
        else:
            s["healing_skill"] -= 0.01
            s["failed_heals"] += 1

    s["healing_skill"]=max(0.05,min(0.80,s["healing_skill"]))

def adapt_check(s):
    # activate resilience if stuck failing
    if (
        s["failed_heals"] >= 6
        and s["pressure"] > 2.0
    ):
        s["adaptive_mode"] = True

    # turn off once stable
    if s["adaptive_mode"] and s["pressure"] < 1.0:
        s["adaptive_mode"] = False
        s["failed_heals"] = 0

def log_state(s):
    with open(LOG_FILE,"a") as f:
        f.write(json.dumps(s)+"\\n")

def step():
    state["cycle"] +=1

    trend(state)
    confidence(state)
    commit_logic(state)

    if state["commit_integrity"]=="REJECTED":
        state["pressure"] += 0.05

    adapt_check(state)

    state["phase"]=phase(state["pressure"])
    recovery(state)

    log_state(state)

    print(
        f"CYCLE {state['cycle']:03d} | "
        f"PHASE={state['phase']:9s} | "
        f"P={state['pressure']:.3f} | "
        f"CONF={state['confidence']:.2f} | "
        f"HSK={state['healing_skill']:.2f} | "
        f"FAIL={state['failed_heals']:02d} | "
        f"ADAPT={'ON' if state['adaptive_mode'] else 'OFF'} | "
        f"COMMIT={state['commit_integrity']}"
    )

    time.sleep(0.05)

def baseline():
    print("[BASELINE]")
    for _ in range(20): step()

def catastrophe():
    print("[CATASTROPHE]")
    state["recovery_active"]=False
    for _ in range(TOTAL_CYCLES):
        state["pressure"] += PRESSURE_INCREMENT
        step()

def release():
    print("[RELEASE]")
    state["recovery_active"]=True
    for _ in range(60): step()

if __name__=="__main__":
    print("=== RESILIENCE MODE EXPERIMENT ===")
    baseline()
    catastrophe()
    release()
    print("\\nDone.")
