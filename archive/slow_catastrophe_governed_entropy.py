import random

PRESSURE = 0.05
CONF = 0.5
HSK = 0.25

RW = 0
success_streak = 0
failure_streak = 0
adapt = False

phase = "BASELINE"

print("=== GOVERNED ENTROPY (MOVING TARGET) ===")

for cycle in range(1, 201):

    # --- phase logic ---
    if PRESSURE < 0.2:
        phase = "BASELINE"
    elif PRESSURE < 0.45:
        phase = "ELEVATED"
    elif PRESSURE < 0.75:
        phase = "DEGRADED"
    else:
        phase = "CRITICAL"

    # --- environment changes ---
    # world gets harder mid-run
    if cycle == 80:
        print("---- ENVIRONMENT SHIFT: rules changed ----")

    difficulty = 1.0
    if cycle >= 80:
        difficulty = 1.4  # moving target

    # --- commit probability ---
    commit_prob = CONF * HSK / difficulty
    commit_ok = random.random() < commit_prob

    # --- adaptation trigger ---
    if failure_streak >= 7:
        adapt = True
    if success_streak >= 12:
        adapt = False

    # --- update streaks ---
    if commit_ok:
        success_streak += 1
        failure_streak = 0
        RW = min(11, RW + 1)
    else:
        failure_streak += 1
        success_streak = 0
        RW = max(0, RW - 1)

    # --- governed adaptation ---
    if adapt:
        CONF = min(1.0, CONF + 0.06)
        HSK = min(1.0, HSK + 0.03)
    else:
        CONF = max(0.05, CONF - 0.01)
        HSK = max(0.05, HSK - 0.005)

    # --- pressure dynamics ---
    if cycle < 140:
        PRESSURE += 0.01
    else:
        PRESSURE -= (RW / 70.0)

    PRESSURE = max(0.0, PRESSURE)

    print(
        f"CYCLE {cycle:03d} | PHASE={phase:<9} | "
        f"P={PRESSURE:.3f} | CONF={CONF:.2f} | HSK={HSK:.2f} | "
        f"RW={RW:02d} | S={success_streak:02d} | F={failure_streak:02d} | "
        f"ADAPT={'ON ' if adapt else 'OFF'} | "
        f"COMMIT={'OK' if commit_ok else 'REJECTED'}"
    )

print("\nDone.")
