from typing import List

from .common import BaseModelRequest, BaseModelResponse


class RerankingRequest(BaseModelRequest):
    query: str
    chunks: List[str]


class RerankingResponse(BaseModelResponse):
    chunk_scores: List[float]
