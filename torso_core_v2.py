import random
import time

# ===============================
# TORSO CORE v2
# Metabolism + Homeostasis + Reserve Tank
# ===============================

# ---- CONFIG ----
MIN_CONCURRENCY = 1.0
MAX_CONCURRENCY = 5.0
TARGET_CONCURRENCY = 3.0

# ---- STATE ----
concurrency = 1.0
maturity = 0.6
energy = 0.8
reserve = 0.5          # <-- reserve tank (fasting buffer)
memory = []

print("=== TORSO CORE v2 (Reserve Tank) ===")

for step in range(25):

    # ---------------------------
    # Environment inputs
    # ---------------------------
    pressure = random.uniform(0.0, 1.0)
    stability = random.uniform(0.0, 1.0)

    # ---------------------------
    # Maturity update
    # ---------------------------
    delta = (stability - pressure) * 0.3
    maturity += delta
    maturity = max(0.0, min(1.0, maturity))

    # ---------------------------
    # Memory field (homeostasis)
    # ---------------------------
    memory.append(maturity)
    if len(memory) > 5:
        memory.pop(0)

    mature_avg = sum(memory) / len(memory)

    # ---------------------------
    # Energy dynamics
    # ---------------------------
    energy += (stability - pressure) * 0.2
    energy = max(0.0, min(1.0, energy))

    # ---------------------------
    # RESERVE TANK LOGIC
    # ---------------------------
    # fasting mode: pull reserve when depleted
    if energy < 0.3:
        pull = min(0.05, reserve)
        energy += pull
        reserve -= pull

    # abundance mode: refill reserve
    elif energy > 0.7:
        store = min(0.02, energy - 0.7)
        energy -= store
        reserve += store

    reserve = max(0.0, min(1.0, reserve))

    # ---------------------------
    # Metabolic rate
    # ---------------------------
    metabolic_rate = (energy + mature_avg) / 2.0

    # ---------------------------
    # Growth signal
    # ---------------------------
    growth_signal = (mature_avg - 0.5) * metabolic_rate

    # ---------------------------
    # Homeostasis drift
    # ---------------------------
    drift = TARGET_CONCURRENCY - concurrency
    growth_signal += drift * 0.05

    # ---------------------------
    # Apply growth
    # ---------------------------
    concurrency += growth_signal
    concurrency = max(MIN_CONCURRENCY,
                      min(MAX_CONCURRENCY, concurrency))

    # ---------------------------
    # Output
    # ---------------------------
    print(
        f"[{step}] "
        f"M={maturity:.2f} "
        f"Avg={mature_avg:.2f} "
        f"E={energy:.2f} "
        f"R={reserve:.2f} "
        f"Meta={metabolic_rate:.2f} "
        f"C={concurrency:.2f}"
    )

    time.sleep(0.2)

print("\nFinal Concurrency:", round(concurrency, 3))
