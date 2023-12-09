import random
import string
from typing import List, Literal, Optional, Type, TypeVar, Union

from pydantic import BaseModel, Extra, Field, create_model
from pydantic.config import BaseConfig

ParameterValueType = Union[str, int, float, bool]


def get_random_string(length=8):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


class ParameterSchemaField(BaseModel):
    name: str
    type: Union[Literal["str"], Literal["int"], Literal["float"], Literal["bool"]]
    description: str
    required: bool  # default is optional


class ParameterSchema(BaseModel):
    parameters: List[ParameterSchemaField]


class ParameterBindings(BaseModel):
    bindings: dict[str, ParameterValueType]

    class Config:
        extra = Extra.forbid


BaseModelT = TypeVar("BaseModelT", bound=BaseModel)


class ParameterSchemaModelConfig(BaseConfig):
    extra = Extra.forbid


def parameter_schema_to_model(
    model_name: str, parameter_schema: ParameterSchema
) -> Type[BaseModelT]:
    """
    Create a Pydantic model from a ParameterSchema
    """
    return create_model(
        model_name,
        __config__=ParameterSchemaModelConfig,
        **{
            field.name: (field.type, ...) if field.required else (field.type, None)
            for field in parameter_schema.parameters
        },
    )


def parse_parameter_bindings(
    parameter_bindings: ParameterBindings,
    parameter_schema: ParameterSchema,
    parameter_schema_name: Optional[str] = None,
) -> BaseModelT:
    model = parameter_schema_to_model(
        parameter_schema_name or get_random_string(), parameter_schema
    )
    return model(**parameter_bindings.bindings)
