import importlib
import glob
import os

print("=== GOVERNED RUNTIME — STATE ORCHESTRATOR ===")

# ---------------------------------------------------
# Shared Living State
# ---------------------------------------------------
state = {
    "coherence": 0.85,
    "pressure": 0.2,
    "trust": 0.75,
    "memory": {},
    "history": [],
    "mode": "INITIALIZING"
}

# ---------------------------------------------------
# Layer Discovery
# ---------------------------------------------------
layers = sorted(glob.glob("layer*.py"))

print(f"Discovered {len(layers)} layers")

# ---------------------------------------------------
# Unified Layer Runner
# ---------------------------------------------------
def run_layer(layer_file, state):
    module_name = layer_file.replace(".py", "")

    print(f"\n--- Running {module_name} ---")

    try:
        mod = importlib.import_module(module_name)

        # Optional standard interface
        if hasattr(mod, "process"):
            state = mod.process(state)

        else:
            print("No process(state) function — demo mode only")

    except Exception as e:
        print(f"ERROR in {module_name}: {e}")

    return state

# ---------------------------------------------------
# Execute Stack
# ---------------------------------------------------
for layer in layers:
    state = run_layer(layer, state)
    state["history"].append(layer)

# ---------------------------------------------------
# Final Snapshot
# ---------------------------------------------------
print("\n=== FINAL STATE SNAPSHOT ===")
for k, v in state.items():
    if k != "history":
        print(f"{k}: {v}")

print(f"Layers Executed: {len(state['history'])}")
print("=== RUNTIME COMPLETE ===")
