#!/usr/bin/env python
# src/financial_crew/main.py

import os
from crew import FinancialCrew

os.makedirs('output', exist_ok=True)

def run():
    print("\n💸 Welcome to the Financial Agent Simulator 💸")
    print("Please enter your details to begin the simulation:\n")

    # Collecting user input
    user_name = input("👤 Enter your name: ").strip()
    if not user_name:
        user_name = "Anonymous User"

    goal = input("🎯 Enter your financial goal (e.g., Save ₹10,000 in 3 months): ").strip()
    if not goal:
        goal = "Save ₹10,000 in 3 months"

    try:
        starting_balance = float(input("💰 Enter your starting balance in ₹ (e.g., 25000): ").strip())
    except ValueError:
        print("⚠️ Invalid number for balance. Defaulting to ₹25,000.")
        starting_balance = 25000

    # Running the crew with real input
    inputs = {
        'user_name': user_name,
        'goal': goal,
        'starting_balance': starting_balance
    }

    result = FinancialCrew().crew().kickoff(inputs=inputs)

    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)
    
    # Save the report
    with open("output/report.md", "w", encoding="utf-8") as f:
        f.write(result.raw)
        
    print("\n\n📄 Report has been saved to: output/report.md")

if __name__ == "__main__":
    run()