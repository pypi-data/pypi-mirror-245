# Note that this file is a duplicate of packages/egp-api-backend/egp_api_backend/server/internal/entities_models.py
# We cannot import it in the SDK directly.

from enum import Enum
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from typing import Dict, List, Literal, Union

from pydantic import Field
from scale_egp.utils.model_utils import BaseModel


class ModelVendor(str, Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    ANTHROPIC = "ANTHROPIC"
    LLMENGINE = "LLMENGINE"
    OTHER = "OTHER"

class OpenAIVendorConfiguration(BaseModel):
    vendor: Literal[ModelVendor.OPENAI] = Field(ModelVendor.OPENAI)


class LaunchVendorConfiguration(BaseModel):
    vendor: Literal[ModelVendor.LLMENGINE] = Field(ModelVendor.LLMENGINE)
    cpus: int = Field(1)
    gpus: int = Field(0)
    registry: str
    image: str
    tag: str
    command: List[str] = Field(default_factory=list)
    env: Dict[str, str] = Field(default_factory=dict)
    readiness_initial_delay_seconds: int = Field(5)

VendorConfiguration = Annotated[
    Union[LaunchVendorConfiguration, OpenAIVendorConfiguration],
    Field(discriminator="vendor")]