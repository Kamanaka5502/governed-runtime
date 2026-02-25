import random

PHASES = ["BASELINE", "ELEVATED", "DEGRADED", "CRITICAL"]

pressure = 0.05
confidence = 0.50
handshake = 0.25
rw = 0
success = 0
fail = 0
adapt = False

drift = 0.0
environment_shift = False

def get_phase(p):
    if p < 0.20:
        return "BASELINE"
    elif p < 0.45:
        return "ELEVATED"
    elif p < 0.75:
        return "DEGRADED"
    return "CRITICAL"

print("=== ADVERSARIAL DRIFT EXPERIMENT ===")

for cycle in range(1, 201):

    # pressure increases slowly
    if cycle < 120:
        pressure += 0.01
    else:
        pressure -= 0.015

    pressure = max(0.0, pressure)

    # ENVIRONMENT LIES begin mid-run
    if cycle == 80:
        environment_shift = True
        print("---- ADVERSARIAL DRIFT ACTIVATED ----")

    if environment_shift:
        drift += 0.01

    # fake success probability (shifts under adaptation)
    truth_threshold = 0.55 - drift

    commit_ok = random.random() < truth_threshold

    if commit_ok:
        success += 1
        fail = 0
        rw = min(11, rw + 1)
    else:
        fail += 1
        success = 0
        rw = max(0, rw - 1)

    # adaptation logic
    if fail >= 6:
        adapt = True
    if success >= 8:
        adapt = False

    # adaptation increases perceived confidence
    if adapt:
        confidence = min(1.0, confidence + 0.06)
        handshake = min(1.0, handshake + 0.03)
    else:
        confidence = max(0.05, confidence - 0.01)
        handshake = max(0.05, handshake - 0.005)

    phase = get_phase(pressure)

    print(
        f"CYCLE {cycle:03d} | "
        f"PHASE={phase:<9} | "
        f"P={pressure:.3f} | "
        f"CONF={confidence:.2f} | "
        f"HSK={handshake:.2f} | "
        f"RW={rw:02d} | "
        f"S={success:02d} | "
        f"F={fail:02d} | "
        f"ADAPT={'ON ' if adapt else 'OFF'} | "
        f"COMMIT={'OK' if commit_ok else 'REJECTED'}"
    )

print("\nDone.")
