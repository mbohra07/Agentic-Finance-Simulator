import os
import json
import streamlit as st
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("output")

def get_simulation_files(simulation_num: int):
    """Generate file paths for a specific simulation number"""
    return {
        "cash_flow": OUTPUT_DIR / f"simulated_cashflow_simulation_{simulation_num}.json",
        "spending_review": OUTPUT_DIR / f"spending_review_simulation_{simulation_num}.json",
        "goal_tracking": OUTPUT_DIR / f"goal_tracking_simulation_{simulation_num}.json",
        "monthly_summary": OUTPUT_DIR / f"monthly_summary_simulation_{simulation_num}.json",
        "coordinator_decision": OUTPUT_DIR / f"coordinator_decision_simulation_{simulation_num}.json",
        "discipline_tracker": OUTPUT_DIR / f"discipline_tracker_simulation_{simulation_num}.json",
        "behavior_tracker": OUTPUT_DIR / f"behavior_tracker_simulation_{simulation_num}.json",
        "karma_tracker": OUTPUT_DIR / f"karmic_tracker_simulation_{simulation_num}.json",
        "mentor_advice": OUTPUT_DIR / f"mentor_advice_simulation_{simulation_num}.json",
        "financial_strategy": OUTPUT_DIR / f"financial_strategy_simulation_{simulation_num}.json"
    }

# --- Cash Flow Simulation ---
def display_cash_flow(sim_no):
    try:
        cashflow_path = f"output/simulated_cashflow_simulation_{sim_no}.json"
        if os.path.exists(cashflow_path):
            with open(cashflow_path, "r") as f:
                cashflow_data = json.load(f)
            st.subheader("💰 Daily Cash Flow Simulation")
            total_inflows = sum(sum(day["inflows"].values()) for day in cashflow_data)
            total_outflows = sum(sum(day["outflows"].values()) for day in cashflow_data)
            net_savings = total_inflows - total_outflows
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Inflows", f"₹{total_inflows:,.2f}")
            col2.metric("Total Outflows", f"₹{total_outflows:,.2f}")
            col3.metric("Net Savings", f"₹{net_savings:,.2f}")
            with st.expander("📅 View Detailed Transactions"):
                df = pd.DataFrame([{
                    "Date": day["date"],
                    "Inflows": sum(day["inflows"].values()),
                    "Outflows": sum(day["outflows"].values()),
                    "Balance": day["balance"],
                    "Notes": ", ".join([f"{k}: ₹{v}" for k, v in {**day["inflows"], **day["outflows"]}.items()])
                } for day in cashflow_data])
                st.dataframe(df.style.format({
                    "Inflows": "₹{:.2f}",
                    "Outflows": "₹{:.2f}",
                    "Balance": "₹{:.2f}"
                }))
            st.markdown("---")
            st.subheader("📈 Balance Over Time")
            st.line_chart(df.set_index("Date")["Balance"])
            st.subheader("📊 Spending Distribution")
            spending = {}
            for day in cashflow_data:
                for category, amount in day["outflows"].items():
                    spending[category] = spending.get(category, 0) + amount
            if spending:
                spending_df = pd.DataFrame({
                    "Category": list(spending.keys()),
                    "Amount": list(spending.values())
                }).sort_values("Amount", ascending=False)
                col1, col2 = st.columns(2)
                with col1:
                    st.bar_chart(spending_df.set_index("Category"))
                with col2:
                    st.dataframe(spending_df.style.format({"Amount": "₹{:.2f}"}))
            notable_days = [day for day in cashflow_data if "note" in day]
            if notable_days:
                st.subheader("🌟 Notable Events")
                for day in notable_days:
                    st.markdown(f"**{day['date']}**: {day['note']}")
        else:
            st.warning("Cash flow data not found. Please run the simulation first.")
    except Exception as e:
        st.error(f"Cash Flow Error: {e}")

