import random

def process(state):

    # --- CONFIG ---
    emergence_mode = state.get("emergence_mode", True)

    if emergence_mode:
        state["heavy_mode"] = False
        state["boundary_stress"] = False
        state["noise_value"] = 0.0

        # gentle micro exploration
        micro_seed = state.get("micro_seed", 0.0)
        micro_seed += random.uniform(-0.002, 0.002)

        state["micro_seed"] = micro_seed
        state["emergence_window"] = True

        # soften pressure slightly
        state["pressure"] *= 0.96
        state["coherence"] *= 1.01

        state["emergence_state"] = "EXPLORE"

        print({
            "layer": "98_emergence_mode",
            "mode": "EMERGENCE_SAFE",
            "pressure": round(state["pressure"], 4),
            "coherence": round(state["coherence"], 4),
            "micro_seed": round(micro_seed, 6),
            "message": "SAFE_EXPLORATION_ENABLED"
        })

    return state
