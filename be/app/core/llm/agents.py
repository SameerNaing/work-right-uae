from typing import AsyncGenerator
from llama_index.core.llms import ChatMessage
from llama_index.core import ServiceContext
from llama_index.core.agent import ReActAgent


from app.db.vector_store import get_chroma_client
from app.core.config import llm


class MOHREAgent:
    def __init__(self):
        self.agent = self._get_agent()

    def _get_agent(self):
        context_prompt = "Role: This agent is designed to assist users with inquiries related to UAE MOHRE (Ministry of Human Resources & Emiratisation) and UAE visa and passport services."

        agent = ReActAgent.from_tools(
            tools=[],
            llm=llm,
            context=context_prompt,
        )

        return agent

    async def _response_stream(self, res):
        for token in res:
            yield f"{token}"

    def chat(self, query):
        stream_res = self.agent.stream_chat(query)

        return self._response_stream(stream_res.response_gen)


mohre_agent = MOHREAgent()
