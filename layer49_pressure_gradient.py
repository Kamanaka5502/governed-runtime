class PressureGradientMonitor:
    def __init__(self):
        self.prev_pressure = None

    # ---------------------------------------------
    # GRADIENT CALCULATION
    # ---------------------------------------------
    def gradient(self, pressure):
        if self.prev_pressure is None:
            delta = 0.0
        else:
            delta = pressure - self.prev_pressure

        self.prev_pressure = pressure

        # interpret gradient
        if delta > 0.15:
            trend = "rising_fast"
        elif delta > 0.03:
            trend = "rising"
        elif delta < -0.15:
            trend = "falling_fast"
        elif delta < -0.03:
            trend = "falling"
        else:
            trend = "stable"

        return {
            "pressure": round(pressure, 3),
            "delta": round(delta, 3),
            "trend": trend
        }


# =============================================
# DEMO / TEST RUN
# =============================================

if __name__ == "__main__":
    pg = PressureGradientMonitor()

    print("=== LAYER 49 - PRESSURE GRADIENT ===")

    pressure_sequence = [
        0.30,
        0.42,
        0.55,
        0.78,  # rising fast
        0.82,
        0.70,
        0.50,  # falling fast
        0.48,
        0.47
    ]

    for p in pressure_sequence:
        result = pg.gradient(p)
        print(result)
