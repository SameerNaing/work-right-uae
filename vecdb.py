from typing import Optional, List, Union

import pandas as pd
from llama_index.core.schema import TextNode

from llama_index.core.response_synthesizers import TreeSummarize, SimpleSummarize
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.vector_stores import SimpleVectorStore, MetadataFilter, MetadataFilters
from llama_index.core import PromptTemplate



def _get_nodes():    
    df = pd.read_csv("./data/documents.csv")

    nodes = []
    for _, row in df.iterrows():
        # Create a TextNode with the document text
        node = TextNode(
            text=row["content"],
            metadata={"documentType": str(row["documentType"])},
        )
        # Add the node to the index
        nodes.append(node)
        
    return nodes

embed_model = HuggingFaceEmbedding(model_name="nomic-ai/nomic-embed-text-v2-moe", trust_remote_code=True)

vec_store = SimpleVectorStore()

storage_context = StorageContext.from_defaults(vector_store=vec_store)


# Create the vector index (initially with no nodes)
index = VectorStoreIndex(
    nodes=_get_nodes(), 
    storage_context=storage_context, 
    embed_model=embed_model
)


qa_prompt_tmpl = (
    "You are a legal assistant helping users understand UAE labor laws and MOHRE services.\n"
    "Read the context information carefully and answer the query based **only on the provided content**, not prior knowledge.\n"
    "Your answer must be complete, specific, and should mention the relevant article, law, or regulation if available.\n"
    "Avoid vague or generic advice. Do not skip critical conditions, exceptions, or timelines.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Query: {query_str}\n"
    "Answer: "
)

qa_prompt = PromptTemplate(qa_prompt_tmpl)


def create_law_db_query_tool(
    llm,
    description: str,
    name: str,
    doc_type: Optional[Union[str, List[str]]] = None,
):
    
    summarizer = TreeSummarize(verbose=True, summary_template=qa_prompt, llm=llm)
    # summarizer = SimpleSummarize(text_qa_template=qa_prompt, llm=llm)
    metadata_filter = None 
    
    
    if doc_type:
        metadata_filter = MetadataFilters(
            filters = [
                MetadataFilter(key="documentType", value=doc_type)
            ]
        )
        
    # Create retriever with optional metadata filters
    retriever = index.as_retriever(
        similarity_top_k=3,
        filters=metadata_filter
    ) if metadata_filter else index.as_retriever(similarity_top_k=3)

    # Build query engine using RetrieverQueryEngine directly
    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        llm=llm,
        response_synthesizer=summarizer
    )

    return QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name=name,
        description=description,
    )

# Example usage:
# Create a default tool with no filters (searches all document types)
mohre_docs_query_tool = lambda llm : create_law_db_query_tool(
    llm=llm,
    description="Use this tool for answering questions based on official MOHRE laws and regulations documents, including employment contracts, labor rights, and work permit rules.",
    name="mohre_docs_query_tool",
    doc_type="mohre-docs",
)

mohre_services_query_tool = lambda llm : create_law_db_query_tool(
    llm=llm,
    description="Use this tool to answer questions related to services provided by MOHRE, such as filing complaints, obtaining work permits, dispute resolution, and Emiratisation initiatives.",
    name="mohre_services_query_tool",
    doc_type="mohre-services",
)

uae_jobs_query_tool = lambda llm : create_law_db_query_tool(
    llm=llm,
    description="Use this tool to provide information about working in the UAE, job searching, employment conditions, and job market policies.",
    name="uae_jobs_query_tool",
    doc_type="uae-jobs",
)

mohre_faq_query_tool = lambda llm : create_law_db_query_tool(
    llm=llm,
    description="Use this tool to answer frequently asked questions regarding MOHRE processes, portal use, and service-related clarifications.",
    name="mohre_faq_query_tool",
    doc_type="mohre-faq",
)

uae_visa_id_query_tool = lambda llm : create_law_db_query_tool(
    llm=llm,
    description="Use this tool for questions about UAE visas, entry permits, Emirates ID applications, renewals, and related immigration procedures.",
    name="uae_visa_id_query_tool",
    doc_type="uae-visa-emirates-id",
)

uae_passport_travel_query_tool = lambda llm : create_law_db_query_tool(
    llm=llm,
    description="Use this tool to answer queries about UAE passport services, travel documents, and lost/stolen passport procedures.",
    name="uae_passport_travel_query_tool",
    doc_type="uae-passport-travel",
)

# search all document types
uae_law_query_tool = lambda llm : create_law_db_query_tool(
    llm=llm,
    description="Useful for answering questions about MOHRE UAE laws, work regulations, job and visa policies, and general UAE procedures by searching across all document types.",
    name="uae_law_query_tool",
    doc_type=None,
)

tools = lambda llm : [
    mohre_docs_query_tool(llm),
    mohre_services_query_tool(llm),
    uae_jobs_query_tool(llm),
    mohre_faq_query_tool(llm),
    uae_visa_id_query_tool(llm),
    uae_passport_travel_query_tool(llm),
    uae_law_query_tool(llm)
]

