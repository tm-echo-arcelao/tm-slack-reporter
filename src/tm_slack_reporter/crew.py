from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from src.tm_slack_reporter.tools.slack_tool import SlackToolSet
from src.tm_slack_reporter.utils.env import config

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


llm = LLM(
    model=config.get("CREWAI_OPENROUTER_MODEL_ID"),
    base_url=config.get("CREWAI_OPENROUTER_BASE_URL"),
    api_key=config.get("CREWAI_OPENROUTER_API_KEY"),
)


@CrewBase
class TmSlackReporter:
    """TmSlackReporter crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def slack_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config["slack_summarizer"],  # type: ignore[index]
            verbose=True,
            tools=SlackToolSet().get_tools(),
            llm=llm,
        )

    @agent
    def action_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config["action_reporter"],  # type: ignore[index]
            verbose=True,
            llm=llm,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def gather_context_task(self) -> Task:
        return Task(
            config=self.tasks_config["gather_context_task"],  # type: ignore[index]
        )

    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config["report_task"],  # type: ignore[index]
            output_file="report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TmSlackReporter crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
            embedder={
                "provider": "ollama",
                "config": {"model": config.get("CREWAI_OLLAMA_EMBEDDER_MODEL_ID")},
            },
            max_rpm=5,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
