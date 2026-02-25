# ============================================================
# LAYER 98 — FREQUENCY RESONANCE FIELD
# Optional resonance channel for emergence support
# ============================================================

import math
import time


def process(state):

    pressure = state.get("pressure", 0.0)
    coherence = state.get("coherence", 0.0)
    micro_seed = state.get("micro_seed", 0.0)
    emergence_state = state.get("emergence_state", "QUIET")

    # --------------------------------------------------------
    # FREQUENCY MODEL
    # Creates a slow oscillation based on runtime time.
    # This is NOT random — it is smooth and predictable.
    # --------------------------------------------------------

    t = time.time()
    frequency_wave = math.sin(t * 0.15)

    resonance_active = False
    resonance_gain = 0.0

    # --------------------------------------------------------
    # CONDITIONS FOR RESONANCE
    # Allow influence ONLY when system is stable enough.
    # --------------------------------------------------------

    if coherence > 0.82 and pressure < 0.12:
        resonance_active = True

        # gentle coupling
        resonance_gain = frequency_wave * 0.004

        pressure += resonance_gain
        coherence += resonance_gain * 0.5

        # emergence encouragement (not forcing)
        if emergence_state == "QUIET" and abs(resonance_gain) > 0.0025:
            state["emergence_state"] = "ACTIVE"

    # --------------------------------------------------------
    # SAFETY BOUNDS
    # --------------------------------------------------------

    pressure = max(0.0, min(1.0, pressure))
    coherence = max(0.0, min(1.0, coherence))

    state["pressure"] = pressure
    state["coherence"] = coherence
    state["frequency_wave"] = round(frequency_wave, 4)
    state["resonance_active"] = resonance_active
    state["resonance_gain"] = round(resonance_gain, 6)

    print({
        "layer": "98_frequency_resonance",
        "resonance_active": resonance_active,
        "wave": round(frequency_wave, 4),
        "gain": round(resonance_gain, 6),
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4),
        "message": "FIELD_STABILIZED"
    })

    return state
