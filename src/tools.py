# ============ Importação ============ #
import os
from dotenv import load_dotenv
from typing import Optional, Sequence

from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.db.sqlite import SqliteDb
from agno.agent import Agent
from agno.media import Image
from agno.tools.function import ToolResult

import pyautogui
from io import BytesIO

# ============ Constantes ============ #
_ = load_dotenv('.env')
os.makedirs("data/lancedb", exist_ok=True)
DB = SqliteDb(
    db_file="data/agents.db",
    knowledge_table="kallia_knowledge"
)
VECTOR_DB = LanceDb(
    table_name="kallia_vector_db",
    uri="data/lancedb",
    embedder=OllamaEmbedder(id="nomic-embed-text", dimensions=768)
)


# ============ Knowledge (RAG) ============ #
knowledge = Knowledge(
    name="KaLLia Knowledge",
    description="Base de conhecimento local para RAG",
    contents_db=DB,
    vector_db=VECTOR_DB,
)


# ============ open_program ============ #
def open_program(query: str) -> str:
    """Abre um programa/arquivo procurando por atalhos (.lnk) no diretório ~/Links.

    Procura por arquivos .lnk que começam com o nome do programa informado
    (case-insensitive) e executa o primeiro encontrado.

    Args:
        query (str): Nome do programa a ser aberto (ex: "vscode", "projeto").
                           Não é necessário incluir a extensão .lnk.

    Returns:
        str: Mensagem de sucesso ou erro indicando o resultado da operação.

    Examples:
        open_program("vscode")
        "Programa 'vscode' aberto com sucesso."

        open_program("projeto")
        "Programa 'projeto' aberto com sucesso."
    """
    links_dir = os.path.join(os.path.expanduser("~"), "Links")

    if not os.path.exists(links_dir):
        return f"Diretório de links não encontrado: {links_dir}"

    for item in os.listdir(links_dir):
        if item.lower().startswith(query.lower()) and item.lower().endswith('.lnk'):
            shortcut_path = os.path.join(links_dir, item)
            try:
                os.startfile(shortcut_path)
                return f"Programa '{query}' aberto com sucesso."
            except Exception as e:
                return f"Erro ao abrir o programa '{query}': {e}"


def capture_screenshot() -> ToolResult:
    """Captura um screenshot da tela do usuário para análise visual.

    Returns:
        ToolResult: Contém a imagem capturada para análise pelo modelo.
    """
    screenshot = pyautogui.screenshot()
    screenshot.save("data/screenshot.png")
    return ToolResult(
        content="Screenshot capturado. Analisando a imagem...",
        images=[Image(filepath="data/screenshot.png")]
    )

# ============= Execução ============== #
if __name__ == "__main__":
    open_program("projeto")
