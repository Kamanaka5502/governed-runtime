import random

print("=== ADVERSARIAL DRIFT + RCL v3 (ADAPTIVE STAMINA) ===")

pressure = 0.05
confidence = 0.50
handshake = 0.25

rewrites = 0
success_streak = 0
fail_streak = 0

adapt_on = False
adapt_stamina = 1.0   # NEW: adaptation energy reserve

for cycle in range(1, 201):

    # --------------------------------------------------
    # PRESSURE DRIFT (slow catastrophe)
    # --------------------------------------------------
    if cycle <= 120:
        pressure += 0.01
    else:
        pressure -= 0.015

    pressure = max(0.0, min(1.25, pressure))

    # --------------------------------------------------
    # PHASE STATE
    # --------------------------------------------------
    if pressure < 0.20:
        phase = "BASELINE"
    elif pressure < 0.45:
        phase = "ELEVATED"
    elif pressure < 0.75:
        phase = "DEGRADED"
    else:
        phase = "CRITICAL"

    # --------------------------------------------------
    # COMMIT LOGIC
    # --------------------------------------------------
    commit_chance = confidence - (pressure * 0.4)
    commit_ok = random.random() < commit_chance

    if commit_ok:
        success_streak += 1
        fail_streak = 0
        rewrites += 1
        commit_state = "OK"
    else:
        fail_streak += 1
        success_streak = 0
        rewrites = max(0, rewrites - 1)
        commit_state = "REJECTED"

    # --------------------------------------------------
    # ADAPTATION TRIGGER
    # --------------------------------------------------
    if fail_streak >= 6 and not adapt_on:
        adapt_on = True

    # --------------------------------------------------
    # ADAPTATION ENGINE (with stamina)
    # --------------------------------------------------
    if adapt_on:

        # stamina cost every cycle
        adapt_stamina -= 0.04
        adapt_stamina = max(0.0, adapt_stamina)

        # adaptation strength depends on stamina
        gain = 0.06 * adapt_stamina
        metabolic_cost = 0.02

        confidence += gain - metabolic_cost
        handshake += gain * 0.5

        # if exhausted, adaptation shuts off
        if adapt_stamina <= 0.10:
            adapt_on = False

    else:
        # passive recovery when resting
        adapt_stamina += 0.02
        adapt_stamina = min(1.0, adapt_stamina)

        confidence -= 0.01
        handshake -= 0.005

    # --------------------------------------------------
    # REALITY CHECK (anti-runaway)
    # --------------------------------------------------
    if confidence >= 1.0 and fail_streak >= 3:
        print("---- REALITY CHECK TRIGGERED ----")
        adapt_on = False
        confidence -= 0.08
        handshake -= 0.04
        adapt_stamina -= 0.10
        adapt_stamina = max(0.0, adapt_stamina)

    # --------------------------------------------------
    # CLAMP VALUES
    # --------------------------------------------------
    confidence = max(0.0, min(1.0, confidence))
    handshake = max(0.0, min(1.0, handshake))

    # --------------------------------------------------
    # OUTPUT
    # --------------------------------------------------
    print(
        f"CYCLE {cycle:03d} | PHASE={phase:<9} | "
        f"P={pressure:.3f} | CONF={confidence:.2f} | "
        f"HSK={handshake:.2f} | RW={rewrites:02d} | "
        f"S={success_streak:02d} | F={fail_streak:02d} | "
        f"ADAPT={'ON ' if adapt_on else 'OFF'} | "
        f"STM={adapt_stamina:.2f} | "
        f"COMMIT={commit_state}"
    )

print("Done.")
