from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain.tools import tool
import csv
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel
from crewai_tools import FileReadTool
from crewai_tools import FileWriterTool

class Save_to_csv_ToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    data: list
    filename: str = "backlog.csv"


class Save_to_csv_Tool(BaseTool):
    name: str = "save_to_csv"
    description: str = (
        "Save a list of dictionaries to a CSV file"
    )
    args_schema: Type[BaseModel] = Save_to_csv_ToolInput

    def _run(self, data,filename) -> str:
        # Implementation goes here
        if not data:
            return "No data to save."
        keys = data[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        return f"CSV saved as {filename}"
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class UxAgileComb():
    """UxAgileComb crew"""
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # @tool("save_to_csv")
    # def save_to_csv (data: list, filename: str = "backlog.csv"):
    #     """Save a list of dictionaries to a CSV file"""
    #     if not data:
    #         return "No data to save."
    #     keys = data[0].keys()
    #     with open(filename, "w", newline="", encoding="utf-8") as f:
    #         writer = csv.DictWriter(f, fieldnames=keys)
    #         writer.writeheader()
    #         writer.writerows(data)
    #     return f"CSV saved as {filename}"
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
   

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    
    @agent
    def requirements(self) -> Agent:
        file_read_tool = FileReadTool(file_path='Docs\Vision.txt')
        file_tool = FileWriterTool()
        return Agent(
            config=self.agents_config['requirements'],
            tools=[file_read_tool,file_tool],
            verbose=True,
        )
    
    @agent
    def Jira_research(self) -> Agent:
        return Agent(
            config=self.agents_config['Jira_research'],
            verbose=True,
            tools=[Save_to_csv_Tool()],
            allow_delegation=False
        )

    @agent
    def Epics(self) -> Agent:
        file_read_tool = FileReadTool(file_path='Docs\backlog.csv')
        return Agent(
            config=self.agents_config['Epics'],
            tools=[file_read_tool,Save_to_csv_Tool()],
            verbose=True
        )
    
    @agent
    def User_Stories(self) -> Agent:
        file_read_tool = FileReadTool(file_path='Docs\backlog.csv')
        return Agent(
            config=self.agents_config['User_Stories'],
            tools=[file_read_tool,Save_to_csv_Tool()],
            verbose=True
        )
    @agent
    def Tasks(self) -> Agent:
        file_read_tool = FileReadTool(file_path='Docs\backlog.csv')
        return Agent(
            config=self.agents_config['Tasks'],
            tools=[file_read_tool,Save_to_csv_Tool()],
            verbose=True
        )
   
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def requirements_task(self) -> Task:
        return Task(
            config=self.tasks_config['requirements_task'],
            output_file='Docs/requirements.txt',
            human_input=True
        )
    
    @task
    def Jira_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['Jira_research_task'],
            output_file='Docs/backlog.csv'
        )

    @task
    def Epics_task(self) -> Task:
        return Task(
            config=self.tasks_config['Epics_task'],
            output_file='Docs/backlog.csv'
        )
    
    @task
    def User_Stories_task(self) -> Task:
        return Task(
            config=self.tasks_config['User_Stories_task'],
            output_file='Docs/backlog.csv'
        )
    
    @task
    def Tasks_task(self) -> Task:
        return Task(
            config=self.tasks_config['Tasks_task'],
            output_file='Docs/backlog.csv'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the UxAgileComb crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
