from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional, Dict, Union, Literal

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from pydantic import (
    Field,
    validator,
    ValidationError,
)

from scale_egp.sdk.enums import (
    TestCaseSchemaType,
    EvaluationStatus,
    ArtifactSource,
    UploadJobStatus,
)
from scale_egp.sdk.models.sub import (
    EmbeddingConfig,
    ChunksStatus,
    EvaluationConfig,
    TestCaseData,
    GenerationTestCaseResultData,
    S3DataSourceConfig,
    SharePointDataSourceConfig,
    GoogleDriveDataSourceConfig,
    LocalChunksSourceConfig,
    CharacterChunkingStrategyConfig,
    CrossEncoderRankStrategy,
    RougeRankStrategy,
    ArtifactsStatus,
    GenerationTestCaseData,
    ModelParameters,
    SharePointDataSourceAuthConfig,
    ChunkToUpload,
)
from scale_egp.utils.model_utils import (
    BaseModel,
    Entity,
    RootModel,
)

DataSourceConfig = Annotated[
    Union[
        S3DataSourceConfig,
        SharePointDataSourceConfig,
        GoogleDriveDataSourceConfig,
        LocalChunksSourceConfig,
    ],
    Field(
        discriminator="source",
        description="Configuration for the data source which describes where to find the data.",
    ),
]


class KnowledgeBase(Entity):
    """
    A data model representing a knowledge base.

    Attributes:
        knowledge_base_id: The unique ID of the knowledge base
        knowledge_base_name: The name of the knowledge base
        embedding_config: The embedding configuration
        metadata: Metadata associated with the knowledge base
        created_at: The timestamp at which the knowledge base was created
        updated_at: The timestamp at which the knowledge base was last updated
    """

    knowledge_base_id: str
    knowledge_base_name: str
    embedding_config: EmbeddingConfig
    metadata: Optional[Dict[str, Any]]
    created_at: str
    updated_at: Optional[str]


class KnowledgeBaseArtifact(BaseModel):
    """
    A data model representing an artifact in a knowledge base.

    Attributes:
        artifact_id: Unique identifier for the artifact
        artifact_name: Friendly name for the artifact
        artifact_uri: Location (e.g. URI) of the artifact in the data source
        artifact_uri_public: Public Location (e.g. URI) of the artifact in the data source
        status: Status of the artifact
        status_reason: Reason for the artifact's status
        source: Data source of the artifact
        chunks_status: Number of chunks pending, completed, and failed
        updated_at: Timestamp at which the artifact was last updated
        chunks: List of chunks associated with the artifact
    """

    artifact_id: str
    artifact_name: str
    artifact_uri: str
    artifact_uri_public: Optional[str] = None
    status: str
    status_reason: Optional[str]
    source: ArtifactSource
    chunks_status: ChunksStatus
    updated_at: Optional[datetime] = None
    chunks: Optional[List[Chunk]] = None


class Chunk(BaseModel):
    """
    A data model representing a chunk.

    Attributes:
        chunk_id: The unique ID of the chunk
        text: The text associated with the chunk
        score: A number between 0 and 1 representing how similar a chunk's embedding is to the
            query embedding. Higher numbers mean that this chunk is more similar.
        embedding: The vector embedding of the text associated with the chunk
        metadata: Any additional key value pairs of information stored with the chunk
    """

    chunk_id: str
    text: str
    score: Optional[float]
    embedding: Optional[List[float]]
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class KnowledgeBaseUpload(BaseModel):
    """
    A data model representing a knowledge base upload.

    Attributes:
        upload_id: Unique ID of the upload job
        data_source_config: Configuration for downloading data from source
        chunking_strategy_config: Configuration for chunking the text content of each artifact
        created_at: The timestamp at which the upload job started
        updated_at: The timestamp at which the upload job was last updated
        status: Sync status
        status_reason: Reason for the upload job's status
        artifacts_status: Number of artifacts pending, completed, and failed
        artifacts: List of info for each artifacts
    """

    upload_id: str
    data_source_config: DataSourceConfig
    chunking_strategy_config: Optional[Union[CharacterChunkingStrategyConfig]]
    created_at: str
    updated_at: str
    status: UploadJobStatus
    status_reason: Optional[str] = None
    artifacts_status: Optional[ArtifactsStatus]
    artifacts: Optional[List[KnowledgeBaseArtifact]]


