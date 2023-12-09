from typing import List, Optional

from pydantic import Field

from .common import BaseModelRequest, BaseModelResponse


class CompletionBaseRequest(BaseModelRequest):
    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=1.0,
        description="What sampling temperature to use, between [0, 1]. Higher values like 0.8 "
        "will make the output more random, while lower values like 0.2 will make it "
        "more focused and deterministic. Setting temperature=0.0 will enable fully "
        "deterministic "
        "(greedy) sampling.",
    )
    stop_sequences: Optional[List[str]] = Field(
        default=None,
        max_items=4,
        description="List of up to 4 sequences where the API will stop generating further tokens. "
        "The returned text will not contain the stop sequence.",
    )
    max_tokens: Optional[int] = Field(
        default=None,
        description="The maximum number of tokens to generate in the completion. The token count "
        "of your prompt plus max_tokens cannot exceed the model's context length. If not, "
        "specified, max_tokens will be determined based on the model used: \n"
        "| Model API family | Model API default | EGP applied default |\n"
        "| --- | --- | --- |\n"
        "| OpenAI Completions | [`16`](https://platform.openai.com/docs/api-reference/completions/create#max_tokens) | `context window - prompt size` |\n"
        "| OpenAI Chat Completions | [`context window - prompt size`](https://platform.openai.com/docs/api-reference/chat/create#max_tokens) | `context window - prompt size` |\n"
        "| LLM Engine | [`max_new_tokens`](https://github.com/scaleapi/launch-python-client/blob/207adced1c88c1c2907266fa9dd1f1ff3ec0ea5b/launch/client.py#L2910) parameter is required | `100` |\n"
        "| Athropic Claude 2 | [`max_tokens_to_sample`](https://docs.anthropic.com/claude/reference/complete_post) parameter is required | `10000` |\n",
    )


class CompletionBaseResponse(BaseModelResponse):
    finish_reason: Optional[str]
