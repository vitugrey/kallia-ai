# ============ Importação ============ #
import os
import json
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from agno.tools.tavily import TavilyTools

from tools import knowledge


# ============ Constantes ============ #
_ = load_dotenv('.env')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
DB = SqliteDb(
    db_file="data/agents.db",
    session_table="kallia_sessions",
    memory_table="kallia_memories"
)


# ============ Código ============ #
class LanguageLargeModel:
    def __init__(self):
        self.config = self._load_config("config_bot.json")

        self.tools = [TavilyTools(api_key=TAVILY_API_KEY)]
        self.agent = None

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get("llm", {})

    def create_agent(self,
                     model: str = "groq",
                     instructions: str = None,
                     tools: list = None,
                     description: str = None,
                     name: str = "agent") -> Agent:

        if model.lower() == "groq":
            model = Groq(
                api_key=GROQ_API_KEY,
                id=self.config.get("model_groq", "openai/gpt-oss-120b"))
        elif model.lower() == "gemini":
            model = Gemini(
                api_key=GOOGLE_API_KEY,
                id=self.config.get("model_gemini", "gemini-3-flash-preview"))
        else:
            raise ValueError(f"Modelo desconhecido: {model}")

        agent = Agent(
            model=model,
            instructions=instructions,
            tools=tools or [],

            knowledge=knowledge,
            search_knowledge=True,

            db=DB,
            add_history_to_context=True,
            num_history_runs=5,
            enable_user_memories=True,
            add_memories_to_context=True,
            add_datetime_to_context=True,
            add_name_to_context=True,

            id=name,
            name=name,
            description=description,
        )

        self.agent = agent
        return agent

    def generate_response(self, prompt: str, llm_provider: str = "gemini") -> str:
        if not prompt:
            return

        if not self.agent:
            self.create_agent(
                model=llm_provider,
                instructions=str(self.config.get("instruction")),
                name=self.config.get("name"),
                description=self.config.get("description"),
                tools=self.tools
            )

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
    prompt = "oi tudo bem?"
    response = llm.generate_response(prompt)
    print(f"Resposta: {response}")
