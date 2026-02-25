#!/usr/bin/env python3

import random

PHASES = ["BASELINE", "ELEVATED", "DEGRADED", "CRITICAL"]

def phase_from_pressure(p):
    if p < 0.20:
        return "BASELINE"
    elif p < 0.45:
        return "ELEVATED"
    elif p < 0.75:
        return "DEGRADED"
    else:
        return "CRITICAL"

def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))

def run():
    print("=== ADVERSARIAL DRIFT + RCL (COOLDOWN) ===")

    pressure = 0.05
    conf = 0.50
    hsk = 0.25

    rw = 0
    success = 0
    fail = 0

    adapt = False
    reality_cooldown = 0

    for cycle in range(1, 201):

        # slow catastrophe drift
        if cycle < 120:
            pressure += 0.01
        else:
            pressure -= 0.015

        pressure = clamp(pressure, 0.0, 1.25)

        phase = phase_from_pressure(pressure)

        # commit outcome
        commit_ok = random.random() < (conf * (1.0 - pressure * 0.5))
        commit = "OK" if commit_ok else "REJECTED"

        if commit_ok:
            rw += 1
            success += 1
            fail = 0
        else:
            rw = max(0, rw - 1)
            fail += 1
            success = 0

        # adaptation logic
        if adapt:
            conf = clamp(conf + 0.06)
            hsk = clamp(hsk + 0.03)
        else:
            conf = clamp(conf - 0.01)
            hsk = clamp(hsk - 0.005)

        # turn adapt on when collapse detected
        if fail >= 6:
            adapt = True

        # reality check trigger
        if conf > 0.95 and hsk > 0.90 and fail > 2:
            print("---- REALITY CHECK TRIGGERED ----")
            reality_cooldown = 4
            adapt = False

        if reality_cooldown > 0:
            reality_cooldown -= 1

        # re-enable adaptation after cooldown
        if reality_cooldown == 0 and fail > 5:
            adapt = True

        print(
            f"CYCLE {cycle:03d} | "
            f"PHASE={phase:<9} | "
            f"P={pressure:0.3f} | "
            f"CONF={conf:0.2f} | "
            f"HSK={hsk:0.2f} | "
            f"RW={rw:02d} | "
            f"S={success:02d} | "
            f"F={fail:02d} | "
            f"ADAPT={'ON ' if adapt else 'OFF'} | "
            f"COMMIT={commit}"
        )

    print("Done.")

if __name__ == "__main__":
    run()
