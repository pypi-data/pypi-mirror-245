# copied from packages/egp-api-backend/egp_api_backend/server/api/models/egp_models.py
from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .common import BaseModelRequest, BaseModelResponse
from .memory_strategy import LastKMemoryStrategy
from .message import Message

MemoryStrategy = LastKMemoryStrategy


# Messages
class ToolRequest(BaseModel):
    name: str = Field(..., description="Name of the tool that the AI wants the client to use.")
    arguments: str = Field(
        ...,
        description="Arguments to pass to the tool. The format must be a JSON Schema-compliant "
        "object serialized into a string.",
    )


class ActionContext(BaseModel):
    content: Optional[str] = Field(
        default=None,
        description="The final output of the agent when it no longer needs any tools",
    )
    tool_request: Optional[ToolRequest] = Field(
        default=None,
        description="The tool request if the agent needs more information.",
    )


class ToolPropertyValue(BaseModel):
    type: Literal["string", "number", "integer", "boolean", "object", "array", "null",] = Field(
        ...,
        description="The argument's type.\n\n"
        "The type is used to help the Agent generate valid arguments for the "
        "tool.\n\n"
        "For more information about types, see: "
        "https://json-schema.org/understanding-json-schema/reference/type.html#type"
        "-specific-keywords",
    )
    description: str = Field(
        ...,
        description="Description of what the argument is used for.\n\n"
        "This description is used to help the Agent generate sensible arguments for "
        "the tool. It is very important that this description is succinct, clear, "
        "and accurate.",
    )
    default: Optional[str] = Field(description="A default value for the argument if unspecified.")
    examples: Optional[List[str]] = Field(
        description="Example values demonstrating how the argument should look.\n\n"
        "This can be used to help the agent understand what a valid argument should "
        "look like."
    )

    class Config(BaseModel.Config):
        title = "property"


class ToolArguments(BaseModel):
    type: Literal["object"] = Field(
        ..., description='Type of argument. Currently only "object" is supported'
    )
    properties: dict[str, ToolPropertyValue] = Field(
        default_factory=dict,
        description="An object where each key is the name of a keyword argument and each "
        "value is a schema used to validate that property. Each schema must have a "
        "type and description, but can also have a default value and examples.\n\n"
        "For more information on how to define a valid property, visit "
        "https://json-schema.org/understanding-json-schema/reference/object.html",
    )


class Tool(BaseModel):
    name: str = Field(
        ...,
        description="Name of the tool.\n\n"
        "A tool is a function that the _client application_ has at its disposal. The "
        "tool name is the name the client wishes the Agent to use to refer to this "
        "function when it decides if it wants the user to use the tool or not. It"
        "must be unique amongst the set of tools provided in a single API call.",
        pattern=r"^[a-zA-Z0-9_-]{1,64}$",
    )
    description: str = Field(
        ...,
        description="Description of the tool.\n\n"
        "Because some queries are complex and may require multiple "
        "tools to complete, it is important to make these descriptions as "
        "informative as possible. If a tool is not being chosen when it should, "
        "it is common practice to tune the description of the tool to make it more "
        "apparent to the agent when the tool can be used effectively.",
    )
    arguments: ToolArguments = Field(
        ...,
        description="An JSON Schema-compliant schema for the tool arguments. To describe a "
        'function that accepts no parameters, provide the value `{"type": "'
        '"object", "properties": {}}`.\n\n'
        "For more information on how to define a valid JSON Schema object, visit "
        "https://json-schema.org/understanding-json-schema/reference/object.html",
    )


class ExecuteAgentRequest(BaseModelRequest):
    memory_strategy: Optional[MemoryStrategy] = Field(
        default=None,
        description="The memory strategy to use for the agent. A memory strategy "
        "is a way to prevent the underlying LLM's context limit from being exceeded. "
        "Each memory strategy uses a different technique to condense the input message "
        "list into a smaller payload for the underlying LLM.\n\n"
        "We only support the Last K memory strategy right now, but will be adding new "
        "strategies soon.",
    )
    tools: List[Tool] = Field(
        ...,
        description="The list of specs of tools that the agent can use. Each spec must contain "
        "a `name` key set to the name of the tool, a `description` key set to the "
        "description of the tool, and an `arguments` key set to a JSON Schema "
        "compliant object describing the tool arguments.\n\n"
        "The name and description of each tool is used by the agent to decide when to "
        "use certain tools. Because some queries are complex and may require multiple "
        "tools to complete, it is important to make these descriptions as "
        "informative as possible. If a tool is not being chosen when it should, "
        "it is common practice to tune the description of the tool to make it more "
        "apparent to the agent when the tool can be used effectively.\n\n",
    )
    messages: List[Message] = Field(
        ...,
        description="The list of messages in the conversation.\n\n"
        "Expand each message type to see how it works and when to use it. "
        "Most conversations should begin with a single `user` message.",
    )
    instructions: Optional[str] = Field(
        default="You are an AI assistant that helps users with their questions. You "
        "can answer questions directly or acquire information from any of the "
        "attached tools to assist you. Always answer the user's most recent query to the "
        "best of your knowledge.\n\n"
        "When asked about what tools are available, you must list each attached "
        "tool's name and description. When asked about what you can do, mention "
        "that in addition to your normal capabilities, you can also use the attached "
        "tools by listing their names and descriptions. You cannot use any other tools "
        "other than the ones provided to you explicitly.",
        description="The initial instructions to provide to the agent.\n\nUse this to guide the "
        "agent to act in more specific ways. For example, if you have specific "
        "rules you want to restrict the agent to follow you can specify them here. "
        "For example, if I want the agent to always use certain tools before others, "
        "I can write that rule in these instructions.\n\n"
        "Good prompt engineering is crucial to getting performant results from the "
        "agent. If you are having trouble getting the agent to perform well, "
        "try writing more specific instructions here before trying more expensive "
        "techniques such as swapping in other models or finetuning the underlying LLM.",
    )


class AgentAction(str, Enum):
    TOOL_REQUEST = "tool_request"
    CONTENT = "content"


class ExecuteAgentResponse(BaseModelResponse):
    action: AgentAction = Field(
        ...,
        description="The action that the agent performed.\n\n"
        "The context will contain a key for each action that the agent can perform. "
        "However, only the key corresponding to the action that the agent actually "
        "performed will have a populated value. The rest of the values will be `null`.",
    )
    context: ActionContext = Field(
        ...,
        description="Context object containing the output payload. This will contain a key for all "
        "actions that the agent can perform. However, only the key corresponding to "
        "the action that the agent performed have a populated value. The rest of the "
        "values will be `null`.",
    )