class ApplicationSpec(Entity):
    """
    A data model representing an Application Spec.

    Attributes:
        id: The ID of the application spec
        name: The name of the application
        description: The description of the application

    """

    id: str
    name: str
    description: str


class StudioProject(Entity):
    """
    A data model representing a Studio project.

    Attributes:
        id: The ID of the Studio project
        name: The name of the Studio project
        description: The description of the Studio project
        created_at: The time the Studio project was created
    """

    id: str
    name: str
    description: str
    created_at: datetime


class EvaluationDataset(Entity):
    """
    A data model representing an evaluation dataset.

    Attributes:
        name: The name of the evaluation dataset
        schema_type: The schema type of the evaluation dataset
        id: The ID of the evaluation dataset
        created_at: The time the evaluation dataset was created
        updated_at: The time the evaluation dataset was last updated
        account_id: The ID of the account that owns the evaluation dataset
        created_by_user_id: The ID of the user that created the evaluation dataset
        version_num: The version number of the evaluation dataset

    """

    name: str
    schema_type: TestCaseSchemaType
    id: str
    created_at: datetime
    updated_at: datetime
    account_id: str
    created_by_user_id: str
    version_num: Optional[int] = None


class TestCase(Entity):
    """
    A data model representing a test case.

    Attributes:
        id: The ID of the test case
        evaluation_dataset_id: The ID of the evaluation dataset that the test case belongs to
        schema_type: The schema type of the test case
        test_case_data: The data of the test case. In general, this can be thought of as the
            data to evaluate an application against.
    """

    id: str
    evaluation_dataset_id: str
    schema_type: TestCaseSchemaType
    test_case_data: TestCaseData


class Evaluation(Entity):
    """
    A data model representing an evaluation.

    Attributes:
        id: The ID of the evaluation
        name: The name of the evaluation
        description: The description of the evaluation
        status: The status of the evaluation
        application_spec_id: The ID of the application spec that the evaluation is for
        evaluation_config: The evaluation config of the evaluation
        tags: The tags of the evaluation represented as a dictionary of key value pairs
        created_at: The time the evaluation was created
    """

    id: str
    name: str
    description: str
    status: EvaluationStatus
    application_spec_id: str
    evaluation_config: EvaluationConfig
    tags: Optional[Dict[str, Any]] = None
    created_at: datetime


class TestCaseResult(Entity):
    """
    A data model representing a test case result.

    Attributes:
        id: The ID of the test case result
        status: The status of the test case result
        application_spec_id: The ID of the application spec that the test case result is for
        evaluation_id: The ID of the evaluation that the test case result is for
        evaluation_dataset_id: The ID of the evaluation dataset that the test case result is for
        evaluation_dataset_version_num: The version number of the evaluation dataset that the
            test case result is for
        test_case_id: The ID of the test case that the test case result is for
        test_case_evaluation_data: A payload representing the data generated by the application
            described by the application spec when evaluated against the test case.
        test_case_evaluation_data_schema: The schema type of the `test_case_evaluation_data`
        result: The payload filled in when the evaluation of this test case result is completed.
            Examine this value to determine how the application performed on the test case.
        completed_at: The time the test case result was completed
        created_at: The time the test case result was created
    """

    id: str
    status: EvaluationStatus
    application_spec_id: str
    evaluation_id: str
    evaluation_dataset_id: str
    evaluation_dataset_version_num: str
    test_case_id: str
    test_case_evaluation_data: GenerationTestCaseResultData
    test_case_evaluation_data_schema: TestCaseSchemaType
    created_at: datetime
    result: Optional[Dict[str, Any]] = None
    completed_at: Optional[datetime] = None


# Update forward refs. We put data models out of order so it looks better in mkdocs.
KnowledgeBaseArtifact.update_forward_refs()


