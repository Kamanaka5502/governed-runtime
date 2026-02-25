import random

print("=== GOVERNED RUNTIME VALIDATION v4 (CLEAN) ===")

pressure = 0.05
confidence = 0.50
handshake = 0.25

rewrites = 0
success_streak = 0
fail_streak = 0

adapt_on = False

FAIL_LIMIT = 20
SYSTEM_FAILURE = False

for cycle in range(1, 301):

    # --------------------------------------------------
    # PRESSURE DRIFT (slow catastrophe)
    # --------------------------------------------------
    if cycle <= 150:
        pressure += 0.01
    else:
        pressure -= 0.015

    pressure = max(0.0, min(1.25, pressure))

    # --------------------------------------------------
    # PHASE
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
    # ADAPTATION (simple & clean)
    # --------------------------------------------------
    if fail_streak >= 6:
        adapt_on = True
    elif success_streak >= 3:
        adapt_on = False

    if adapt_on:
        confidence += 0.04
        handshake += 0.02
    else:
        confidence -= 0.01
        handshake -= 0.005

    # --------------------------------------------------
    # CLAMP
    # --------------------------------------------------
    confidence = max(0.0, min(1.0, confidence))
    handshake = max(0.0, min(1.0, handshake))

    # --------------------------------------------------
    # FAILURE CONDITION (THE POINT)
    # --------------------------------------------------
    if fail_streak >= FAIL_LIMIT:
        SYSTEM_FAILURE = True
        print("---- SYSTEM FAILURE DETECTED ----")

    # --------------------------------------------------
    # OUTPUT
    # --------------------------------------------------
    print(
        f"CYCLE {cycle:03d} | PHASE={phase:<9} | "
        f"P={pressure:.3f} | CONF={confidence:.2f} | "
        f"HSK={handshake:.2f} | RW={rewrites:02d} | "
        f"S={success_streak:02d} | F={fail_streak:02d} | "
        f"ADAPT={'ON ' if adapt_on else 'OFF'} | "
        f"COMMIT={commit_state}"
    )

    if SYSTEM_FAILURE:
        print(f"FAILED AT CYCLE {cycle}")
        break

if not SYSTEM_FAILURE:
    print("SURVIVED FULL RUN")
