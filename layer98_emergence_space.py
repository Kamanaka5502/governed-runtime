# ============================================================
# LAYER 98 — EMERGENCE SPACE
# "Change is allowed to stabilize itself."
# ============================================================

import math
import random

def process(state):

    # --------------------------------------------------------
    # READ STATE
    # --------------------------------------------------------
    pressure = state.get("pressure", 0.0)
    coherence = state.get("coherence", 0.0)
    micro_seed = state.get("micro_seed", 0.0)
    emergence_state = state.get("emergence_state", "QUIET")
    phase_momentum = state.get("phase_momentum", 0.0)

    # --------------------------------------------------------
    # SAFE EMERGENCE CONDITIONS
    # only allow expansion inside stable bands
    # --------------------------------------------------------
    safe_window = (
        pressure < 0.20 and
        coherence > 0.78
    )

    emergence_window = False
    resonance_gain = 0.0

    # --------------------------------------------------------
    # FREQUENCY POSSIBILITY (gentle oscillation field)
    # gives system something soft to lean into
    # --------------------------------------------------------
    wave = math.sin(random.uniform(0, math.pi * 2))

    if safe_window and emergence_state in ["SURGE", "ACTIVE"]:
        emergence_window = True

        # extremely small gain — this is NOT a shove
        resonance_gain = wave * 0.004

        pressure += resonance_gain
        coherence += abs(resonance_gain) * 0.45

        # tiny momentum encouragement
        phase_momentum += abs(resonance_gain) * 0.2

    # --------------------------------------------------------
    # HARD SAFETY LIMITS
    # --------------------------------------------------------
    pressure = max(0.0, min(1.0, pressure))
    coherence = max(0.0, min(1.0, coherence))
    phase_momentum = max(0.0, min(1.0, phase_momentum))

    # --------------------------------------------------------
    # WRITE BACK
    # --------------------------------------------------------
    state["pressure"] = pressure
    state["coherence"] = coherence
    state["phase_momentum"] = phase_momentum

    state["emergence_window"] = emergence_window
    state["frequency_wave"] = round(wave, 4)
    state["resonance_gain"] = round(resonance_gain, 6)

    print({
        "layer": "98_emergence_space",
        "emergence_window": emergence_window,
        "wave": round(wave, 4),
        "gain": round(resonance_gain, 6),
        "pressure": round(pressure, 4),
        "coherence": round(coherence, 4),
        "message": "SAFE_SPACE_GRANTED"
    })

    return state
