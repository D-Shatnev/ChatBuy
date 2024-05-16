"""
This module contains the agents interfaces for the ChatBuy project.
"""

from chat_buy.agents.agents import (
    consultant_agent,
    dialog_control_agent,
    search_query_agent,
)

__all__ = [
    "consultant_agent",
    "dialog_control_agent",
    "search_query_agent",
]
