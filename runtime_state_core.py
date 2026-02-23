# =========================================================
# GOVERNED RUNTIME — STATE ORCHESTRATOR
# FULL CAP VERSION — NUMERICAL ORDER + STAGED EXECUTION
# =========================================================

import os
import glob
import importlib.util
import re

print("""
╔══════════════════════════════════════════════════════════════╗
║                  GOVERNED RUNTIME v1.3                       ║
║            FULL CAP + EOS GOVERNANCE EXECUTION               ║
╚══════════════════════════════════════════════════════════════╝
""")

# =========================================================
# BASE STATE
# =========================================================
state = {
    "coherence": 0.85,
    "pressure": 0.2,
    "trust": 0.75,
    "energy": 1.0,
    "drift": 0.0,
    "velocity": 0.0,
    "phase": "BASELINE",
    "mode": "INITIALIZING",
}

# =========================================================
# DISCOVER LAYERS
# =========================================================
layer_files = sorted(glob.glob("layer*.py"))

print(f"Discovered {len(layer_files)} layers")

# =========================================================
# HELPERS
# =========================================================
def extract_number(filename):
    match = re.search(r"layer(\d+)", filename)
    return int(match.group(1)) if match else 9999


def load_module(path):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def metabolic_tick(state):
    state["pressure"] *= 0.99
    state["drift"] *= 0.95
    state["energy"] = min(1.0, state["energy"] + 0.002)

    state["coherence"] = max(
        0.0,
        min(1.0, state["coherence"] - (state["pressure"] * 0.002))
    )
    return state


# =========================================================
# STAGED EXECUTION MODEL (FULL CAP)
# =========================================================
LAYER_STAGES = {
    "INIT": range(1, 21),
    "GOVERNANCE": range(21, 61),
    "HOMEOSTASIS": range(61, 81),
    "ANALYSIS": range(81, 94),
    "TEMPORAL": range(94, 99),
    "REFLECTION": range(99, 100),
    "EOS": range(100, 101),
}

layers_executed = 0

# =========================================================
# EXECUTION LOOP
# =========================================================
for stage, rng in LAYER_STAGES.items():

    print(f"\n=== STAGE: {stage} ===")

    for file in layer_files:

        num = extract_number(file)

        if num not in rng:
            continue

        name = os.path.splitext(os.path.basename(file))[0]
        print(f"--- Running {name} ---")

        try:
            module = load_module(file)

            if hasattr(module, "process"):
                state = module.process(state)
                print("process(state) executed")
            else:
                print("No process(state) function — skipped")

            state = metabolic_tick(state)
            layers_executed += 1

        except Exception as e:
            print(f"Layer failed: {e}")

# =========================================================
# FINAL CLASSIFICATION
# =========================================================
if state["pressure"] > 0.8:
    state["mode"] = "CRITICAL"
elif state["pressure"] > 0.5:
    state["mode"] = "GUARD"
else:
    state["mode"] = "STABLE"

# =========================================================
# FINAL SNAPSHOT
# =========================================================
print("\n============================================================")
print("FINAL STATE SNAPSHOT")
print("============================================================")

for k, v in state.items():
    print(f"{k}: {v}")

print(f"\nLayers Executed: {layers_executed}")

print("\n============================================================")
print("RUNTIME COMPLETE")
print("============================================================")
