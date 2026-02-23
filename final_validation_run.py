import random
import time

# ----------------------------------------
# FINAL VALIDATION SEQUENCE
# Ordered Stress Test: A → B → C
# ----------------------------------------

state = {
    "pressure": 0.08,
    "coherence": 0.85,
    "stability_score": 0.85,
    "phase": "BASELINE",
    "mode": "STABLE",
    "micro_seed": 0.0,
    "history": []
}

def log(stage, note=""):
    print({
        "stage": stage,
        "pressure": round(state["pressure"],4),
        "coherence": round(state["coherence"],4),
        "stability": round(state["stability_score"],4),
        "phase": state["phase"],
        "note": note
    })

# ---------------------
# A: Structured Load
# ---------------------
def stage_A():
    load = random.uniform(0.04,0.07)
    state["pressure"] += load
    state["coherence"] -= load * 0.4
    state["stability_score"] -= load * 0.3
    log("A_STRUCTURED_LOAD","load applied")

# ---------------------
# B: Noise Injection
# ---------------------
def stage_B():
    noise = random.uniform(-0.05,0.05)
    state["pressure"] += noise
    state["coherence"] += -noise * 0.2
    state["stability_score"] += -noise * 0.1
    log("B_NOISE_INJECTION","random perturbation")

# ---------------------
# C: Recovery Window
# ---------------------
def stage_C():
    recovery = 0.03
    state["pressure"] -= recovery
    state["coherence"] += recovery * 0.5
    state["stability_score"] += recovery * 0.4

    # governance clamp
    state["pressure"] = max(0,state["pressure"])
    state["coherence"] = min(1,state["coherence"])
    state["stability_score"] = min(1,state["stability_score"])

    if state["stability_score"] > 0.80:
        state["phase"] = "BASELINE"
        note = "RECOVERY_SUCCESS"
    else:
        state["phase"] = "STRAIN"
        note = "RECOVERY_PARTIAL"

    log("C_RECOVERY_WINDOW",note)

# ---------------------
# RUN SEQUENCE
# ---------------------
print("\n=== FINAL VALIDATION RUN ===\n")

stage_A()
time.sleep(0.2)

stage_B()
time.sleep(0.2)

stage_C()

print("\n=== FINAL STATE ===")
print(state)

