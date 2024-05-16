"""
This module contains the interfaces for the shared modules.
"""

from chat_buy.api.routers.chat import chat_router
from chat_buy.api.routers.provision import provision_router

__all__ = [
    "chat_router",
    "provision_router",
]
