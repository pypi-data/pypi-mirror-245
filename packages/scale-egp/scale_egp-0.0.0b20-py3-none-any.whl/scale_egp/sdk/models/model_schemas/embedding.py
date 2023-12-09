from typing import List

from .common import BaseModelRequest, BaseModelResponse


class EmbeddingRequest(BaseModelRequest):
    text: str


class EmbeddingResponse(BaseModelResponse):
    embedding: List[float]
