"""
This module contains the models for the agents.
"""

from enum import Enum


class DialogStatus(str, Enum):
    """
    Dialogue status based on the context of the discussion.
    """

    DIALOG = "dialog"
    OFFER = "offer"

    def __str__(self) -> str:
        return str.__str__(self)
