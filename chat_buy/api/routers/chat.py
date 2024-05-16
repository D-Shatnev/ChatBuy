"""
This module contains endpoints for chat processing.
"""

from typing import List

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from chat_buy.api.models import Message
from chat_buy.constants import API_BASE, API_KEY
from chat_buy.openai.openai_client import OpenAIClient

chat_router = APIRouter()


@chat_router.post("/v1/chat/")
async def process_messages(messages: List[Message]) -> StreamingResponse:
    """
    Processes a list of messages and streams back a response.
    """
    return StreamingResponse(
        OpenAIClient(api_base=API_BASE, api_key=API_KEY).get_stream_response(
            model="gpt-3.5-turbo", temperature=0.7, context_messages=[message.model_dump() for message in messages]
        ),
        media_type="text/event-stream",
    )
