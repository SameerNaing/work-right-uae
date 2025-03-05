from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex


class ChromaRepository:
    def __init__(self, collection: ChromaVectorStore, index: VectorStoreIndex):
        self.collection = collection
        self.index = index

    def add_node_to_collection(self, nodes):
        self.index.insert_nodes(nodes=nodes)

    def add_document_to_collection(self, document):
        self.index.insert(document=document)

    def query_documents_by_metadata(self, metadata_filter: dict) -> list:
        results = self.collection.query(metadata_filter=metadata_filter)
        return results

    def delete_document_by_metadata(self, metadata_filter: dict):
        self.collection.delete(metadata_filter=metadata_filter)
