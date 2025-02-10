from pydantic_settings import BaseSettings
from firecrawl import FirecrawlApp
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+aiomysql://root:admin@127.0.0.1:3306/mohre"
    FIRECRAWL_URL: str = "http://localhost:3002"
    REDIS_URL: str = "redis://localhost:6379"
    PORT: int = 3001
    LLM_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "gemma2:9b"
    EMBED_MODEL: str = "nomic-embed-text"
    FIRECRAWL_URL: str = "http://localhost:3002"
    FIRECRAWL_API_KEY: str = ""
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
    MOHRE_DOC_CHROMA_COLLECTION: str = "mohre"
    MAILER_USER: str
    MAILER_PASSWORD: str
    MAILER_HOST: str
    MAILER_PORT: int

    class Config:
        env_file = ".env"


settings = Settings()

firecrawl_app = FirecrawlApp(
    api_url=settings.FIRECRAWL_URL, api_key=settings.FIRECRAWL_API_KEY
)

embed_model = OllamaEmbedding(
    base_url=settings.LLM_URL, model_name=settings.EMBED_MODEL
)

llm = Ollama(base_url=settings.LLM_URL, model=settings.LLM_MODEL, request_timeout=10000)
