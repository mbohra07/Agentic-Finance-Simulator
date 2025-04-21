# src/financial_crew/crew.py
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
#from tools.utils import financial_simulation_tool 
from dotenv import load_dotenv
"""from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
import os"""

"""# Use environment variable with fallback
storage_path = os.getenv("CREWAI_STORAGE_DIR", "./my_crew_storage")

# Ensure the storage directory exists
os.makedirs(storage_path, exist_ok=True)"""

load_dotenv()

groq_llm = LLM(model="groq/llama-3.1-70b-versatile")

@CrewBase
class FinancialCrew():

    @agent
    def spending_advisor(self) -> Agent:
        return Agent(config=self.agents_config['spending_advisor'], verbose=True)

    @agent
    def goal_tracker(self) -> Agent:
        return Agent(config=self.agents_config['goal_tracker'], verbose=True)

    @agent
    def emotional_bias_agent(self) -> Agent:
        return Agent(config=self.agents_config['emotional_bias_agent'], verbose=True)

    @agent
    def mentor_agent(self) -> Agent:
        return Agent(config=self.agents_config['mentor_agent'], verbose=True)

    @task
    def simulate_cash_flow(self) -> Task:
        return Task(config=self.tasks_config['simulate_cash_flow'])

    @task
    def evaluate_spending(self) -> Task:
        return Task(config=self.tasks_config['evaluate_spending'])

    @task
    def track_goals(self) -> Task:
        return Task(config=self.tasks_config['track_goals'])

    @task
    def monthly_summary(self) -> Task:
        return Task(config=self.tasks_config['monthly_summary'], output_file='output/report.md')
    
    @crew
    def crew(self, input_data=None) -> Crew:

        simulate_task = self.simulate_cash_flow()
        evaluate_task = self.evaluate_spending()
        goal_task = self.track_goals()
        summary_task = self.monthly_summary()

        evaluate_task.context = [simulate_task]
        goal_task.context = [simulate_task, evaluate_task]
        summary_task.context = [simulate_task, evaluate_task, goal_task]

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            input_data= input_data,
            process=Process.sequential,
            verbose=True,
            memory=False,
    )

"""long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path=os.path.join(storage_path, "long_term_memory_storage.db")
                )
            ),
    
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                    embedder_config={
                            "provider": "cohere",
                            "config": {
                                "model": 'embed-english-v3.0'
                            }
                    },
                    type="short_term",
                    path=storage_path
                )
            ),
        
            entity_memory = EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "cohere",
                        "config": {
                            "model": 'embed-english-v3.0'
                        }
                    },
                    type="short_term",
                    path=storage_path
                )
            ),"""