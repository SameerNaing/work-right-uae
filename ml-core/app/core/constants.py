from enum import Enum

MOHRE_URL = "https://www.mohre.gov.ae"
MOHRE_FAQ_URL = "https://www.mohre.gov.ae/en/laws-and-regulations/laws/faq.aspx"
MOHRE_SERVICES_URL = "https://www.mohre.gov.ae/en/services.aspx"
MOHRE_DOC_LAWS_URL = "https://www.mohre.gov.ae/en/laws-and-regulations/laws.aspx"
MOHRE_DOC_RESOLUTION_CIRCULARS_URL = (
    "https://www.mohre.gov.ae/en/laws-and-regulations/resolutions-and-circulars.aspx"
)
MOHRE_DOC_INTERNATIONAL_AGREE_ULR = (
    "https://www.mohre.gov.ae/en/laws-and-regulations/international-agreements.aspx"
)


chat_history_chroma_collection = "chat_history"

user_memory_redis = lambda user_id, chat_id: f"memory:{user_id}_{chat_id}"


class ChatRole(Enum):
    USER = "user"
    AGENT = "agent"


class ChatFeedBack(Enum):
    LIKE = "like"
    DISLIKE = "dislike"
