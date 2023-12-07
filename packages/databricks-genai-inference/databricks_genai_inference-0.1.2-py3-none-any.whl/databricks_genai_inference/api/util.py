"""Utils for the API.
"""
from enum import Enum


class EmbeddingModel(Enum):
    """Supported embedding models.
    """
    BGE_LARGE_ENG = 'bge-large-en'


class CompletionModel(Enum):
    """Supported completion models.
    """
    MPT_7B_INSTRUCT = 'mpt-7b-instruct'
    MPT_30B_INSTRUCT = 'mpt-30b-instruct'


class ChatCompletionModel(Enum):
    """Supported chat completion models.
    """
    LLAMA_2_70B_CHAT = 'llama-2-70b-chat'
