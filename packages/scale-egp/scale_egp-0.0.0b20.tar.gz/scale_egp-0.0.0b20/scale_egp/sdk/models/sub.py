from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional, Union, List, Dict, Any

from pydantic import Field, validator

from scale_egp.sdk.enums import (
    EmbeddingModelName,
    DataSource,
    DeduplicationStrategy,
    ChunkingStrategy,
    EvaluationType,
    QuestionType,
    ExtraInfoSchema,
    CrossEncoderModelName,
)
from scale_egp.utils.model_utils import BaseModel, Entity

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

class EmbeddingConfig(BaseModel):
    """
    A data model representing the configuration of the embedding.

    Attributes:
        embedding_model: The name of the embedding model to use.
    """

    embedding_model: EmbeddingModelName = Field(
        description="The name of the embedding model to use. We only support the models listed "
        "here so far."
    )


class ArtifactsStatus(BaseModel):
    """
    A data model representing the status of the artifacts in a knowledge base.

    Attributes:
        artifacts_completed: Number of artifacts uploaded successfully.
        artifacts_pending: Number of artifacts awaiting upload.
        artifacts_uploading: Number of artifacts with upload in progress.
        artifacts_failed: Number of artifacts that failed upload.
    """

    artifacts_completed: int
    artifacts_pending: int
    artifacts_uploading: int
    artifacts_failed: int


class ChunksStatus(BaseModel):
    """
    A data model representing the status of the chunks in an artifact.

    Attributes:
        chunks_completed: Number of chunks uploaded successfully
        chunks_pending: Number of chunks awaiting upload
        chunks_failed: Number of chunks that failed upload
    """

    chunks_completed: int
    chunks_pending: int
    chunks_failed: int


class S3DataSourceConfig(BaseModel):
    """
    A data model representing the configuration of a S3 data source.

    Attributes:
        source: The data source type. Must be 's3'.
        s3_bucket: The name of the S3 bucket where the data is stored
        s3_prefix: The prefix of the S3 bucket where the data is stored
        aws_region: The AWS region where the S3 bucket is located
        aws_account_id: The AWS account ID that owns the S3 bucket
    """

    source: Literal[DataSource.S3] = DataSource.S3.value
    s3_bucket: str
    aws_region: str
    aws_account_id: str
    s3_prefix: Optional[str] = None


class SharePointDataSourceConfig(BaseModel):
    """
    A data model representing the configuration of a SharePoint data source.

    Attributes:
        source: The data source type. Must be 'sharepoint'.
        client_id: The client ID associated with this SharePoint site
        tenant_id: The tenant ID that the SharePoint site is within
        site_id: The site ID for this SharePoint site
        folder_path: The nested folder path to read files from the root of the site
        recursive: Whether to recurse through the folder contents
    """

    source: Literal[DataSource.SHAREPOINT] = DataSource.SHAREPOINT.value
    client_id: str
    tenant_id: str
    site_id: str
    folder_path: Optional[str] = ""
    recursive: Optional[bool] = True


class GoogleDriveDataSourceConfig(BaseModel):
    """
    A data model representing the configuration of a Google Drive data source.

    Attributes:
        source: The data source type. Must be 'google_drive'.
        drive_id: The ID of the Google Drive to retrieve contents from
    """

    source: Literal[DataSource.GOOGLE_DRIVE] = DataSource.GOOGLE_DRIVE.value
    drive_id: str


class LocalChunksSourceConfig(BaseModel):
    """
    A data model representing the configuration of a local chunks data source.

    Attributes:
        source: The data source type. Must be 'local_chunks'.
        artifact_name: The file name assigned to the artifact, containing a file extension.
            Adding an extension is mandatory, to allow detecting file types for text extraction.
        artifact_uri: A unique identifier for an artifact within the knowledge base, such as full
            path in a directory or file system.
        deduplication_strategy: Action to take if an artifact with the same name already exists
            in the knowledge base. Can be either Overwrite (default) or Fail.
    """

    source: Literal[DataSource.LOCAL_CHUNKS] = DataSource.LOCAL_CHUNKS.value
    artifact_name: str
    artifact_uri: str
    deduplication_strategy: Optional[DeduplicationStrategy] = DeduplicationStrategy.OVERWRITE