# KnowledgeBase.update_forward_refs()
# EmbeddingConfig.update_forward_refs()
# ApplicationSpec.update_forward_refs()
# StudioProject.update_forward_refs()
# EvaluationDataset.update_forward_refs()
# TestCase.update_forward_refs()
# Evaluation.update_forward_refs()
# TestCaseResult.update_forward_refs()
# EvaluationDatasetVersion.update_forward_refs()
# StudioEvaluationConfig.update_forward_refs()
# CategoricalQuestion.update_forward_refs()
# CategoricalChoice.update_forward_refs()
# GenerationTestCaseData.update_forward_refs()
# GenerationTestCaseResultData.update_forward_refs()
# ExtraInfo.update_forward_refs()
# Completion.update_forward_refs()
# CompletionContent.update_forward_refs()
# TokenUsage.update_forward_refs()
# ModelParameters.update_forward_refs()
class EvaluationDatasetRequest(BaseModel):
    name: str
    schema_type: TestCaseSchemaType
    account_id: Optional[str] = Field(
        description="Account to create knowledge base in. If you have access to more than one "
        "account, you must specify an account_id"
    )


class EvaluationDatasetVersionRequest(BaseModel):
    account_id: str = Field(..., description="The ID of the account that owns the given entity.")


class StudioProjectRequest(BaseModel):
    name: str
    description: str
    studio_api_key: str
    account_id: Optional[str] = Field(
        description="Account to create knowledge base in. If you have access to more than one "
        "account, you must specify an account_id"
    )


class ApplicationSpecRequest(BaseModel):
    name: str
    description: str
    account_id: Optional[str] = Field(
        description="Account to create application spec in. If you have access to more than one "
        "account, you must specify an account_id"
    )


class EvaluationRequest(BaseModel):
    name: str
    description: str
    application_spec_id: str
    tags: Optional[Dict[str, Any]] = None
    evaluation_config: EvaluationConfig
    account_id: Optional[str] = Field(
        description="Account to create knowledge base in. If you have access to more than one "
        "account, you must specify an account_id"
    )


class TestCaseRequest(BaseModel):
    schema_type: TestCaseSchemaType
    test_case_data: TestCaseData
    account_id: Optional[str] = Field(
        description="Account to create knowledge base in. If you have access to more than one "
        "account, you must specify an account_id"
    )

    @validator("test_case_data")
    @classmethod
    def test_case_data_matches_schema_type(cls, test_case_data, values):
        schema_type = values.get("schema_type")
        TestCaseSchemaValidator.validate(schema_type, test_case_data)
        return test_case_data


class TestCaseResultRequest(BaseModel):
    application_spec_id: str
    evaluation_dataset_version_num: int
    test_case_id: str
    test_case_evaluation_data_schema: TestCaseSchemaType
    test_case_evaluation_data: GenerationTestCaseResultData
    result: Optional[Dict[str, Any]] = Field(default_factory=dict)
    account_id: Optional[str] = Field(
        description="Account to create knowledge base in. If you have access to more than one "
        "account, you must specify an account_id"
    )

    @validator("test_case_evaluation_data")
    @classmethod
    def test_case_evaluation_data_matches_schema_type(cls, test_case_evaluation_data, values):
        schema_type = values.get("test_case_evaluation_data_schema")
        TestCaseResultSchemaValidator.validate(schema_type, test_case_evaluation_data)
        return test_case_evaluation_data


class TestCaseSchemaValidator:
    TEST_CASE_SCHEMA_TO_DATA_TYPE = {
        TestCaseSchemaType.GENERATION: GenerationTestCaseData,
    }

    @classmethod
    def validate(cls, schema_type: TestCaseSchemaType, data: Dict[str, Any]):
        try:
            model = cls.TEST_CASE_SCHEMA_TO_DATA_TYPE[schema_type]
            model.from_dict(data)
        except ValidationError as e:
            raise ValueError(f"Test case data does not match schema type {schema_type}") from e

    @classmethod
    def get_model(cls, schema_type: TestCaseSchemaType):
        return cls.TEST_CASE_SCHEMA_TO_DATA_TYPE[schema_type]

    @classmethod
    def dict_to_model(cls, schema_type: TestCaseSchemaType, data: Dict[str, Any]):
        return cls.TEST_CASE_SCHEMA_TO_DATA_TYPE[schema_type].from_dict(data)


