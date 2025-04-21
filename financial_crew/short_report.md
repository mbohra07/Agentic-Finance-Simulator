# Short Report

# Introduction

This project implements an AI-powered personal finance simulator that provides actionable insights into spending, savings, and financial goals. The simulation uses multiple agents that handle different aspects of financial management, such as identifying wasteful spending, tracking goal progress, and simulating emotional spending behaviors. A new Wellness Score feature has been added to quantify financial health and track learning progress over time.

# Agents and Their Logic

	1.	Spending Advisor:
	•	Goal: Help the user optimize their spending by analyzing cash flow data and identifying non-essential expenses.
	•	Logic: Analyzes spending patterns using data-driven insights and provides concrete suggestions. For example, it might identify high food delivery costs and suggest a weekly cooking challenge to reduce expenses.
	•	Behavioral Focus: Uses economic principles like marginal utility and opportunity cost to evaluate spending efficiency.

	2.	Goal Tracker:
	•	Goal: Track the user’s financial goals, such as saving a target amount or investing in a particular asset.
	•	Logic: Periodically updates the user on their progress towards the goal. It calculates how much has been saved and how much more is needed to reach the goal.
	•	Behavioral Focus: Provides concise updates and offers recommendations for accelerating goal achievement.

	3.	Emotional Bias Agent:
	•	Goal: Simulate emotional spending behaviors like retail therapy or guilt-driven splurging that may influence financial decisions.
	•	Logic: Introduces random emotional events at controlled intervals to simulate real-life emotional triggers that affect decision-making.
	•	Behavioral Focus: Helps the user recognize emotional biases in their financial decisions and offers strategies to counteract them.

	4.	Mentor Agent:
	•	Goal: Provide reflective guidance based on past financial behavior, helping the user stay on track for long-term growth.
	•	Logic: Reviews past financial decisions, identifies successes and areas for improvement, and offers actionable advice for building better financial habits.
	•	Behavioral Focus: Encourages long-term discipline and offers support in achieving sustainable financial growth.

# System Architecture

The system is built using the Crew AI framework, which allows for easy management and execution of tasks and agents. Each agent is defined with a specific role and goal, and tasks such as simulating cash flow or tracking goals are executed sequentially. The agents communicate with each other to provide a comprehensive view of the user’s financial behavior.

# Tasks and Simulations

	•	Simulate Cash Flow: This task simulates monthly inflows and outflows based on the user’s financial profile (e.g., salary, expenses, unexpected events). It generates a structured JSON file that tracks each transaction.

	•	Evaluate Spending: This task analyzes the simulated cash flow to identify inefficiencies and wasteful spending. It provides actionable suggestions to improve savings.

	•	Track Goals: This task evaluates the user’s progress toward their financial goal, offering insights and projections based on their current savings and spending behavior.

	•	Monthly Summary: At the end of the simulation, this task generates a summary report that consolidates all data, provides insights into the user’s behavior, and suggests improvements.

	•	Wellness Scoring: All simulation tasks now contribute to a real-time Financial Wellness Score (0-100) that evaluates spending discipline, savings efficiency, and goal progress, with personalized improvement tips generated after each simulation. The score appears in all reports and dashboards, visually tracking the user's financial learning curve over time.

# Memory Storage Implementation
	•	The memory components for the system have been fully integrated to enhance agent capabilities. However, due to limitations with the free version of the platform, these memory components are currently commented out. The intention is to activate them once higher resource limits are available.
    Long term memory, Short term memory and Entity memory
    Once the limitations are lifted, these memory features will be reactivated, allowing for more dynamic and adaptive agent behaviors.

# UI and User Interaction
	•	The system uses Streamlit to present the simulation in a clean, user-friendly interface. Streamlit helps to make the system interactive and accessible, providing a smooth experience for users to input data, view financial progress, and receive guidance from agents.

# Conclusion

The project provides a flexible and modular system for personal finance management, using AI agents to simulate various aspects of financial decision-making. By leveraging behavioral economics and AI technologies, the system helps users optimize their finances and achieve their goals while accounting for emotional biases and real-life constraints. The project’s design allows for easy expansion, making it a scalable solution for personal finance simulation and guidance.