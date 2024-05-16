"""
This module contains the ConsultantAgent class.
"""

from typing import AsyncGenerator

from chat_buy.agents.base_agent import BaseAgent


class ConsultantAgent(BaseAgent):
    """
    An agent providing advice to the user.
    """

    async def advise_user(self, messages: list) -> AsyncGenerator[str, None]:
        """
        Asynchronously provides advice to the user based on his messages.

        Args:
            messages (list): List of messages.

        Yields:
            Iterator[AsyncGenerator[str, None]]: A generator that yields the response.
        """
        context_msgs = [{"role": "system", "content": self.prompt}] + messages[:]
        async for part in self.openai_client.get_stream_response(
            model=self.model,
            temperature=self.temperature,
            context_messages=context_msgs,
        ):
            yield part