class TestCaseResultSchemaValidator:
    TEST_CASE_RESULT_SCHEMA_TO_DATA_TYPE = {
        TestCaseSchemaType.GENERATION: GenerationTestCaseResultData,
    }

    @classmethod
    def validate(cls, schema_type: TestCaseSchemaType, data: Dict[str, Any]):
        try:
            model = cls.TEST_CASE_RESULT_SCHEMA_TO_DATA_TYPE[schema_type]
            model.from_dict(data)
        except ValidationError as e:
            raise ValueError(
                f"Test case result data does not match schema type {schema_type}"
            ) from e

    @classmethod
    def get_model(cls, schema_type: TestCaseSchemaType):
        return cls.TEST_CASE_RESULT_SCHEMA_TO_DATA_TYPE[schema_type]

    @classmethod
    def dict_to_model(cls, schema_type: TestCaseSchemaType, data: Dict[str, Any]):
        return cls.TEST_CASE_RESULT_SCHEMA_TO_DATA_TYPE[schema_type].from_dict(data)


class CompletionRequest(BaseModel):
    model: Literal[
        "gpt-4",
        "gpt-4-0613",
        "gpt-4-32k",
        "gpt-4-32k-0613",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-16k-0613",
        "text-davinci-003",
        "text-davinci-002",
        "text-curie-001",
        "text-babbage-001",
        "text-ada-001",
    ] = Field(
        ...,
        description="The ID of the model to use for completions.\n\n"
        "Users have two options:\n"
        "- Option 1: Use one of the supported models from the dropdown.\n"
        "- Option 2: Enter the ID of a custom model.\n\n"
        "Note: For custom models we currently only support models finetuned using "
        "using the Scale-hosted LLM-Engine API.",
    )
    prompt: str = Field(
        ...,
        description="Prompt for which to generate the completion.\n\n"
        "Good prompt engineering is crucial to getting performant results from the "
        "model. If you are having trouble getting the model to perform well, "
        "try writing a more specific prompt here before trying more expensive "
        "techniques such as swapping in other models or finetuning the underlying LLM.",
    )
    model_parameters: Optional[ModelParameters] = Field(
        default=ModelParameters(temperature=0.2),
        description="Configuration parameters for the completion model, such as temperature, "
        "max_tokens, and stop_sequences.\n\n"
        "If not specified, the default value are:\n"
        "- temperature: 0.2\n"
        "- max_tokens: None (limited by the model's max tokens)\n"
        "- stop_sequences: None",
    )
    stream: bool = Field(
        default=False,
        description="Whether or not to stream the response.\n\n"
        "Setting this to True will stream the completion in real-time.",
    )


class KnowledgeBaseRequest(BaseModel):
    knowledge_base_name: str = Field(..., description="A unique name for the knowledge base")
    embedding_config: EmbeddingConfig = Field(description="The configuration of the embedding")
    account_id: Optional[str] = Field(
        description="Account to create knowledge base in. If you have access to more than one "
        "account, you must specify an account_id"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        description="Metadata associated with the knowledge base"
    )


class KnowledgeBaseResponse(BaseModel):
    knowledge_base_id: str = Field(..., description="The unique ID of the created knowledge base")


class ListKnowledgeBasesResponse(BaseModel):
    items: List[KnowledgeBase] = Field(
        description="A list of the names and IDs, embedding configurations, metadata, created and "
        "updated dates of your knowledge bases"
    )


class ListKnowledgeBaseArtifactsResponse(BaseModel):
    artifacts: List[KnowledgeBaseArtifact] = Field(..., description="List of artifacts.")


class KnowledgeBaseChunksRequest(BaseModel):
    chunk_id: Optional[str] = Field(None, description="Optional search by chunk_id")
    metadata_filters: Optional[Dict[str, Any]] = Field(
        None, description="Optional search by metadata fields"
    )


class KnowledgeBaseChunksResponse(BaseModel):
    chunks: List[Chunk] = Field(
        ..., description="List of chunks that match the chunk_id and metadata filters"
    )


