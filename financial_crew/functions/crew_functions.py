from functions.economic_context import EconomicEnvironment
from functions.monthly_simulation import simulate_month
import os
import json
from litellm import RateLimitError
from crew import FinancialCrew
import time
from crewai import Crew
import traceback
import streamlit as st

# *******************************************Functions to sequentially and hierarchically run my crew workflow************************

def kickoff_sequential(self, inputs, sleep_between_calls=15):
    print("🚀 Starting Sequential Crew Execution...")
    results = []

    for task in self.tasks:
        print(f"\n🟢 Executing task: {task.name} for agent: {task.agent.role}")
        # 🔎 Debugging: Check if the tool(s) is working
        if hasattr(task, 'tool') and task.tool:
            try:
                # You can define a `check_status()` or `ping()` method in your Tool classes
                tool_status = task.tool.check_status()  # Simulated check
                if tool_status:
                    print(f"🛠️ Tool '{task.tool.name}' is working properly ✅")
                else:
                    print(f"⚠️ Tool '{task.tool.name}' is NOT responding ❌")
            except Exception as e:
                print(f"❗ Error checking tool '{task.tool.name}': {e}")
        else:
            print(f"ℹ️ No tool assigned to task '{task.name}'")

        # Execute task via its agent
        task_result = task.agent.execute_task(task, inputs)

        print(f"✅ Finished task: {task.name}\nResult: {task_result}")

        results.append({
            "task_name": task.name,
            "result": task_result
        })

        if hasattr(task, 'output_file') and task.output_file:
            month_number = inputs.get('Month', 1)  # Default to 1 if not provided
            output_dir = os.path.dirname(task.output_file)
            os.makedirs(output_dir, exist_ok=True)

            # Get the base file name and insert `_simulation_{month}` before `.json`
            base_file_name = os.path.basename(task.output_file)
            file_name_without_ext, ext = os.path.splitext(base_file_name)
            dynamic_file_name = f"{file_name_without_ext}_simulation_{month_number}{ext}"
            output_path = os.path.join(output_dir, dynamic_file_name)

            try:
                # Check if the task result is a string and needs to be parsed
                if isinstance(task_result, str):
                    parsed_result = json.loads(task_result)  # Parse the string as JSON
                else:
                    parsed_result = task_result  # If already in a dictionary or list format, use as is

            except json.JSONDecodeError:
                print("❗ Task result is not valid JSON. Writing as plain text.")
                parsed_result = task_result  # Fallback to original task result (if not valid JSON)

            # Write the result to a JSON file
            with open(output_path, "w", encoding="utf-8") as f:
                # If parsed_result is not a string, write as JSON
                json.dump(parsed_result, f, indent=4, ensure_ascii=False)

            print(f"💾 Output written to {output_path}")
        # Sleep between calls to smooth out token rate usage
        time.sleep(sleep_between_calls)

    print("🎉 All tasks completed sequentially!")
    return parsed_result

def kickoff_hierarchical(self, inputs):
        # Recursive hierarchical task execution logic
        print("🚀 Starting Hierarchical Crew Execution...")
        results = []

        def execute_task_hierarchy(tasks):
            """Recursively execute tasks in a hierarchical manner."""
            for task in tasks:
                print(f"\n🟢 Executing task: {task.name} for agent: {task.agent.role}")
                task_result = task.agent.execute_task(task, inputs)
                print(f"✅ Finished task: {task.name}\nResult: {task_result}")
                results.append({
                    "task_name": task.name,
                    "result": task_result
                })
                if hasattr(task, 'sub_tasks') and task.sub_tasks:
                    print(f"🔄 Recursively executing sub-tasks of '{task.name}'...")
                    execute_task_hierarchy(task.sub_tasks)
                time.sleep(5)  # Add sleep time if needed

        # Start execution from the root tasks
        execute_task_hierarchy(self.tasks)
        return results

# Patch the method into your Crew instance
Crew.kickoff_sequential = kickoff_sequential

# *****************************************************Simulation for my Crew workflow****************************************************

def run_simulation_with_retries(inputs, custom_agents=None, custom_tasks=None, max_attempts=3):
    hashable_inputs = json.dumps(inputs, sort_keys=True)
    customized_agents = custom_agents
    customized_tasks = custom_tasks
    for attempt in range(max_attempts):
        try:
            result = FinancialCrew().flexible_crew(
                input_data=hashable_inputs,
                agent_overrides=customized_agents,
                task_overrides=customized_tasks
            ).kickoff_sequential(inputs=inputs)
            return result
        except RateLimitError:
            st.warning(f"Rate limit hit. Retrying in 10 seconds... (Attempt {attempt + 1}/{max_attempts})")
            time.sleep(10)
        except Exception as e:
            print("Full Traceback:")
            traceback.print_exc()
            st.error(f"An unexpected error occurred: {e}")
            break
    return None


def simulate_timeline(n_months, simulation_unit, user_inputs):
    previous_result = None
    for month in range(1, n_months+1):
        eco_env = EconomicEnvironment(unit=simulation_unit)
        eco_env.simulate_step()
        context = eco_env.get_context()
        economic_context = context
        user_name = user_inputs['user_name']
        user_inputs["previous_summary"] = previous_result or "No previous data"
        user_inputs['inflation'] = economic_context['inflation_rate']
        user_inputs['interest_rate'] = economic_context['interest_rate']
        user_inputs['cost_of_living_index'] = economic_context['cost_of_living_index']
        user_inputs['Month'] = month 
        if previous_result:
            # ✅ Extract last known net savings
            print("Previous result content:", type(previous_result))
            last_summary = previous_result[-1]['overview']['cash_flow_summary']
            last_balance = last_summary['net_savings']

            # ✅ Extract past emotional patterns
            last_emotion = previous_result[-1]['overview']['spending_behavior_and_emotional_patterns']
            impulsiveness = last_emotion['impulsiveness_score']
            discipline = last_emotion['discipline_score']

            # ✅ Extract goal progress
            last_goal = previous_result[-1]['overview']['goal_progress']
            progress_percent = last_goal['progress_percent']
            projected_savings = last_goal['projected_savings']

            user_inputs['cashflow_context'] = (
                f"Previous summary exists. Continue cash flow simulation using last net savings ₹{last_balance}. "
                f"Maintain emotional pattern: impulsiveness_score {impulsiveness}, discipline_score {discipline}. "
                f"Goal progress is {progress_percent}% with projected savings ₹{projected_savings}. "
                f"Ensure the new month is {month + 1}."
            )
            user_inputs['starting_balance'] = last_balance  # 🟢 Carry forward balance
        else:
            user_inputs['cashflow_context'] = "No previous summary exists. Start fresh as a new simulation."

        print(f"Simulating Month {month}")
        previous_result = run_simulation_with_retries(inputs=user_inputs)
        simulate_month(user_name, month_index= month)
        
    return True