from typing import Literal

from pydantic import BaseModel, Field


# Memory Strategies
class LastKMemoryStrategyParams(BaseModel):
    k: int = Field(
        ...,
        ge=1,
        description="The maximum number of previous messages to remember.",
    )


class LastKMemoryStrategy(BaseModel):
    name: Literal["last_k"] = Field(
        default="last_k",
        const=True,
        description="Name of the memory strategy. Must be `last_k`.\n\n"
        "This strategy truncates the message history to the last `k` messages. It is "
        "the simplest way to prevent the model's context limit from being exceeded. "
        "However, this strategy only allows the model to have short term memory. For "
        "longer term memory, please use one of the other strategies.",
    )
    params: LastKMemoryStrategyParams = Field(
        ..., description="Configuration parameters for the memory strategy."
    )

    class Config(BaseModel.Config):
        title = "Last K Memory Strategy"
