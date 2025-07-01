from dotenv import load_dotenv
load_dotenv()
import os
from crewai_tools import ScrapeWebsiteTool, SerperDevTool, PDFSearchTool


os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
os.environ['EMBEDDING_API_KEY'] = os.getenv('EMBEDDING_API_KEY')
# Setze GOOGLE_API_KEY auf den Wert von GEMINI_API_KEY
os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')

# Initialize the tool for internet searching capabilities
search_tool = SerperDevTool()

# Initialize the website scraping tool
scrape_tool = ScrapeWebsiteTool()


# In agent.py (oder wo du das Tool instanziierst)
from crewai_tools import RagTool
import os



pdf_search_tool_direct = PDFSearchTool(
    config=dict(
        llm=dict(
            provider="google",
            config=dict(
                model="gemini/gemini-1.5-flash-8b",
            ),
        ),
        embedder=dict(
            provider="google",
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
            ),
        ),
    )
)
# Generiert von Gemini
# In tools.py (Wieder die Version MIT args_schema)
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from query_data import query_rag

class ChromaSearchInput(BaseModel):
    query: str = Field(description="Die Suchanfrage als String, um die ChromaDB zu durchsuchen.")

class ChromaSearchTool(BaseTool):
    name: str = "ChromaDB PDF Search"
    description: str = ("Fragt die ChromaDB PDF-Datenbank nach relevanten Inhalten zur Anfrage ab. "
                        "Die Eingabe sollte die Suchanfrage als String sein.")
    args_schema: type[BaseModel] = ChromaSearchInput # <--- Schema wieder aktivieren

    def _run(self, query: str) -> str: # <--- Erwartet wieder String
        """Benutzt das Tool."""
        print(f"--- TOOL INFO (BaseTool mit Schema): Empfangene Query: '{query}'") # Angepasster Print
        try:
            return query_rag(query)
        except Exception as e:
            print(f"--- TOOL ERROR (BaseTool mit Schema): Fehler bei query_rag für '{query}': {e}")
            return f"Fehler bei der Suche in der Wissensdatenbank: {e}"

rag_tool = ChromaSearchTool()