class KnowledgeBaseQueryRequest(BaseModel):
    query: str = Field(
        description="The natural language query to be answered by referencing the data ingested "
        "into the knowledge base"
    )
    top_k: int = Field(
        gt=0,
        description="Number of chunks to return. Must be greater than 0 if specified. If not "
        "specified, all chunks will be returned.",
    )
    include_embeddings: bool = Field(
        default=True,
        description="Whether or not to include the embeddings for each chunk",
    )
    metadata_filters: Optional[Dict[str, Any]] = Field(
        None, description="Optional filter by metadata fields"
    )


class KnowledgeBaseQueryResponse(BaseModel):
    chunks: List[Chunk] = Field(
        description="An ordered list of the k most similar chunks and their similarity scores "
        "from most to least similar"
    )


class KnowledgeBaseChunksResponse(BaseModel):
    chunks: List[Chunk] = Field(
        description="A list of chunks that match the chunk_id and metadata filters"
    )


class KnowledgeBaseRemoteUploadRequest(BaseModel):
    upload_type: Literal["remote"] = "remote"
    data_source_config: DataSourceConfig
    data_source_auth_config: Optional[SharePointDataSourceAuthConfig] = Field(
        None,
        description="Configuration for the data source which describes how to "
        "authenticate to the data source.",
    )
    chunking_strategy_config: CharacterChunkingStrategyConfig = Field(
        None,
        description="Configuration for the chunking strategy which describes how to chunk the "
        "data.",
    )


class KnowledgeBaseLocalChunkUploadRequest(BaseModel):
    upload_type: Literal["local_chunks"] = "local_chunks"
    data_source_config: LocalChunksSourceConfig = Field(
        ...,
        description="Configuration for the data source which describes where to find the data.",
    )
    chunks: List[ChunkToUpload] = Field(..., description="List of chunks.")


class KnowledgeBaseUploadRequest(RootModel):
    __root__: Union[
        KnowledgeBaseRemoteUploadRequest,
        KnowledgeBaseLocalChunkUploadRequest,
    ] = Field(
        ...,
        discriminator="upload_type",
    )


class KnowledgeBaseUploadResponse(BaseModel):
    upload_id: str = Field(..., description="ID of the created knowledge base upload job.")


class ListKnowledgeBaseUploadsResponse(BaseModel):
    uploads: List[KnowledgeBaseUpload] = Field(..., description="List of knowledge base uploads.")


class CancelKnowledgeBaseUploadResponse(BaseModel):
    upload_id: str = Field(
        ..., description="ID of the knowledge base upload job that was cancelled."
    )
    canceled: bool = Field(..., description="Whether cancellation was successful.")


class ChunkRankRequest(BaseModel):
    query: str = Field(
        ...,
        description="Natural language query to re-rank chunks against. If a vector store query "
        "was originally used to retrieve these chunks, please use the same query for "
        "this ranking",
    )
    relevant_chunks: List[Chunk] = Field(..., description="List of chunks to rank")
    rank_strategy: Union[CrossEncoderRankStrategy, RougeRankStrategy] = Field(
        ...,
        discriminator="method",
        description="The ranking strategy to use.\n\n"
        "Rank strategies determine how the ranking is done, They consist of the "
        "ranking method name and additional params needed to compute the ranking.\n\n"
        "So far, only the `cross_encoder` rank strategy is supported. We plan to "
        "support more rank strategies soon.",
    )
    top_k: Optional[int] = Field(
        gt=0,
        description="Number of chunks to return. Must be greater than 0 if specified. If not "
        "specified, all chunks will be returned.",
    )


class ChunkRankResponse(BaseModel):
    relevant_chunks: List[Chunk] = Field(
        ..., description="List of chunks ranked by the requested rank strategy"
    )


class ChunkSynthesisRequest(BaseModel):
    query: str = Field(
        ...,
        description="Natural language query to resolve using the supplied chunks.",
    )
    chunks: List[Chunk] = Field(
        ..., description="List of chunks to use to synthesize the response."
    )


class ChunkSynthesisResponse(BaseModel):
    response: str = Field(..., description="Natural language response addressing the query.")
    metadata: Optional[Dict[str, Dict]] = Field(
        None, description="Optional metadata present on each chunk."
    )