# --- Spending Review ---
def display_spending_review(sim_no):
    try:
        review_path = f"output/spending_review_simulation_{sim_no}.json"
        if os.path.exists(review_path):
            with open(review_path, "r") as f:
                review_data = json.load(f)
            st.subheader("💡 Spending Review & Suggestions")
            for obj in review_data:
                st.markdown(f"**User:** {obj['user_name']}, **Occupation:** {obj['occupation']}, **Goal:** {obj['goal']}")
                st.write(f"**Savings Rate:** {obj['savings_rate']}")
                st.write("**Top Wasteful Expenses:**")
                st.table(pd.DataFrame(obj['top_wasteful_expenses']))
                st.write("**Overspending Categories:**")
                st.table(pd.DataFrame(obj['overspending_categories']))
                sra = obj['savings_rate_assessment']
                st.write(f"**Savings Rate Assessment:** Current: {sra['current_rate']}, Suggested: {sra['suggested_improvement']}, Notes: {sra['notes']}")
                st.write("**Consistency Tips:**")
                for tip in obj.get('consistency_tips', []):
                    st.markdown(f"- {tip}")
        else:
            st.warning("Spending review not found. Please run the simulation first.")
    except Exception as e:
        st.error(f"Error reading spending review data: {e}")

# --- Goal Tracking ---
def display_goal_tracking(sim_no):
    try:
        goal_path = f"output/goal_tracking_simulation_{sim_no}.json"
        if os.path.exists(goal_path):
            with open(goal_path, "r") as f:
                goal_data = json.load(f)
            st.subheader("🎯 Goal Progress Tracking")
            for obj in goal_data:
                st.write(f"**Goal:** {obj['goal']}")
                st.write(f"**Achieved:** {obj['achieved_percentage']}%")
                st.write(f"**Projected Amount:** ₹{obj['projected_amount']}")
                st.write(f"**Time Left:** {obj['time_left']}")
                st.info(obj['economic_adjustments_tip'])
                st.progress(obj['achieved_percentage'] / 100)
        else:
            st.warning("Goal tracking data not found. Please run the simulation first.")
    except Exception as e:
        st.error(f"Error reading goal tracking data: {e}")

# --- Monthly Summary ---
def display_monthly_summary(sim_no):
    try:
        summary_path = f"output/monthly_summary_simulation_{sim_no}.json"
        if os.path.exists(summary_path):
            with open(summary_path, "r") as f:
                summary_data = json.load(f)
            st.subheader("📋 Monthly Financial Summary")
            obj = summary_data[0] if isinstance(summary_data, list) else summary_data
            overview = obj.get("overview", {})
            cash = overview.get("cash_flow_summary", {})
            st.markdown(f"**Total Income:** ₹{cash.get('total_income', 'N/A')}")
            st.markdown(f"**Total Expenses:** ₹{cash.get('total_expenses', 'N/A')}")
            st.markdown(f"**Net Savings:** ₹{cash.get('net_savings', 'N/A')}")
            st.markdown(f"**Net Cash Flow:** ₹{cash.get('net_cash_flow', 'N/A')}")
            st.markdown("---")
            beh = overview.get("spending_behavior_and_emotional_patterns", {})
            st.write("**Spending & Emotional Patterns:**")
            st.write(f"Impulsiveness Score: {beh.get('impulsiveness_score', 'N/A')}")
            st.write(f"Discipline Score: {beh.get('discipline_score', 'N/A')}")
            st.write(f"Emotional Triggers: {beh.get('emotional_triggers', 'N/A')}")
            st.write(f"Observed Patterns: {beh.get('observed_spending_patterns', 'N/A')}")
            goal = overview.get("goal_progress", {})
            st.write(f"**Goal:** {goal.get('goal', 'N/A')}")
            st.write(f"Progress: {goal.get('progress_percent', 'N/A')}%")
            st.write(f"Projected Savings: ₹{goal.get('projected_savings', 'N/A')}")
            st.write(f"Time to Goal: {goal.get('time_to_goal', 'N/A')}")
            st.markdown("---")
            rec = obj.get("recommendations", {})
            st.success(f"**Coordinator Recommendation:** {rec.get('coordinator_recommendation', 'N/A')}")
            st.info(f"**Suggestions for Next Month:** {rec.get('suggestions_for_next_month', 'N/A')}")
        else:
            st.warning("Monthly summary not found. Please run the simulation first.")
    except Exception as e:
        st.error(f"Error reading monthly summary data: {e}")

