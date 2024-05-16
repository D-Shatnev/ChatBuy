"""
This module contains the DialogControlAgent class.
"""

from chat_buy.agents.base_agent import BaseAgent
from chat_buy.agents.models import DialogStatus


class DialogControlAgent(BaseAgent):
    """
    An agent controlling the process of dialog with the user.
    """

    async def check_dialog_or_offer(self, messages: list) -> DialogStatus:
        """
        Asynchronously checks the dialog or offer status.

        Args:
            messages (list): List of messages.

        Returns:
            DialogStatus: The dialog or offer status.
        """
        context_msgs = [{"role": "system", "content": self.prompt}] + messages[:]
        full_response = []
        async for part in self.openai_client.get_stream_response(
            model=self.model,
            temperature=self.temperature,
            context_messages=context_msgs,
        ):
            full_response.append(part)
            if "<start_search> " in part.lower():
                return DialogStatus.OFFER
        full_response = "".join(full_response)
        return DialogStatus.OFFER if "<start_search> " in full_response.lower() else DialogStatus.DIALOG
