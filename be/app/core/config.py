import torch
from pydantic_settings import BaseSettings
from firecrawl import FirecrawlApp

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig 


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
    JWT_SECRET: str = "$EcR3t"
    JWT_ACCESS_TOKEN_EXPIRE_DAYS: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 40
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()

firecrawl_app = FirecrawlApp(
    api_url=settings.FIRECRAWL_URL, api_key=settings.FIRECRAWL_API_KEY
)

embed_model = OllamaEmbedding(
    base_url=settings.LLM_URL, model_name=settings.EMBED_MODEL
)

model_path = "app/core/models/llm-model"

quantization_config = BitsAndBytesConfig(
   load_in_4bit=True,
   bnb_4bit_quant_type="nf4",
   bnb_4bit_use_double_quant=True,
   bnb_4bit_compute_dtype=torch.float16
)
tokenizer = AutoTokenizer.from_pretrained(
    model_path
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto",

    quantization_config=quantization_config
)

print(model)



mohre_llm = HuggingFaceLLM(model=model, tokenizer=tokenizer, is_chat_model=True, local_files_only=True)

llm = Ollama(base_url=settings.LLM_URL, model=settings.LLM_MODEL, request_timeout=10000)
