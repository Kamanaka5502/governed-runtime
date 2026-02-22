import random
import time

# ==============================
# TORSO CORE — ADAPTIVE RUNTIME
# ==============================

# --- Baselines ---
concurrency = 1.0
maturity = 0.6
energy = 0.7

TARGET_CONCURRENCY = 2.0

MAX_CONCURRENCY = 5.0
MIN_CONCURRENCY = 1.0

memory = []

print("=== TORSO CORE (Metabolism + Homeostasis) ===")

for step in range(20):

    # --- External environment ---
    pressure = random.uniform(0.0, 1.0)
    stability = random.uniform(0.0, 1.0)

    # --- Maturity evolution ---
    delta_maturity = (stability - pressure) * 0.25
    maturity += delta_maturity
    maturity = max(0.0, min(1.0, maturity))

    # --- Memory field ---
    memory.append(maturity)
    if len(memory) > 6:
        memory.pop(0)

    mature_avg = sum(memory) / len(memory)

    # --- Metabolism ---
    load = pressure * 0.6
    recovery = stability * 0.4

    energy += recovery - load
    energy = max(0.0, min(1.0, energy))

    metabolic_rate = (energy + mature_avg) / 2

    # --- Growth signal ---
    growth_signal = (mature_avg - 0.5) * metabolic_rate

    # --- Homeostasis drift ---
    drift = TARGET_CONCURRENCY - concurrency
    growth_signal += drift * 0.05

    # --- Apply growth ---
    concurrency += growth_signal
    concurrency = max(MIN_CONCURRENCY,
                      min(MAX_CONCURRENCY, concurrency))

    # --- Output ---
    print(
        f"[{step}] "
        f"M={maturity:.2f} "
        f"Avg={mature_avg:.2f} "
        f"E={energy:.2f} "
        f"Meta={metabolic_rate:.2f} "
        f"C={concurrency:.2f}"
    )

    time.sleep(0.2)

print("\nFinal Concurrency:", round(concurrency, 3))
