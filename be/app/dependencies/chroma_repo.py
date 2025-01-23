from app.db.vector_store import get_vector_store
from app.repositories.chroma_repository import ChromaRepository


def get_chroma_repository(collection_name: str):
    vec = get_vector_store(collection_name)
    return ChromaRepository(collection=vec)
