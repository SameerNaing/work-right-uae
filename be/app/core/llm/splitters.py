from typing import List
from llama_index.core.node_parser import (
    MarkdownNodeParser,
    SemanticSplitterNodeParser,
)
from llama_index.core import Document
from llama_index.core.schema import TextNode


from app.core.config import embed_model


class SplittersManager:
    def __init__(self):
        self.markdown_parser = MarkdownNodeParser(num_workers=4)
        self.semantic_splitter = SemanticSplitterNodeParser(
            embed_model=embed_model, num_workers=4
        )

    def markdown_splitter(self, docs, metadata, length_threshold=500) -> List[TextNode]:
        docs = [Document(text=doc, metadata=metadata) for doc in docs]

        nodes = self.markdown_parser.get_nodes_from_documents(documents=docs)

        final_nodes = []

        for node in nodes:
            text = node.get_content()
            if len(text) > length_threshold:
                new_nodes = self.semantic_splitter.get_nodes_from_documents(
                    documents=[Document(text=text, metadata=metadata)]
                )
                final_nodes.extend(new_nodes)
                continue

            final_nodes.append(node)

        return final_nodes


splitter_manager = SplittersManager()
