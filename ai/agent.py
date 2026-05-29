import os
import yaml
from crewai import Agent, Task, Crew, Process, LLM
from ai.tools.api_tools import get_fleet_telemetry, get_port_metrics

def run_agent(ship_id: str) -> str:
    local_llm = LLM(
        model="ollama/llama3.1:8b",
        base_url="http://localhost:11434"
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))
    agents_config_path = os.path.join(base_dir, "config", "agents.yaml")
    tasks_config_path = os.path.join(base_dir, "config", "tasks.yaml")

    with open(agents_config_path, "r") as f:
        agents_config = yaml.safe_load(f)

    with open(tasks_config_path, "r") as f:
        tasks_config = yaml.safe_load(f)

    monitoring_agent = Agent(
        role=agents_config["monitoring_agent"]["role"],
        goal=agents_config["monitoring_agent"]["goal"],
        backstory=agents_config["monitoring_agent"]["backstory"],
        tools=[get_fleet_telemetry],
        llm=local_llm,
        verbose=True
    )

    routing_agent = Agent(
        role=agents_config["routing_agent"]["role"],
        goal=agents_config["routing_agent"]["goal"],
        backstory=agents_config["routing_agent"]["backstory"],
        llm=local_llm,
        verbose=True
    )

    logistics_agent = Agent(
        role=agents_config["logistics_agent"]["role"],
        goal=agents_config["logistics_agent"]["goal"],
        backstory=agents_config["logistics_agent"]["backstory"],
        tools=[get_port_metrics],
        llm=local_llm,
        verbose=True
    )

    monitoring_task = Task(
        description=tasks_config["monitoring_task"]["description"],
        expected_output=tasks_config["monitoring_task"]["expected_output"],
        agent=monitoring_agent
    )

    routing_task = Task(
        description=tasks_config["routing_task"]["description"],
        expected_output=tasks_config["routing_task"]["expected_output"],
        agent=routing_agent
    )

    logistics_task = Task(
        description=tasks_config["logistics_task"]["description"],
        expected_output=tasks_config["logistics_task"]["expected_output"],
        agent=logistics_agent
    )

    crew = Crew(
        agents=[monitoring_agent, routing_agent, logistics_agent],
        tasks=[monitoring_task, routing_task, logistics_task],
        process=Process.sequential
    )

    result = crew.kickoff(inputs={"ship_id": ship_id})
    return str(result)
