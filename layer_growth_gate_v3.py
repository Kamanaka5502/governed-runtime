import random
import time

concurrency = 1.0
maturity = 0.6

MAX_CONCURRENCY = 5.0
MIN_CONCURRENCY = 1.0

memory = []

print("=== Adaptive Growth Gate v3 (Memory) ===")

for step in range(12):

    pressure = random.uniform(0.0, 1.0)
    stability = random.uniform(0.0, 1.0)

    delta = (stability - pressure) * 0.3
    maturity += delta
    maturity = max(0.0, min(1.0, maturity))

    # ← MEMORY FIELD
    memory.append(maturity)
    if len(memory) > 5:
        memory.pop(0)

    mature_avg = sum(memory) / len(memory)

    growth_signal = (mature_avg - 0.5) * 0.8

    concurrency += growth_signal
    concurrency = max(MIN_CONCURRENCY,
                      min(MAX_CONCURRENCY, concurrency))

    print(f"[{step}] M={maturity:.2f} Avg={mature_avg:.2f} C={concurrency:.2f}")

    time.sleep(0.2)

print("\nFinal:", concurrency)
