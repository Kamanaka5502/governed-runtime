import random
import time

concurrency = 1.0
maturity = 0.6   # <-- start above threshold

MAX_CONCURRENCY = 5.0
MIN_CONCURRENCY = 1.0

print("=== Adaptive Growth Gate v2 ===")

for step in range(10):

    pressure = random.uniform(0.0, 1.0)
    stability = random.uniform(0.0, 1.0)

    delta_maturity = (stability - pressure) * 0.3
    maturity += delta_maturity
    maturity = max(0.0, min(1.0, maturity))

    growth_signal = (maturity - 0.5) * 0.8

    concurrency += growth_signal
    concurrency = max(MIN_CONCURRENCY, min(MAX_CONCURRENCY, concurrency))

    print(f"[{step}] M={maturity:.2f} C={concurrency:.2f}")

    time.sleep(0.2)

print("\nFinal:", concurrency)

def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({
        "layer": "_growth_gate_v2",
        "status": "active"
    })

    return state
