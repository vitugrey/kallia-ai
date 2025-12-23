# ============ Importação ============ #
import os
from dotenv import load_dotenv

from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.db.sqlite import SqliteDb


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


# ============= Execução ============== #
if __name__ == "__main__":
    pdf_path = "C:\\Users\\USER\\Downloads\\exemplo.pdf"
    if os.path.exists(pdf_path):
        knowledge.add_content(path=pdf_path)
        print("Conteúdo adicionado à base de conhecimento:", pdf_path)
    else:
        print("Arquivo não encontrado:", pdf_path)