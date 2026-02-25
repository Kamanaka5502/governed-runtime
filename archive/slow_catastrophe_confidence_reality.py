#!/usr/bin/env python3
import random
import math

TOTAL_CYCLES = 200

# ---------- STATE ----------
pressure = 0.05
confidence = 0.50
healing_skill = 0.25

phase = "BASELINE"

success_streak = 0
fail_streak = 0

adapt_mode = False

# ---------- HELPERS ----------
def phase_from_pressure(p):
    if p < 0.20:
        return "BASELINE"
    elif p < 0.45:
        return "ELEVATED"
    elif p < 0.75:
        return "DEGRADED"
    return "CRITICAL"


def try_commit(p, conf, hsk, adapt):
    """
    Reality-based commit chance:
    higher pressure hurts
    confidence + healing skill help
    adapt mode gives mild boost
    """
    base = (conf * 0.45) + (hsk * 0.45)

    if adapt:
        base += 0.10

    penalty = min(p / 5.0, 0.85)

    chance = max(0.01, base - penalty)
    return random.random() < chance


print("=== CONFIDENCE REALITY EXPERIMENT ===")
print("[BASELINE]")

for cycle in range(1, TOTAL_CYCLES + 1):

    # ---- catastrophe injection ----
    if 21 <= cycle <= 140:
        pressure += 0.01

    # release phase
    if cycle == 141:
        print("[RELEASE]")
        pressure *= 0.93

    # natural cooling after release
    if cycle > 141:
        pressure += random.uniform(-0.25, 0.18)

    pressure = max(0.0, pressure)

    phase = phase_from_pressure(pressure)

    # ---------- SURVIVAL TWITCH ----------
    # If confidence bottoms out, occasionally force adaptation ON
    if confidence <= 0.10 and not adapt_mode:
        if random.random() < 0.08:   # 8% reflex chance
            adapt_mode = True

    # ---------- COMMIT ----------
    success = try_commit(pressure, confidence, healing_skill, adapt_mode)

    if success:
        commit = "OK"
        success_streak += 1
        fail_streak = 0

        # success increases confidence slightly
        confidence = min(1.0, confidence + 0.02)

        # mild learning
        healing_skill = min(1.0, healing_skill + 0.005)

    else:
        commit = "REJECTED"
        fail_streak += 1
        success_streak = 0

        # repeated failure erodes confidence
        confidence = max(0.05, confidence - 0.02)

        # prolonged failure slowly erodes skill
        if fail_streak > 2:
            healing_skill = max(0.05, healing_skill - 0.01)

    # ---------- ADAPT LOGIC ----------
    if fail_streak >= 6:
        adapt_mode = True

    if success_streak >= 3:
        adapt_mode = False
        fail_streak = 0

    # ---------- PRINT ----------
    print(
        f"CYCLE {cycle:03d} | "
        f"PHASE={phase:<9} | "
        f"P={pressure:0.3f} | "
        f"CONF={confidence:0.2f} | "
        f"HSK={healing_skill:0.2f} | "
        f"S={success_streak:02d} | "
        f"F={fail_streak:02d} | "
        f"ADAPT={'ON' if adapt_mode else 'OFF':<3} | "
        f"COMMIT={commit}"
    )

print("\nDone.")
