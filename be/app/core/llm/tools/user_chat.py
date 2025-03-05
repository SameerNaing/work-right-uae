from llama_index.core.tools import FunctionTool
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters


from app.core.constants import chat_history_chroma_collection
from app.dependencies.chroma_repo import get_chroma_repository


def get_user_chats(query: str, user_id: str, chat_id: str):
    print(
        "user_id",
        user_id,
        "chat_id",
        chat_id,
    )
    try:
        chroma_repo = get_chroma_repository(chat_history_chroma_collection)
        metadata_filters = MetadataFilters(
            filters=[
                MetadataFilter(key="user_id", value=user_id),
                MetadataFilter(key="chat_id", value=chat_id),
            ]
        )

        retrieved_nodes = chroma_repo.index.as_retriever(
            similarity_top_k=3, filters=metadata_filters
        ).retrieve(query)

        result = ""
        for node in retrieved_nodes:
            result += node.node.text + "\n"

        return result

    except Exception as e:
        return f"An error occurred while retrieving chat messages.\n{e}"


def retrieve_user_chat_tool(user_id: str, chat_id: str):

    def retrieve_user_chat(query: str) -> str:
        """This tool retrieves the chat history for a specific user for a specific chat.

        Args:
            query (str): query string for chat history

        Returns:
            str: chat history
        """
        return get_user_chats(query, user_id, chat_id)

    return FunctionTool.from_defaults(
        fn=retrieve_user_chat,
        name="retrieve_user_chat",
        description="""This tool retrieves the chat history for a specific user for a specific chat.""",
    )
