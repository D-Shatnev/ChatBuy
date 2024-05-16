"""
This module contains the client for the OpenAI API.
"""

from typing import AsyncGenerator
import openai

from chat_buy.api.constants import LOG_LEVEL
from chat_buy.api.utils import get_logger

logger = get_logger("openai_client", level=LOG_LEVEL)


class OpenAIClient:
    """
    Client for the OpenAI API.
    Provides methods for interacting with the API.
    """

    def __init__(self, api_key: str, api_base: str) -> None:
        openai.api_key = api_key
        openai.api_base = api_base

    async def get_stream_response(
        self, model: str, temperature: float, context_messages: list
    ) -> AsyncGenerator[str, None, None]:
        """
        Asynchronously retrieves a response from a chat stream.

        Args:
            model (str): The name of the model to use.
            temperature (float): The temperature to use.
            context_messages (list): A list of chat messages as context.

        Returns:
            AsyncGenerator[str, None, None]: A generator that yields the response.
        """
        try:
            response_generator = await openai.ChatCompletion.acreate(
                model=model,
                messages=context_messages,
                temperature=temperature,
                stream=True,
            )
            response = ""
            async for response_item in response_generator:
                delta = response_item.choices[0].delta
                if "content" in delta:
                    response += delta.content
                    yield response
        except Exception as error:
            yield str(error)
            return
        response = response.strip()
        yield response