# --- Coordinator Decision ---
def display_coordinator_decision(sim_no):
    try:
        path = f"output/coordinator_decision_simulation_{sim_no}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
            st.subheader("🧑‍💼 Coordinator's Final Decision")
            for obj in data:
                st.write(f"**Final Action:** {obj['final_action']}")
                st.write(f"**Rationale:** {obj['rationale']}")
                st.write(f"**Emotional Behavior:** {obj['emotional_behavior']}")
                st.write(f"**Spending Summary:** {obj['summary_of_spending']}")
                st.write(f"**Goals Summary:** {obj['summary_of_goals']}")
                st.write("**Recommendations:**")
                for rec in obj.get('List of recommendations', []):
                    st.markdown(f"- {rec}")
        else:
            st.warning("Coordinator decision not found. Please run the simulation first.")
    except Exception as e:
        st.error(f"Error reading coordinator decision data: {e}")

# --- Discipline Tracker ---
def display_discipline_tracker(sim_no):
    try:
        path = f"output/discipline_tracker_results_simulation_{sim_no}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
            st.subheader("🧭 Discipline & Character Profile")
            for obj in data:
                profile = obj.get("character_profile", {})
                st.write("**Character Traits:**")
                st.write(profile)
                st.write(f"**Updated At:** {obj.get('updated_at', 'N/A')}")
        else:
            st.warning("Discipline tracker data not found.")
    except Exception as e:
        st.error(f"Error reading discipline tracker data: {e}")

# --- Behavior Tracker ---
def display_behavior_tracker(sim_no):
    try:
        path = f"output/behavior_tracker_simulation_{sim_no}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
            st.subheader("🧠 Behavior Tracker")
            for obj in data:
                st.write(f"**User:** {obj['user_name']}, **Month:** {obj['month']}")
                st.write(f"Spending: ₹{obj['spending']}, Saving: ₹{obj['saving']}")
                st.write(f"Goal Achieved: {'✅' if obj['goal_achieved'] else '❌'}")
                st.write(f"Behavior Pattern: {obj['behavior_pattern']}")
                st.write("**Historical Log:**")
                st.table(pd.DataFrame(obj['historical_log']))
        else:
            st.warning("Behavior tracker data not found.")
    except Exception as e:
        st.error(f"Error reading behavior tracker data: {e}")

# --- Karma Tracker ---
def display_karma_tracker(sim_no):
    try:
        path = f"output/karmic_tracker_simulation_{sim_no}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
            st.subheader("🕉️ Karma Tracker")
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.write("**Recent Karmic Actions:**")
            for entry in data[-5:]:
                emoji = "🟢" if entry["karmic_score"] > 0 else "🟠" if entry["karmic_score"] == 0 else "🔴"
                st.markdown(f"{emoji} **{entry['date']}**: {entry['symbolic_reason']}")
        else:
            st.warning("Karma tracker data not found.")
    except Exception as e:
        st.error(f"Error reading karma tracker data: {e}")

# --- Mentor Advice ---
def display_mentor_advice(sim_no):
    try:
        path = f"output/mentor_advice_simulation_{sim_no}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
            st.subheader("🧘 Mentor's Guidance")
            for obj in data:
                st.markdown(f"**Message:** {obj['message']}")
                st.markdown(f"**Insight:** {obj['insight']}")
                st.markdown(f"**Suggestion:** {obj['suggestion']}")
                st.markdown(f"**Karmic Reflection:** {obj['karmic_reflection']}")
        else:
            st.warning("Mentor advice not found.")
    except Exception as e:
        st.error(f"Error reading mentor advice data: {e}")

# --- Financial Strategy ---
def display_financial_strategy(sim_no):
    try:
        path = f"output/financial_strategy_simulation_{sim_no}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
            st.subheader("📈 Financial Strategy")
            plan = data.get("financial_allocation_plan", {})
            st.write(f"**Debt Repayment:** {plan.get('debt_rep_payment_pct', 'N/A')}% (₹{plan.get('debt_rep_payment_amount', 'N/A')})")
            st.write(f"**Investment:** {plan.get('investment_pct', 'N/A')}% (₹{plan.get('investment_amount', 'N/A')})")
            st.write(f"**Emergency Fund:** {plan.get('emergency_fund_pct', 'N/A')}% (₹{plan.get('emergency_fund_amount', 'N/A')})")
        else:
            st.warning("Financial strategy not found.")
    except Exception as e:
        st.error(f"Error reading financial strategy data: {e}")

