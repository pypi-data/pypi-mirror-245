"""
DO NOT ADD ANY IMPORTS IN THIS FILE (except basic Python libs & Pydantic). IT IS SHARED WITH DOCKER IMAGES OF MODELS.
"""

from enum import Enum


class ModelType(str, Enum):
    COMPLETION = "COMPLETION"
    CHAT_COMPLETION = "CHAT_COMPLETION"
    AGENT = "AGENT"
    EMBEDDING = "EMBEDDING"
    RERANKING = "RERANKING"
