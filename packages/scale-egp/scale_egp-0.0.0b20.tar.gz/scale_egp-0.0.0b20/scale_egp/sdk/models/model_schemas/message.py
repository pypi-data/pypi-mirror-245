from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field


class ToolRequest(BaseModel):
    name: str  # Name of the tool
    arguments: str  # Arguments (JSON serializable string) to pass to the tool


class AgentMessage(BaseModel):
    role: Literal["agent"] = "agent"
    content: Optional[str] = None  # Output of the agent if finished
    tool_request: Optional[ToolRequest] = None  # Request to run a tool


class ToolMessage(BaseModel):
    role: Literal["tool"] = "tool"
    name: str  # Name of the tool
    content: str  # Output of calling the tool (JSON serialized to string)


class UserMessage(BaseModel):
    role: Literal["user"] = "user"
    content: str


class AssistantMessage(BaseModel):
    role: Literal["assistant"] = "assistant"
    content: str


class SystemMessage(BaseModel):
    role: Literal["system"] = "system"
    content: str


Message = Annotated[
    Union[UserMessage, ToolMessage, AgentMessage, SystemMessage], Field(discriminator="role")
]
