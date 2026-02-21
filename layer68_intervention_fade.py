class InterventionFade:

    def __init__(self):
        self.level = 1.0

    def update(self, recovery_window):
        if recovery_window:
            self.level *= 0.9
        else:
            self.level = min(1.0, self.level + 0.05)

        return {"intervention_level": round(self.level,3)}

if __name__ == "__main__":
    f = InterventionFade()
    print("=== LAYER 68 — INTERVENTION FADE ===")

    demo = [False,False,True,True,True,True]
    for d in demo:
        print(f.update(d))
