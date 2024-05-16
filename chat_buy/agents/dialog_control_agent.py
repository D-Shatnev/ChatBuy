"""
This module contains the DialogControlAgent class.
"""

from chat_buy.agents.base_agent import BaseAgent
from chat_buy.agents.models import DialogStatus
from chat_buy.constants import API_BASE, API_KEY
from chat_buy.openai.openai_client import OpenAIClient


class DialogControlAgent(BaseAgent):
    """
    An agent controlling the process of dialog with the user.
    """

    def __init__(self) -> None:
        super().__init__()
        self.openai_client = OpenAIClient(api_base=API_BASE, api_key=API_KEY)

    async def check_dialog_or_offer(self, messages: list) -> DialogStatus:
        """
        Asynchronously checks the dialog or offer status.

        Args:
            messages (list): List of messages.

        Returns:
            DialogStatus: The dialog or offer status.
        """
        full_response = []
        async for part in self.openai_client.get_stream_response(
            model=self.model,
            temperature=self.temperature,
            context_messages=messages,
        ):
            full_response.append(part)
            if "<start_search> " in part.lower():
                return "offer"
        full_response = "".join(full_response)
        return DialogStatus.OFFER if "<start_search> " in full_response.lower() else DialogStatus.DIALOG
