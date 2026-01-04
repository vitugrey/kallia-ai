# ============ Importação ============ #
import os
import json
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.db.sqlite import SqliteDb
from agno.tools.tavily import TavilyTools

from tools import knowledge, open_program


# ============ Constantes ============ #
_ = load_dotenv('.env')
OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
DB = SqliteDb(
    db_file="data/agents.db",
    session_table="kallia_sessions",
    memory_table="kallia_memories",
    knowledge_table="kallia_knowledge"
)


# ============ Código ============ #
class LanguageLargeModel:
    def __init__(self):
        self.config = self._load_config("config_bot.json")

        self.tools = [
            TavilyTools(api_key=TAVILY_API_KEY),
            open_program
        ]
        self.agent = None

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get("llm", {})

    def create_agent(self) -> Agent:
        model_ollama = self.config.get("model_ollama", "ministral-3:3b")

        if model_ollama:
            model = Ollama(
                id=model_ollama,
                api_key=OLLAMA_API_KEY
            )
        else:
            raise ValueError(f"Modelo ollama desconhecido: {model_ollama}")

        agent = Agent(
            id=self.config.get("agent_id"),
            name=self.config.get("name"),
            description=self.config.get("description"),

            model=model,
            instructions=str(self.config.get("instruction")),
            tools=self.tools or [],
            knowledge=knowledge,
            search_knowledge=True,

            db=DB,
            add_history_to_context=True,
            num_history_runs=5,
            enable_user_memories=True,
            add_memories_to_context=True,
            add_datetime_to_context=True,
            add_name_to_context=True,
        )

        self.agent = agent
        return agent

    def generate_response(self, prompt: str) -> str:
        if not prompt:
            return

        if not self.agent:
            self.create_agent()

        response = self.agent.run(
            input=prompt,
            session_id=self.config.get("session_id", "main_session"),
            user_id=self.config.get("user_id", "main_user")
        )
        if response.tools:
            for tool in response.tools:
                print(f"Ferramenta Usada: {tool.tool_name}")
                print(f"Query: {tool.tool_args.get('query')}")

        return response.content


# ============= Execução ============== #
if __name__ == "__main__":
    llm = LanguageLargeModel()
    prompt = "reabra o programa projeto"
    response = llm.generate_response(prompt=prompt)
    print(f"Resposta: {response}")
