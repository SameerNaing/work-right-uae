from llama_index.vector_stores.chroma import ChromaVectorStore


class ChromaRepository:
    def __init__(self, collection: ChromaVectorStore):
        self.collection = collection

    def add_document_to_collection(self, document: str, metadata: dict):
        self.collection.add(document, metadata=metadata)

    def query_documents_by_metadata(self, metadata_filter: dict) -> list:
        results = self.collection.query(metadata_filter=metadata_filter)
        return results

    def delete_document_by_metadata(self, metadata_filter: dict):
        self.collection.delete(metadata_filter=metadata_filter)
