from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from curriculumbuildercrew.tools.video_tool import VideoTool
from curriculumbuildercrew.tools.course_tool import OnlineCourseTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Curriculumbuilder():
    """Curriculumbuilder crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def input_ingestion_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['input_ingestion_agent'],
            verbose=True
        )

    @agent
    def curriculum_structuring_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['curriculum_structuring_agent'],
            verbose=True
        )

    @agent
    def scheduler_duration_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['scheduler_duration_agent'],
            verbose=True
        )

    @agent
    def resource_aggregation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['resource_aggregation_agent'],
            tools=[VideoTool(), OnlineCourseTool()],
            verbose=True
        )

    @agent
    def coordination_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['coordination_agent'],
            verbose=True
        )

    @agent
    def quality_assurance_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['quality_assurance_agent'],
            verbose=True
        )

    # To learn more about structured task outputs, 
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def input_ingestion_task(self) -> Task:
        return Task(
            config=self.tasks_config['input_ingestion_task'],
        )

    @task
    def curriculum_structuring_task(self) -> Task:
        return Task(
            config=self.tasks_config['curriculum_structuring_task'],
        )

    @task
    def scheduler_duration_task(self) -> Task:
        return Task(
            config=self.tasks_config['scheduler_duration_task'],
        )

    @task
    def resource_aggregation_task(self) -> Task:
        return Task(
            config=self.tasks_config['resource_aggregation_task'],
        )

    @task
    def coordination_task(self) -> Task:
        return Task(
            config=self.tasks_config['coordination_task'],
        )

    @task
    def quality_assurance_task(self) -> Task:
        return Task(
            config=self.tasks_config['quality_assurance_task'],
            output_file='curriculum.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Curriculumbuilder crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )