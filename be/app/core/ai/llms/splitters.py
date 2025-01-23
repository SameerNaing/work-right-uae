from llama_index.core.node_parser import (
    MarkdownNodeParser,
    SemanticSplitterNodeParser,
)
from llama_index.core import Document


from app.core.config import embed_model


def markdown_splitter(docs, metadata, length_threshold=500, num_workers=4):
    markdown_parser = MarkdownNodeParser(num_workers=num_workers)
    semantic_splitter = SemanticSplitterNodeParser(
        embed_model=embed_model, num_workers=num_workers
    )

    docs = [Document(text=doc, metadata=metadata) for doc in docs]

    nodes = markdown_parser.get_nodes_from_documents(documents=docs)

    final_nodes = []

    for node in nodes:
        text = node.get_content()
        if len(text) > length_threshold:
            new_nodes = semantic_splitter.get_nodes_from_documents(
                documents=[Document(text=text, metadata=metadata)]
            )
            final_nodes.extend(new_nodes)
            continue

        final_nodes.append(node)

    return final_nodes
