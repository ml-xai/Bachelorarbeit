import argparse
import os
import shutil
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from embedding import get_embedding_function
from langchain_chroma import Chroma

# Generiert von Gemini
CHROMA_PATH = "chroma"
DATA_PATH = r"C:\Users\maxi-\PycharmProjects\PythonProject\Gemini_AI_Agent\gemini_agents\Rag_PDF"

def load_documents():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
        chunk.metadata["id"] = chunk_id
    return chunks

def add_to_chroma(chunks: list[Document]):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    chunks_with_ids = calculate_chunk_ids(chunks)
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Anzahl existierender Dokumente in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        chunk_id = chunk.metadata.get("id")
        if chunk_id is None:
            print(f"Warnung: Chunk ohne ID gefunden: {chunk.page_content[:50]}...")
            continue
        if chunk_id not in existing_ids:
            new_chunks.append(chunk)

    if new_chunks:
        print(f"👉 Füge neue Dokumente hinzu: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    # db.persist() entfernt, da nicht mehr nötig

def check_db_content():
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    all_docs = db.get(include=["metadatas"])
    print(f"Anzahl Dokumente in DB: {len(all_docs['ids'])}")
    sources_in_db = set()
    for metadata in all_docs['metadatas']:
        if metadata and 'source' in metadata:
            sources_in_db.add(metadata['source'])
    print("\nDateien in der Datenbank:")
    for source in sorted(list(sources_in_db)):
        print(f"- {source}")

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


def search_documents(query):
    from langchain_chroma import Chroma
    db = Chroma(persist_directory="chroma", embedding_function=get_embedding_function())
    results = db.similarity_search_with_score(query, k=5)
    return [doc for doc, _score in results]  # Rückgabe der Dokumente

def search_chroma_db(query: str) -> str:
    """Durchsucht die ChromaDB nach relevanten Inhalten und gibt die Ergebnisse als String zurück."""
    results = search_documents(query)  # Deine bestehende Suchfunktion für ChromaDB
    return "\n".join([doc.page_content for doc in results])



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)

if __name__ == "__main__":
    main()
    check_db_content()