class SharePointDataSourceAuthConfig(BaseModel):
    """
    A data model representing the configuration of a SharePoint data source.

    Attributes:
        source: The data source type. Must be 'sharepoint'.
        client_secret: The secret for the app registration associated with this SharePoint site
    """

    source: Literal[DataSource.SHAREPOINT] = DataSource.SHAREPOINT.value
    client_secret: str


class CharacterChunkingStrategyConfig(BaseModel):
    """
    A data model representing the configuration of a character chunking strategy.

    Attributes:
        strategy: The chunking strategy type. Must be 'character'.
        separator: Character designating breaks in input data. Text data will first be split
            into sections by this separator, then each section will be split into chunks
            of size `chunk_size`.
        chunk_size: Maximum number of characters in each chunk. If not specified, a chunk size
            of 1000 will be used.
        chunk_overlap: Number of characters to overlap between chunks. If not specified, an overlap
            of 200 will be used. For example if the chunk size is 3 and the overlap size
            is 1, and the text to chunk is 'abcde', the chunks will be 'abc', 'cde'.
    """

    strategy: Literal[ChunkingStrategy.CHARACTER] = ChunkingStrategy.CHARACTER.value
    separator: Optional[str] = "\n\n"
    chunk_size: Optional[int] = 1000
    chunk_overlap: Optional[int] = 200


class CategoricalChoice(BaseModel):
    """
    A choice for a categorical question.

    This is only used in a StudioEvaluationConfig to specify a choice for a  question that will be
    asked to users when they are evaluating generated outputs in the EGP annotation UI.

    Attributes:
        label: The text displayed to annotators for this choice.
        value: The value reported in the TestCaseResult for this question if this choice is
            selected.

            If users would like to track the improvement of a model over time, it is
            recommended to use a numeric value for this field.

            A string value can be used if no ordering is desired.
    """

    label: str
    value: Union[str, int, bool]


class CategoricalQuestion(BaseModel):
    """
    A categorical question.

    This is only used in a StudioEvaluationConfig to specify a question that will be asked to
    users when they are evaluating generated outputs in the EGP annotation UI.

    Attributes:
        question_id: A unique id for this question. Each question_id will be represented as a
            key in the `result` field in the TestCaseResult after an annotation is completed.
            When examining how an application has performed on a specific question, users should
            look at the `result` field in the TestCaseResult for the key with the
            corresponding id.
        question_type: The type of the question.
        title: The text displayed to annotators for this question.
        choices: The choices for the question.
    """

    question_id: str
    question_type: Literal[QuestionType.CATEGORICAL] = QuestionType.CATEGORICAL.value
    title: str
    choices: List[CategoricalChoice]


Question = CategoricalQuestion


class StudioEvaluationConfig(BaseModel):
    """
    This specifies the configuration for a studio evaluation job.

    Users should use this evaluation config if they intend to do human evaluation through
    [Studio](https://scale.com/studio).

    Attributes:
        evaluation_type: The type of the evaluation.
        studio_project_id: The ID of the Studio project to use for the evaluation.
        questions: The questions to ask users when they are evaluating generated outputs in the
            EGP annotation UI.
    """

    evaluation_type: EvaluationType = EvaluationType.STUDIO
    studio_project_id: str
    questions: List[Question]


EvaluationConfig = StudioEvaluationConfig


class EvaluationDatasetVersion(Entity):
    num: int
    evaluation_dataset_id: str
    id: str
    created_at: datetime
    account_id: str
    created_by_user_id: str


class ExtraInfo(BaseModel):
    """
    A data model representing the extra info of a generation model.

    Attributes:
        schema_type: The schema type of the extra info
        info: The content of the extra info. This must match the schema type.
    """

    schema_type: ExtraInfoSchema
    info: str

    @validator("info")
    def info_matches_schema_type(cls, info, values):
        schema_type = values.get("schema_type")
        if schema_type == ExtraInfoSchema.STRING:
            if not isinstance(info, str):
                raise ValueError("schema_type STRING requires info to be a string")
        else:
            raise ValueError(f"Unknown schema_type: {schema_type}")
        return info


class GenerationTestCaseData(BaseModel):
    """
    A data model representing the data of a Testcase with a GENERATION schema type.

    Attributes:
        input: The input to the generation model
        expected_output: The expected output of the generation model
        expected_extra_info: The expected extra info of the generation model
    """

    input: str
    expected_output: Optional[str] = ""
    expected_extra_info: Optional[ExtraInfo] = ExtraInfo(
        schema_type=ExtraInfoSchema.STRING,
        info="",
    )


