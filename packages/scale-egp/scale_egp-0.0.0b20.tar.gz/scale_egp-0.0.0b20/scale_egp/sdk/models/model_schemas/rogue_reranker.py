from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class RougeType(str, Enum):
    rouge1 = "rouge1"
    rouge2 = "rouge2"
    rougeL = "rougeL"


class RougeScore(str, Enum):
    precision = "precision"
    recall = "recall"
    fmeasure = "fmeasure"


class RerankRequest(BaseModel):
    query: str = Field(...)
    chunks: List[str] = Field(...)


class CrossEncoderRerankRequest(RerankRequest):
    pass


# Any custom input classes' members MUST be OPTIONAL, as currently the gateway doesn't support anything else
class RougeRerankRequest(RerankRequest):
    rouge_type: Optional[RougeType] = Field(RougeType.rouge2)
    score: Optional[RougeScore] = Field(RougeScore.recall)
    use_stemmer: Optional[bool] = Field(True)
    split_summaries: Optional[bool] = Field(False)


class RerankResponse(BaseModel):
    chunk_scores: List[float]
