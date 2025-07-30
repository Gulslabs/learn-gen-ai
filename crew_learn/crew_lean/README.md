# Lean Crew
Sample project to lean how to use crewAI works with Preplexity

## Understanding Your Crew

The `crew_lean` is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Installation

```bash
Step 1: pip install uv
Step 2: crewai install
```


### Customizing

**Add your `PERPLEXITY_API_KEY` into the `.env` file**

- Modify `src/crew_lean/config/agents.yaml` to define your agents
- Modify `src/crew_lean/config/tasks.yaml` to define your tasks
- Modify `src/crew_lean/crew.py` to add your own logic, tools and specific args
- Modify `src/crew_lean/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the crew_lean Crew, assembling the agents and assigning them tasks as defined in your configuration. `report.md` file will be generated with the output of a research on LLMs in the root folder.


This example, unmodified, will run the create a

## Bonus - What are tooling and how they work 
- CrewAI custom tools are essentially functions that extend what your AI agents can do beyond just generating text. Think of them as specialized abilities you give to your agents - like giving a human assistant access to a calculator, database, or API. Tools are assigned to agents through the tools parameter, and agents automatically decide when and how to use them based on the task requirements.
- There are two main ways to create custom tools in CrewAI:
    - Using the @tool decorator (simpler, more common)
    - Subclassing BaseTool (more advanced, object-oriented)
- Example of a tool:
```
@tool("Weather Checker")
def get_weather(city: str) -> str:
    """
    Gets current weather for a city using a weather API.
    
    :param city: Name of the city
    :return: Weather information as a string
    """
    # This is a mock example - replace with real API
    # api_key = "your_api_key"
    # url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    # For demo purposes, returning mock data
    return f"Weather in {city}: 22°C, Sunny with light clouds"
```
- How to reference tool in agent:
```python
agent = Agent(
    name="Researcher",
    goal="Conduct research on {topic}",
    backstory="You are a research assistant.",
    tools=[get_weather],
    model="gpt-3.5-turbo",
    max_iterations=3,
    verbose=True,
)
```