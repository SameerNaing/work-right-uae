from chromadb import HttpClient
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore

from app.core.config import embed_model, settings


def get_chroma_client() -> HttpClient:
    return HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)


def get_vector_store(collection_name: str):
    chroma_client = get_chroma_client()
    collection = chroma_client.get_or_create_collection(collection_name)
    vec_store = ChromaVectorStore(collection)
    storage_context = StorageContext.from_defaults(vector_store=vec_store)

    index = VectorStoreIndex(
        nodes=[], storage_context=storage_context, embed_model=embed_model
    )

    return collection, index, vec_store