TestCaseData: TypeAlias = GenerationTestCaseData


class GenerationTestCaseResultData(BaseModel):
    """
    A data model representing the data of a TestcaseResult with a GENERATION schema type.

    Attributes:
        generation_output: The output of the generation model
        generation_extra_info: The extra info of the generation model
    """

    generation_output: str
    generation_extra_info: Optional[ExtraInfo] = None


TestCaseResultData: TypeAlias = GenerationTestCaseResultData


class CompletionContent(BaseModel):
    """
    A data model representing the completion text and the finish reason.

    Attributes:
        text: Completion text. If streaming, this field will contain each packet of text.
        finish_reason: Reason the LLM finished generating text.
    """

    text: str
    finish_reason: Optional[str] = None


class TokenUsage(BaseModel):
    """
    A data model representing LLM token usage numbers.

    Attributes:
        prompt: Number of tokens in the prompt.
        completion: Number of tokens in the completion.
        total: Total number of tokens in both the prompt and the completion.
    """

    prompt: Optional[int] = None
    completion: Optional[int] = None
    total: int


class Completion(BaseModel):
    """
    A data model representing a completion.

    Attributes:
        completion: The actual completion text and the finish reason.
        token_usage: Token usage numbers. If streaming, this field is null until the stream
            completes, at which point it will be populated (if supported).
    """

    completion: CompletionContent
    token_usage: Optional[TokenUsage] = None


class ModelParameters(BaseModel):
    """
    A data model representing the configuration parameters for the completion model.

    Attributes:
        temperature: What sampling temperature to use, between [0, 1]. Higher values like 0.8
            will make the output more random, while lower values like 0.2 will make it more
            focused and deterministic. Setting temperature=0.0 will enable fully deterministic
            (greedy) sampling.
        stop_sequences: List of up to 4 sequences where the API will stop generating further
            tokens. The returned text will not contain the stop sequence.
        max_tokens: The maximum number of tokens to generate in the completion. The token count
            of your prompt plus max_tokens cannot exceed the model's context length. If not,
            specified, max_tokens will be determined based on the model used:
            | Model API family | Model API default | EGP applied default |
            | --- | --- | --- |
            | OpenAI Completions | [`16`](
            https://platform.openai.com/docs/api-reference/completions/create#max_tokens) |
            `context window - prompt size` |
            | OpenAI Chat Completions | [`context window - prompt size`](
            https://platform.openai.com/docs/api-reference/chat/create#max_tokens) | `context
            window - prompt size` |
    """

    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    stop_sequences: Optional[List[str]] = Field(default=None, max_items=4)
    max_tokens: Optional[int] = Field(default=None)


class ChunkToUpload(BaseModel):
    """
    A data model representing a local chunk.

    Attributes:
        text: The text associated with the chunk
        chunk_position: The position of the chunk in the artifact
        metadata: Any additional key value pairs of information stored with the chunk
    """

    text: str
    chunk_position: int
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CrossEncoderRankParams(BaseModel):
    cross_encoder_model: Literal[
        "cross-encoder/ms-marco-MiniLM-L-12-v2",
        "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",
    ] = Field(
        default=CrossEncoderModelName.CROSS_ENCODER_MS_MARCO_MINILM_L12_V2,
        description="Cross encoder model to use when ranking.",
    )


class CrossEncoderRankStrategy(BaseModel):
    method: Literal["cross_encoder"] = Field(
        default="cross_encoder",
        const=True,
        description="The name of the rank strategy. Must be `cross_encoder`.",
    )
    params: CrossEncoderRankParams = Field(
        default=CrossEncoderRankParams(),
        description="The parameters needed for ranking.",
    )


class RougeRankParams(BaseModel):
    metric: str = Field(
        default="rouge2",
        description="Rouge type, can be n-gram based (e.g. rouge1, rouge2) or longest common "
        "subsequence (rougeL or rougeLsum)",
    )
    score: Literal["precision", "recall", "fmeasure"] = Field(
        default="recall", description="Metric to use from Rouge score"
    )


class RougeRankStrategy(BaseModel):
    method: Literal["rouge"] = Field(
        default="rouge",
        const=True,
        description="The name of the rank strategy.",
    )
    params: RougeRankParams = Field(
        default=RougeRankParams(),
        description="The parameters needed for ranking.",
    )
