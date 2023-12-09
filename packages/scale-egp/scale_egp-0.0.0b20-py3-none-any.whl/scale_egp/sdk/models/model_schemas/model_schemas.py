from typing import Tuple

from pydantic import BaseModel

# Note: the relative imports here are important since
# these module names must also be valid within model docker containers.
from .agents import ExecuteAgentRequest, ExecuteAgentResponse
from .chat_completions import ChatCompletionRequest, ChatCompletionResponse
from .completions import CompletionRequest, CompletionResponse
from .embedding import EmbeddingRequest, EmbeddingResponse
from .model_type import ModelType
from .reranking import RerankingRequest, RerankingResponse

MODEL_SCHEMAS: dict[ModelType, Tuple[BaseModel, BaseModel]] = {
    ModelType.COMPLETION: [CompletionRequest, CompletionResponse],
    ModelType.CHAT_COMPLETION: [ChatCompletionRequest, ChatCompletionResponse],
    ModelType.AGENT: [ExecuteAgentRequest, ExecuteAgentResponse],
    ModelType.RERANKING: [RerankingRequest, RerankingResponse],
    ModelType.EMBEDDING: [EmbeddingRequest, EmbeddingResponse],
}
