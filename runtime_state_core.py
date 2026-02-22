# =========================================================
# GOVERNED RUNTIME — STATE ORCHESTRATOR (FULL CAT)
# =========================================================

import glob
import importlib.util
import os

print("=== GOVERNED RUNTIME START ===")

# ---- BASE STATE ----
state = {
    "coherence": 0.85,
    "pressure": 0.2,
    "trust": 0.75,
    "energy": 1.0,
    "drift": 0.0,
    "velocity": 0.0,
    "phase": "BASELINE",
    "mode": "INITIALIZING"
}

# ---- DISCOVER LAYERS ----
layer_files = sorted(glob.glob("layer*.py"))
print(f"Discovered {len(layer_files)} layers")


# ---- SAFE MODULE LOADER ----
def load_module(path):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---- METABOLIC TICK ----
def metabolic_tick(state):

    # pressure naturally decays
    state["pressure"] *= 0.99

    # drift fades over time
    state["drift"] *= 0.95

    # energy slowly restores
    state["energy"] = min(1.0, state["energy"] + 0.002)

    # coherence slightly affected by pressure
    state["coherence"] = max(
        0.0,
        min(1.0, state["coherence"] - (state["pressure"] * 0.002))
    )

    return state


# ---- MAIN LOOP ----
layers_executed = 0

for file in layer_files:

    name = os.path.splitext(os.path.basename(file))[0]
    print(f"\n--- Running {name} ---")

    try:
        module = load_module(file)

        if hasattr(module, "process"):
            try:
                state = module.process(state)
                print("process(state) executed")
            except Exception as e:
                print(f"process(state) error: {e}")
        else:
            print("No process(state) function — demo mode only")

        # ALWAYS RUN METABOLISM
        state = metabolic_tick(state)
        layers_executed += 1

    except Exception as e:
        print(f"Layer load failed: {e}")


# ---- FINAL CLASSIFICATION ----
if state["pressure"] > 0.8:
    state["mode"] = "CRITICAL"
elif state["pressure"] > 0.5:
    state["mode"] = "GUARD"
else:
    state["mode"] = "STABLE"


# ---- OUTPUT ----
print("\n=== FINAL STATE SNAPSHOT ===")
for k, v in state.items():
    print(f"{k}: {v}")

print(f"Layers Executed: {layers_executed}")
print("=== RUNTIME COMPLETE ===")

