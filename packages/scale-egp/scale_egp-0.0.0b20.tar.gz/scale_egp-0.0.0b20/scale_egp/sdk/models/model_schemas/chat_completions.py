# these pydantic model definitions were copied from
# packages/egp-api-backend/egp_api_backend/server/internal/entities.py
from typing import List

from .completions_shared import CompletionBaseRequest, CompletionBaseResponse
from .message import Message


class ChatCompletionRequest(CompletionBaseRequest):
    messages: List[Message]


class ChatCompletionResponse(CompletionBaseResponse):
    message: Message
