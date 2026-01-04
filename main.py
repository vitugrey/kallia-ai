from agno.agent import Agent
from agno.models.ollama import Ollama

agent = Agent(
    model=Ollama(id="ministral-3:3b", host="http://localhost:11434/"),
    markdown=True
)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story.")