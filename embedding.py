from langchain_google_vertexai import VertexAIEmbeddings

def get_embedding_function():
    return VertexAIEmbeddings(model_name="text-multilingual-embedding-002")


