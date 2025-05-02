import streamlit as st
from functions.streamlit_functions import *
import agentops
from functions.crew_functions import *

agentops.init(
    api_key='0c4bf935-54bd-42f0-8c82-9a044f1afe10',
    default_tags=['crewai']
)

# ************************************************Streamlit configuration************************************************************

st.set_page_config(
    page_title="🧠 Financial Agent Simulator", 
    layout="centered",
    initial_sidebar_state="expanded"
)
st.title("📈 Financial Agent Simulation")

st.markdown("""
Welcome to your **Personal Financial Simulation**. Simulate months of financial life, get guidance, 
and improve your money habits with AI agents!
""")

# Sidebar for navigation
with st.sidebar:
    st.header("Simulation Navigation")
    display_option = st.radio(
        "View Results",
        options = [
            "📋 Monthly Summary",
            "💰 Cash Flow",
            "💡 Spending Review",
            "🎯 Goal Tracking",
            "📊 Coordinator Decision",
            "✅ Discipline Tracker",
            "🧠 Behavior Tracker",
            "🌱 Karma Tracker",
            "🧑‍🏫 Mentor Advice",
            "📈 Financial Strategy"
        ],
        index=0
    )
    st.markdown("---")
    st.caption("ℹ️ Run a new simulation to update all reports")

# *************************************************Collecting user profile details*****************************************************
with st.form("user_profile_form"):
    st.subheader("👤 Basic User Profile")

    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("Name")
        age = st.slider("Age", min_value=18, max_value=70)
        occupation = st.selectbox("Occupation", ["Student", "Salaried", "Freelancer", "Business Owner", "Unemployed"])
    with col2:
        income_level = st.selectbox("Monthly Income Level (₹)", ["<10,000", "10,000–30,000", "30,000–70,000", "70,000+"])
        opening_balance = st.number_input("Starting Bank Balance (₹)", min_value=0)

        simulation_unit = st.radio("Choose simulation unit:", ["Months", "Days"], horizontal=True)
        if simulation_unit == "Months":
            simulation_steps = st.slider("Simulate how many Months?", min_value=1, max_value=12, value=3)
        else:
            simulation_steps = st.slider("Simulate how many days?", min_value=1, max_value=31, value=3)

    st.markdown("---")
    st.subheader("💰 Income Sources")

    inc_col1, inc_col2 = st.columns(2)
    with inc_col1:
        num_income_sources = st.number_input("Number of income sources", min_value=1, max_value=10, value=1)

    income_sources = {}
    total_amount_earning = 0
    for i in range(num_income_sources):
        with st.expander(f"Income Source {i+1}"):
            col1, col2 = st.columns(2)
            with col1:
                source = st.text_input(f"Source {i+1} Name", key=f"inc_name_{i}")
            with col2:
                amount = st.number_input(f"Amount Per Month(₹)", min_value=0.0, format="%.2f", key=f"inc_amt_{i}")
            if source and amount > 0:
                income_sources[source] = amount
                total_amount_earning += amount

    st.markdown("---")
    st.subheader("💸 Monthly Expense Categories")

    exp_col1, exp_col2 = st.columns(2)
    default_expenses = ["Rent", "Food", "Entertainment"]
    expenses = {}
    total_expenses = 0
    for i, category in enumerate(default_expenses):
        with (exp_col1 if i % 2 == 0 else exp_col2):
            expenses[category] = st.number_input(f"{category} (₹)", min_value=0.0, format="%.2f", key=f"exp_{category}")
            total_expenses += expenses[category]

    st.subheader("➕ Custom Expense Categories")
    custom_col1, custom_col2 = st.columns(2)
    with custom_col1:
        num_custom = st.number_input("How many?", min_value=0, max_value=5, value=0)

    for i in range(num_custom):
        with st.expander(f"Custom Expense {i+1}"):
            col1, col2 = st.columns(2)
            with col1:
                custom_name = st.text_input(f"Name", key=f"custom_exp_name_{i}")
            with col2:
                custom_amount = st.number_input(f"Amount (₹)", min_value=0.0, format="%.2f", key=f"custom_exp_amt_{i}")
            if custom_name:
                expenses[custom_name] = custom_amount
                total_expenses += expenses[custom_name]

    st.markdown("---")
    st.subheader("💰 Savings Goals")

    savings_target = st.number_input("Monthly Savings Target (₹)", min_value=0, value=5000)
    percentage_of_my_savings = st.slider("Savings Percentage of Income (%)", min_value=0, max_value=100, value=33)
    financial_goal = st.text_input("What's your financial goal? (e.g., 'Save ₹50,000 for emergency fund')")

    st.markdown("---")
    submit = st.form_submit_button("💡 Run Financial Simulation")

# ***************************************************Running my Crew workflow**********************************************************
if submit:
    with st.spinner("🔍 Simulating your financial journey..."):
        user_inputs = {
            'user_name': user_name,
            'age': age,
            'occupation': occupation,
            'income_level': income_level,
            'goal': financial_goal,
            'starting_balance': opening_balance,
            'simulation_unit': simulation_unit,
            'simulation_steps': simulation_steps,
            'monthly_earning': total_amount_earning,
            'savings_target': savings_target,
            'percentage_of_my_savings': percentage_of_my_savings,
            'monthly_expenses': total_expenses,
        }
        custom_agents = {
            'spending_advisor': {'goal': 'Save more money this month'},
            'goal_tracker': {'goal': 'Increase savings target by 20%'}
        }
        custom_tasks = {
            'simulate_cash_flow': {'expected_output': 'Custom output for this run'}
        }
        result = simulate_timeline(simulation_steps, simulation_unit ,user_inputs)

        if result:
            st.success("✅ Simulation Complete!")
            st.balloons()
        else:
            st.error("Simulation failed after multiple attempts.")

# **********************************************Display the selected content based on navigation********************************************
sim_number = st.sidebar.selectbox(
    "Choose Simulation", 
    list(range(1, simulation_steps + 1))
)

if display_option == "📋 Monthly Summary":
    display_monthly_summary(sim_number)
elif display_option == "💰 Cash Flow":
    display_cash_flow(sim_number)
elif display_option == "💡 Spending Review":
    display_spending_review(sim_number)
elif display_option == "🎯 Goal Tracking":
    display_goal_tracking(sim_number)
elif display_option == "📊 Coordinator Decision":
    display_coordinator_decision(sim_number)
elif display_option == "✅ Discipline Tracker":
    display_discipline_tracker(sim_number)
elif display_option == "🧠 Behavior Tracker":
    display_behavior_tracker(sim_number)
elif display_option == "🌱 Karma Tracker":
    display_karma_tracker(sim_number)
elif display_option == "🧑‍🏫 Mentor Advice":
    display_mentor_advice(sim_number)
elif display_option == "📈 Financial Strategy":
    display_financial_strategy(sim_number)

st.markdown("---")
st.caption("""
ℹ️ This is a simulation tool. Actual financial results may vary based on real-world circumstances.
Use the insights to inform your decisions, but consult a financial advisor for personalized advice.
""")