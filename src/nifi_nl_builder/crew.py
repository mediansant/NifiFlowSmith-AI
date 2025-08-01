import os
import yaml
from dotenv import load_dotenv
from crewai import Crew, Agent, Task, LLM

# Load environment variables
load_dotenv()
from .tools.crewai_tools import (
    CreateProcessGroupTool, AddProcessorTool, ConnectProcessorsTool,
    StartProcessorTool, StopProcessorTool, ListProcessorsTool,
    GetFlowStatusTool, ExportFlowTool
)

class NiFiNLCrew:
    def __init__(self, config_dir=None):
        if config_dir is None:
            # Get the directory where this file is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.config_dir = os.path.join(current_dir, "config")
        else:
            self.config_dir = config_dir
        self.agents = self._load_agents()
        self.tasks = self._load_tasks()
        
        # Configure LLMs for different agents
        self.llms = {
            "nl_parser": LLM(model="gpt-4o", max_tokens=2000, temperature=0.1),
            "flow_planner": LLM(model="gpt-4o", max_tokens=1500, temperature=0.1),
            "flow_builder": LLM(model="gpt-4o-mini", max_tokens=3000, temperature=0.2),
            "cdf_deployer": LLM(model="gpt-4o", max_tokens=1000, temperature=0.1)
        }
        
    def _load_agents(self):
        """Load agent configurations from YAML"""
        try:
            with open(f"{self.config_dir}/agents.yaml", 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Agents configuration file not found at {self.config_dir}/agents.yaml")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing agents.yaml: {e}")
    
    def _load_tasks(self):
        """Load task configurations from YAML"""
        try:
            with open(f"{self.config_dir}/tasks.yaml", 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Tasks configuration file not found at {self.config_dir}/tasks.yaml")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing tasks.yaml: {e}")
    
    def _create_agent(self, agent_id, config):
        """Create a CrewAI agent from configuration"""
        tools = []
        
        # Attach NiFi tools specifically to flow_builder agent
        if agent_id == "flow_builder":
            tools = [
                CreateProcessGroupTool(),
                AddProcessorTool(),
                ConnectProcessorsTool(),
                StartProcessorTool(),
                StopProcessorTool(),
                ListProcessorsTool(),
                GetFlowStatusTool(),
                ExportFlowTool()
            ]
        
        # Use configured LLM for the agent
        llm = self.llms.get(agent_id, LLM(model="gpt-4o"))
        
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm=llm,
            tools=tools,
            verbose=True,
            allow_delegation=False
        )
    
    def _create_task(self, task_id, config, agents):
        """Create a CrewAI task from configuration"""
        agent = agents[config["agent"]]
        
        return Task(
            description=config["description"],
            expected_output=config["expected_output"],
            agent=agent
        )
    
    def build_crew(self):
        """Build the complete crew with agents and tasks"""
        # Create agents
        agents = {}
        for agent_id, config in self.agents.items():
            agents[agent_id] = self._create_agent(agent_id, config)
        
        # Create tasks
        tasks = []
        for task_id, config in self.tasks.items():
            task = self._create_task(task_id, config, agents)
            tasks.append(task)
        
        # Create crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=True,
            memory=True
        )
        
        return crew
    
    def run(self, description):
        """Run the crew with a natural language description"""
        crew = self.build_crew()
        
        # Set the description context for all tasks
        for task in crew.tasks:
            task.context = f"Description: {description}"
        
        result = crew.kickoff()
        return result

def main():
    """Main function to run the NiFi NL Builder crew"""
    crew_manager = NiFiNLCrew()
    
    # Example usage
    description = "Create a flow that reads from Kafka topic 'input-data', filters records with status 'active', and writes to HDFS path '/data/processed'"
    
    print("Starting NiFi NL Builder Crew...")
    print(f"Processing description: {description}")
    
    result = crew_manager.run(description)
    
    print("\n=== Crew Execution Result ===")
    print(result)
    
    return result

if __name__ == "__main__":
    main() 