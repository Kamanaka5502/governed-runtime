import random

MAX_CYCLES = 200

pressure = 0.05
confidence = 0.50
healing_skill = 0.25

success_streak = 0
fail_streak = 0

adapt = False

# NEW
recovery_window = 0

def phase(p):
    if p < 0.20:
        return "BASELINE"
    elif p < 0.45:
        return "ELEVATED"
    elif p < 0.75:
        return "DEGRADED"
    else:
        return "CRITICAL"

print("=== RECOVERY MOMENTUM EXPERIMENT ===")

for cycle in range(1, MAX_CYCLES + 1):

    # catastrophe ramp
    if 20 < cycle <= 140:
        pressure += 0.01

    # release phase
    if cycle > 140:
        pressure -= 0.12 + random.uniform(-0.08, 0.08)

    pressure = max(0.0, pressure)

    ph = phase(pressure)

    # adaptive trigger
    adapt = (fail_streak >= 6) or (recovery_window > 0)

    # success probability
    success_chance = confidence * 0.6 + healing_skill * 0.4
    success = random.random() < success_chance

    if success:
        success_streak += 1
        fail_streak = 0

        conf_gain = 0.02
        heal_gain = 0.01

        # momentum boosts growth
        if recovery_window > 0:
            conf_gain *= 1.8
            heal_gain *= 1.5

        confidence += conf_gain
        healing_skill += heal_gain

        # stress rebound trigger
        if adapt and pressure > 0.60:
            confidence += 0.12
            healing_skill += 0.05
            recovery_window = 12   # NEW MAGIC

        commit = "OK"

    else:
        fail_streak += 1
        success_streak = 0

        conf_loss = 0.02
        heal_loss = 0.01

        # momentum reduces damage
        if recovery_window > 0:
            conf_loss *= 0.35
            heal_loss *= 0.50

        confidence -= conf_loss
        healing_skill -= heal_loss
        commit = "REJECTED"

    # tick down window
    if recovery_window > 0:
        recovery_window -= 1

    confidence = max(0.05, min(1.0, confidence))
    healing_skill = max(0.05, min(1.0, healing_skill))

    print(
        f"CYCLE {cycle:03} | "
        f"PHASE={ph:<9} | "
        f"P={pressure:.3f} | "
        f"CONF={confidence:.2f} | "
        f"HSK={healing_skill:.2f} | "
        f"RW={recovery_window:02} | "
        f"S={success_streak:02} | "
        f"F={fail_streak:02} | "
        f"ADAPT={'ON ' if adapt else 'OFF'} | "
        f"COMMIT={commit}"
    )

print("\nDone.")
