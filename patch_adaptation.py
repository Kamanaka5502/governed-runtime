def adaptation_factor(self):
    total = self.allow_count + self.constrain_count

    if total == 0:
        return 1.0

    bias = (self.allow_count - self.constrain_count) / total

    # nonlinear adaptation — stronger learning curve
    # squared curve amplifies consistent patterns
    adjusted = 1.0 - (bias * abs(bias) * 0.45)

    return max(0.6, min(adjusted, 1.2))
