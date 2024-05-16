"""
This module contains the schemas for the API.
The schemas are used to validate the input and output data for the API.
"""

from enum import Enum

from pydantic import BaseModel, Field


class Roles(str, Enum):
    """
    Enum class for roles, they indicate who the message is coming from.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    def __str__(self) -> str:
        return str.__str__(self)


class Message(BaseModel):
    """
    This model represent user message.
    """

    role: Roles
    content: str = Field(..., min_length=1, max_length=3000, description="Text of the message.")
