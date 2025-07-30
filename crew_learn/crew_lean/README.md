# Lean Crew
Sample project to lean how to use crewAI works with Preplexity. 
This `crew_lean` is a base project that demonstrate the use of multi-agents to acheive specific goal. Each agent has unique roles, goals, and tools. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew(**agents are stitched with preplexity models**). The agents collaborate on a couple of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to generate research summary on any given topic(_main.py_)

## Installation

```bash
Step 1: pip install uv
Step 2: crewai install
Step 3: git clone https://github.com/Gulslabs/learn-gen-ai.git
Step 4: cd crew_learn/crew_lean
Step 5: crewai run # This will run the crew_lean crew
```
**IMP:** This command initializes the crew_lean Crew, assembling the agents and assigning them tasks as defined in your configuration. `report.md` file will be generated with the output of a research on LLMs in the root folder.

## Customization
- Modify `src/crew_lean/config/agents.yaml` to define your agents
- Modify `src/crew_lean/config/tasks.yaml` to define your tasks
- Modify `src/crew_lean/crew.py` to add your own logic, tools and specific args
- Modify `src/crew_lean/main.py` to add custom inputs for your agents and tasks

## Reference - How to setup perplexity locally
-  With a Perplexity Pro subscription(_available for free for airtel users in India_), you can interact programmatically with Perplexity's models using their official API in your Python projects.
    - Log into Perplexity[https://www.perplexity.ai/account/api/keys]
    - Goto `Settings → API` geneate and copy the API key. 
    - Set variable  `PERPLEXITY_API_KEY` with value of the copied api key into the `.env` file Or set it as a environment variable. 

## What are tooling and how they work 
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
