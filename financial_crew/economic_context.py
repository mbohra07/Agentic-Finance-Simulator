# economic_context.py

import random

class EconomicContext:
    def __init__(self):
        self.inflation = 0.03  # 3%
        self.interest_rate = 0.04  # 4%
        self.cost_of_living_index = 100  # baseline

    def simulate_step(self):
        # Simulate inflation change: small random walk
        self.inflation += random.uniform(-0.005, 0.01)
        self.inflation = max(0.0, round(self.inflation, 4))

        # Interest rate is affected by inflation
        self.interest_rate += (self.inflation - 0.03) * 0.5
        self.interest_rate = max(0.0, round(self.interest_rate, 4))

        # Cost of living scales with inflation and a little noise
        self.cost_of_living_index *= (1 + self.inflation + random.uniform(-0.002, 0.002))
        self.cost_of_living_index = round(self.cost_of_living_index, 2)

    def get_context(self):
        return {
            "inflation": self.inflation,
            "interest_rate": self.interest_rate,
            "cost_of_living_index": self.cost_of_living_index
        }

    def __str__(self):
        return f"Inflation: {self.inflation*100:.2f}%, Interest: {self.interest_rate*100:.2f}%, Cost of Living Index: {self.cost_of_living_index:.2f}"