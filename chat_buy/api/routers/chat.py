"""
This module contains endpoints for chat processing.
"""

from typing import List

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from chat_buy.agents import consultant_agent, dialog_control_agent, search_query_agent
from chat_buy.agents.models import DialogStatus
from chat_buy.api.models import Message

chat_router = APIRouter()


@chat_router.post("/v1/chat/")
async def process_messages(messages: List[Message]) -> StreamingResponse:
    """
    Processes a list of messages and streams back a response.
    """
    action = None
    response_agent_name = None
    messages = [message.model_dump() for message in messages]

    match await dialog_control_agent.check_dialog_or_offer(messages):
        case DialogStatus.DIALOG:
            response_agent_name = consultant_agent.__class__.__name__
            action = consultant_agent.advise_user
        case DialogStatus.OFFER:
            response_agent_name = search_query_agent.__class__.__name__
            action = search_query_agent.offer_products

    return StreamingResponse(
        action(messages),
        media_type="text/event-stream",
        headers={"Response-Agent": response_agent_name},
    )
