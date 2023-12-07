from enum import Enum


class TestCaseSchemaType(str, Enum):
    """
    An enum representing the different test case schema types.

    Attributes:
        GENERATION: If a TestCase specifies this schema type, it must have the following fields:

            - `input` [Required] The input to the generation model.
            - `expected_output` [Optional] The expected output of the generation model.
            - `expected_extra_info` [Optional] The expected extra info of the generation model.

            If a TestCaseResult specifies this schema type, it must have the following fields:

            - `generation_output` [Required] The output of the generation model.
            - `generation_extra_info` [Required] The extra info of the generation model.
    """

    GENERATION: str = "GENERATION"


class EvaluationStatus(str, Enum):
    """
    An enum representing the differ possible statuses of an Evaluation.

    Attributes:
        PENDING: Denotes that an evaluation is pending.
        COMPLETED: Denotes that an evaluation is completed.
        FAILED: Denotes that an evaluation has failed.
    """

    PENDING: str = "PENDING"
    COMPLETED: str = "COMPLETED"
    FAILED: str = "FAILED"


class EvaluationType(str, Enum):
    """
    An enum representing the different types of evaluations.

    Currently only studio evaluations are supported.

    Attributes:
        STUDIO: Denotes that an evaluation is a studio evaluation.
    """

    STUDIO: str = "studio"


class QuestionType(str, Enum):
    """
    An enum representing the different types of questions.

    This is only used in a StudioEvaluationConfig to specify the type of a question.

    Currently only categorical questions are supported.

    Attributes:
        CATEGORICAL: Denotes that a question is a categorical question.
    """

    CATEGORICAL: str = "categorical"


class ExtraInfoSchema(str, Enum):
    """
    An enum representing the different types of extra info schemas.

    Denotes the type of the "info" field in the ExtraInfo model.

    Attributes:
        STRING: Denotes that the "info" field is a string.
    """

    STRING: str = "STRING"


class EmbeddingModelName(str, Enum):
    """
    An enum representing the different types of embedding models supported.

    Attributes:
        SENTENCE_TRANSFORMERS_ALL_MINILM_L12_V2:
            Denotes that the model is a sentence transformer model.
        SENTENCE_TRANSFORMERS_MULTI_QA_DISTILBERT_COS_V1:
            Denotes that the model is a sentence transformer model.
        SENTENCE_TRANSFORMERS_PARAPHRASE_MULTILINGUAL_MPBET_BASE_V2:
            Denotes that the model is a sentence transformer model.
        OPENAI_TEXT_EMBEDDING_ADA_002:
            Denotes that the model is an openai text embedding model.
    """

    SENTENCE_TRANSFORMERS_ALL_MINILM_L12_V2 = "sentence-transformers/all-MiniLM-L12-v2"
    SENTENCE_TRANSFORMERS_MULTI_QA_DISTILBERT_COS_V1 = (
        "sentence-transformers/multi-qa-distilbert-cos-v1"
    )
    SENTENCE_TRANSFORMERS_PARAPHRASE_MULTILINGUAL_MPBET_BASE_V2 = (
        "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    )
    OPENAI_TEXT_EMBEDDING_ADA_002 = "openai/text-embedding-ada-002"


class DataSource(str, Enum):
    """
    An enum representing the different types of data sources supported.

    Attributes:
        S3: Denotes that the data source is S3.
    """

    S3: str = "S3"
    SHAREPOINT: str = "SharePoint"
    GOOGLE_DRIVE: str = "GoogleDrive"
    LOCAL_CHUNKS: str = "LocalChunks"


class DeduplicationStrategy(str, Enum):
    OVERWRITE = "Overwrite"
    FAIL = "Fail"


class ChunkingStrategy(str, Enum):
    CHARACTER = "character"


class ArtifactSource(str, Enum):
    S3 = "S3"
    CONFLUENCE = "Confluence"
    SHAREPOINT = "SharePoint"
    GOOGLE_DRIVE = "GoogleDrive"
    LOCAL_FILE = "LocalFile"
    LOCAL_CHUNKS = "LocalChunks"


class StatusType(str, Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELED = "Canceled"
    CHUNKING = "Chunking"
    DELETING = "Deleting"
    UPLOADING = "Uploading"


class UploadJobStatus(str, Enum):
    RUNNING = StatusType.RUNNING.value
    COMPLETED = StatusType.COMPLETED.value
    FAILED = StatusType.FAILED.value
    CANCELED = StatusType.CANCELED.value


class ChunkUploadStatus(str, Enum):
    PENDING = StatusType.PENDING.value
    COMPLETED = StatusType.COMPLETED.value
    FAILED = StatusType.FAILED.value


class CrossEncoderModelName(str, Enum):
    CROSS_ENCODER_MS_MARCO_MINILM_L12_V2 = "cross-encoder/ms-marco-MiniLM-L-12-v2"
    CROSS_ENCODER_MMARCO_MMINILMV2_L12_H384_V1 = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
