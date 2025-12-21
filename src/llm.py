# ============ IMPORTAÇÕES ============ #
import os
import json
from typing import Optional, List, Dict
from dotenv import load_dotenv

from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb

from agno.tools.tavily import TavilyTools

from time_exec import time_exec

# ============ CONSTANTES ============ #
_ = load_dotenv('.env')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
DB = SqliteDb(
    db_file="data/agents.db",
    session_table="agent_sessions"
)


# ============ Código ============ #
class LanguageLargeModel:
    def __init__(self):
        self.config = self._load_config("config_bot.json")
        
        self.agents = []
        self.team = None

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get("llm", {})

# ============ CRIAR AGENTES ============ #
    def create_agent(self, instructions: str = None,
                     tools: list = None,
                     role: str = None,
                     name: str = "agent") -> Agent:

        instructions = instructions
        role = role or f"Agente {name} para processamento de texto."

        agent = Agent(
            instructions=instructions,
            tools=tools,
            role=role,

            id=name,
            name=name,
        )
        self.agents.append(agent)
        return agent

# (02) team vs agents
# (03) model
# (04) instructions
# (05) tools
# ============ CRIAR TIMES ============ #
    def make_team(self):
        team_config = self.config.get("team", {})
        agents_config = team_config.get("agents", [])

        # Criar agentes
        for agent_data in agents_config:
            name = agent_data["name"]
            role = agent_data.get("role", f"Agente {name}")
            instructions = agent_data.get("instruction", self.config.get("system_message", ""))

            # Atribuir tools baseado no nome
            tools = []
            if "search" in name.lower():
                tools = [TavilyTools(api_key=TAVILY_API_KEY)]
            elif "local_executor" in name.lower():
                tools = []

            self.create_agent(
                name=name,
                role=role,
                instructions=instructions,
                tools=tools
            )

        # Criar o time diretamente
        name = team_config.get("name", "KaLLia Team")
        model_teams = team_config.get("model_teams", "openai/gpt-oss-120b")
        instructions = team_config.get("instruction_team", "Você é um time de agentes para processamento de texto.")
        role = team_config.get("role", f"Time {name} para processamento de texto.")
        
        if not self.agents:
            raise ValueError("Nenhum agente criado para o time")

        self.team = Team(
            model=Groq(
                api_key=GROQ_API_KEY,
                id=model_teams
            ),
            instructions=instructions,
            members=self.agents,
            role=role,
            name=name,

            db=DB,
            add_history_to_context=True,
            num_history_runs=5,
            enable_user_memories=True,
            add_memories_to_context=True,
            add_team_history_to_members=True, # quando True, cada agente tem acesso ao histórico do time
            num_team_history_runs=3
        )
        return self.team

 
# ============ GERAR RESPOSTA ============ #
    def generate_response(self, prompt: str, session_id: str = "main_session") -> str:
        if not prompt:
            raise ValueError("O prompt não pode estar vazio")
        # (07) acidentes
        
        
        if self.team:
            response = ''
            response_stream = self.team.run(prompt, stream=True)
            print("Bot:")
            for event in response_stream:
                event_type = event.event
                
                if event_type == "RunStarted":
                    print('Execução iniciada...')
                    print("-"*50)
                elif event_type == "RunContent":
                    content = event.content
                    if content:
                        response += content
                        print(content, end='', flush=True)
                elif event_type == "TeamRunContent":
                    content = event.content
                    if content:
                        response += content
                        
                        print(content, end='', flush=True)
                elif event_type == "ToolCallStarted":
                    tool = event.tool
                    tool_name = tool.tool_name
                    tool_args = tool.tool_args
                    print(f'TOOL INICIADA: {tool_name}')
                    print(f'ARGUMENTOS: {tool_args}')
                    
                elif event_type == "ToolCallCompleted":
                    tool_name = event.tool.tool_name
                    print(f'TOOL FINALIZADA: {tool_name}')
                    print("-"*50)
                    
                elif event_type == "RunCompleted":
                    print('\nExecução finalizada.')
                    print("-"*50)
                    metrics = event.metrics
                    if metrics:
                        print(f"METRICAS: {json.dumps(metrics, indent=2)}")
                
                else:
                    print(f'Evento desconhecido: {event_type}')
        else:
            raise ValueError("Nenhum agente ou time configurado")
        
        return response



# ============= Execução ============== #
if __name__ == "__main__":
    llm = LanguageLargeModel()
    llm.make_team()
    prompt = "oi tudo bem?"
    response = llm.generate_response(prompt)
