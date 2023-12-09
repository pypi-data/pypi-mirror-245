from .completions_shared import CompletionBaseRequest, CompletionBaseResponse


class CompletionRequest(CompletionBaseRequest):
    prompt: str


class CompletionResponse(CompletionBaseResponse):
    text: str
