# query_data.py
import argparse
from langchain.prompts import ChatPromptTemplate
# Besser: langchain_community.vectorstores
#from langchain_community.vectorstores.chroma import Chroma
# Besser: ChatVertexAI für Gemini
from langchain_google_vertexai import ChatVertexAI
# Dein Embedding-Modul
from embedding import get_embedding_function
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv

# Generiert von Gemini
load_dotenv()

PROJECT_ID = os.environ.get("PROJECT_ID", "meine-rag-cloud")
LOCATION = os.environ.get("LOCATION", "europe-west3")
CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """..."""

def query_rag(query_text: str):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    model = ChatVertexAI(model_name="gemini-2.0-flash-lite-001", project=PROJECT_ID, location=LOCATION)


CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Beantworte die Frage nur basierend auf dem folgenden Kontext:

{context}

---

Beantworte die Frage basierend auf dem obigen Kontext: {question}
"""


def query_rag(query_text: str):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Suche in der DB
    results = db.similarity_search_with_score(query_text, k=5)  # k=Anzahl der Chunks

    if not results:
        print("Keine relevanten Dokumente gefunden.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Nutze ChatVertexAI für Gemini
    model = ChatVertexAI(model_name="gemini-2.0-flash-lite-001")

    # Rufe das Modell auf
    response = model.invoke(prompt)
    # Die Antwort ist normalerweise im .content Attribut
    response_content = response.content

    # Hole die Quellen (funktioniert am besten, wenn populate_db.py die IDs erzeugt hat)
    sources = [doc.metadata.get("id", doc.metadata.get("source", None)) for doc, _score in
               results]  # Fallback auf source
    formatted_response = f"Antwort: {response_content}\nQuellen: {sources}"
    print(formatted_response)
    return response_content


# Füge argparse wieder hinzu für Flexibilität
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="Der Anfragetext.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


if __name__ == "__main__":
    main()