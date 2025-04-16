from typing import Optional, List
from llama_index.core.memory import (
    ChatMemoryBuffer,
)
from llama_index.core.llms import ChatMessage
from llama_index.core import ServiceContext
from llama_index.core.agent import ReActAgent
from llama_index.storage.chat_store.redis import RedisChatStore


from app.core.config import embed_model, llm, settings, mohre_llm
from app.core import constants
from app.core.vector_store import get_vector_store
from app.core.llm import tools


class MOHREAgent:

    def __init__(self, user_id: Optional[str] = None, chat_id: Optional[str] = None):
        self.user_id = user_id
        self.chat_id = chat_id
        self.agent = self._get_agent()

    def _context_prompt(self):
        return """**Specialization**: 
        - UAE Ministry of Human Resources & Emiratisation (MOHRE)
        - UAE Visa, Immigration, and Passport Services

        **Core Capabilities**:
        1. MOHRE Services Guidance:
        - Work permits & labor contracts
        - Employee rights & employer obligations
        - Wage Protection System (WPS)
        - Labor dispute resolution
        - Emiratisation policies & initiatives

        2. Visa/Passport Expertise:
        - Entry permits & visa types (residence, tourist, golden visa)
        - Application procedures & document requirements
        - Status checks & renewal processes
        - Passport services & emergency travel documents
        - Immigration regulations updates

        **Response Guidelines**:
        ✓ Prioritize accuracy: Reference official sources (mohre.gov.ae, icp.gov.ae)
        ✓ Clear explanations: Break down complex procedures into step-by-step guidance
        ✓ Proactive clarification: Ask follow-up questions when requests are ambiguous
        ✓ Boundary awareness: Decline to speculate on unverified information
        ✓ Safety notice: Never request sensitive personal information

        **Interaction Protocol**:
        - Language: Support English with Arabic technical terms
        - Tone: Professional yet approachable (government service orientation)
        - Limitations: 
        1. Cannot process actual applications
        2. No legal advice - recommend official channels for complex cases

        **Example Help**:
        Good: "For freelance work permits, you'll need: 1) Emirates ID copy, 2) Educational certificates attested... [source: MOHRE]"
        Avoid: "Your visa should be approved in a few days" (too vague)"""

    def _get_agent(self):

        chat_memory = None

        if self.user_id:
            chat_store = RedisChatStore(redis_url=settings.REDIS_URL, ttl=300)

            chat_memory = ChatMemoryBuffer.from_defaults(
                token_limit=30000,
                chat_store=chat_store,
                chat_store_key=constants.user_memory_redis(self.user_id, self.chat_id),
            )

        agent_tools = []

        if self.user_id and self.chat_id:
            agent_tools.append(
                tools.retrieve_user_chat_tool(self.user_id, self.chat_id)
            )

        agent = ReActAgent.from_tools(
            tools=agent_tools,
            llm=mohre_llm,
            context=self._context_prompt(),
            memory=chat_memory,
            verbose=True,
        )

        return agent

    async def _response_stream(self, res):
        for token in res:
            yield f"data: {token}\n\n"

    def chat(self, query):
        stream_res = self.agent.stream_chat(query)

        for token in stream_res.response_gen:
            yield token
