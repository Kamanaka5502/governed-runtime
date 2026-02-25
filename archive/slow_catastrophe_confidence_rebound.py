import random

MAX_CYCLES = 200

pressure = 0.05
confidence = 0.50
healing_skill = 0.25

success_streak = 0
fail_streak = 0

adapt = False

def phase(p):
    if p < 0.20:
        return "BASELINE"
    elif p < 0.45:
        return "ELEVATED"
    elif p < 0.75:
        return "DEGRADED"
    else:
        return "CRITICAL"

print("=== CONFIDENCE REBOUND EXPERIMENT ===")

for cycle in range(1, MAX_CYCLES + 1):

    # catastrophe ramp
    if 20 < cycle <= 140:
        pressure += 0.01

    # release phase
    if cycle > 140:
        pressure -= 0.12 + random.uniform(-0.08,0.08)

    pressure = max(0.0, pressure)

    ph = phase(pressure)

    # adaptive mode
    adapt = fail_streak >= 6

    # success probability depends on confidence
    success_chance = confidence * 0.6 + healing_skill * 0.4
    success = random.random() < success_chance

    if success:
        success_streak += 1
        fail_streak = 0

        # normal recovery
        confidence += 0.02
        healing_skill += 0.01

        # ===== NEW MAGIC =====
        # success under stress causes rebound
        if adapt and pressure > 0.60:
            confidence += 0.12
            healing_skill += 0.05
        # =====================

        commit = "OK"

    else:
        fail_streak += 1
        success_streak = 0

        confidence -= 0.02
        healing_skill -= 0.01
        commit = "REJECTED"

    confidence = max(0.05, min(1.0, confidence))
    healing_skill = max(0.05, min(1.0, healing_skill))

    print(
        f"CYCLE {cycle:03} | "
        f"PHASE={ph:<9} | "
        f"P={pressure:.3f} | "
        f"CONF={confidence:.2f} | "
        f"HSK={healing_skill:.2f} | "
        f"S={success_streak:02} | "
        f"F={fail_streak:02} | "
        f"ADAPT={'ON ' if adapt else 'OFF'} | "
        f"COMMIT={commit}"
    )

print("\nDone.")
