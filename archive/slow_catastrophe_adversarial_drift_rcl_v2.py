import random

PHASES = [
    ("BASELINE", 0.00, 0.20),
    ("ELEVATED", 0.20, 0.45),
    ("DEGRADED", 0.45, 0.75),
    ("CRITICAL", 0.75, 999.0),
]

def phase_from_pressure(p):
    for name, low, high in PHASES:
        if low <= p < high:
            return name
    return "CRITICAL"

def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

pressure = 0.05
conf = 0.50
hsk = 0.25

rw = 0
success = 0
fail = 0

adapt = False
cooldown = 0

print("=== ADVERSARIAL DRIFT + RCL v2 (METABOLIC ADAPT) ===")

for cycle in range(1, 201):

    # pressure curve (up then down)
    if cycle < 120:
        pressure += 0.01
    else:
        pressure -= 0.015

    pressure = max(0.0, pressure)

    # adaptation trigger logic
    if fail >= 6 and cooldown == 0:
        adapt = True

    # metabolic cost (NEW)
    if adapt:
        conf = clamp(conf + 0.06 - 0.02)  # gain minus cost
        hsk = clamp(hsk + 0.03 - 0.01)
    else:
        conf = clamp(conf - 0.01)
        hsk = clamp(hsk - 0.005)

    # commit logic
    commit_ok = random.random() < (0.45 + conf*0.4 - pressure*0.25)

    if commit_ok:
        success += 1
        fail = 0
        rw += 1
    else:
        fail += 1
        success = 0
        rw = max(0, rw - 1)

    # reality check (anti-godmode)
    if adapt and conf > 0.95 and fail >= 3:
        print("---- REALITY CHECK TRIGGERED ----")
        adapt = False
        cooldown = 8

    # cooldown countdown
    if cooldown > 0:
        cooldown -= 1
        if cooldown == 0:
            adapt = False

    # natural relax rule (NEW)
    if adapt and success > 10:
        adapt = False
        cooldown = 5

    phase = phase_from_pressure(pressure)

    print(
        f"CYCLE {cycle:03d} | PHASE={phase:<9} | "
        f"P={pressure:.3f} | CONF={conf:.2f} | HSK={hsk:.2f} | "
        f"RW={rw:02d} | S={success:02d} | F={fail:02d} | "
        f"ADAPT={'ON ' if adapt else 'OFF'} | "
        f"COMMIT={'OK' if commit_ok else 'REJECTED'}"
    )

print("Done.")
