"""
This module contains the SearchQueryAgent class.
"""

import re
from typing import AsyncGenerator

from chat_buy.agents.base_agent import BaseAgent
from chat_buy.web_parser import WebParser


class SearchQueryAgent(BaseAgent):
    """
    An agent that offers products to the user based on his messages.
    """

    def __init__(self, browser: str) -> None:
        super().__init__()
        self.parser = WebParser(browser)

    def _parse_neuroweb_answer(self, text: str) -> list[str]:
        """
        Selects a list of products from a text.

        Args:
            text (str): text from neuroweb with products.

        Returns:
            List[str]: names of products from the text.
        """
        pattern = r"<search_query>\n(.*?)\n<search_query>"

        matches = re.search(pattern, text, re.DOTALL)
        if matches:
            content = matches.group(1)
            return [line.strip() for line in content.split("\n") if line.strip()]
        return []

    async def offer_products(self, messages: list) -> AsyncGenerator[str, None]:
        """
        Asynchronously offers products to the user based on his messages.

        Args:
            messages (list): List of messages.

        Yields:
            Iterator[AsyncGenerator[str, None]]: A generator that yields the response.
        """
        context_msgs = [{"role": "system", "content": self.prompt}] + messages[:]
        full_response = []
        async for part in self.openai_client.get_stream_response(
            model=self.model,
            temperature=self.temperature,
            context_messages=context_msgs,
        ):
            full_response.append(part)
        full_response = "".join(full_response)
        products = self._parse_neuroweb_answer(full_response)
        for product in products:
            yield product

    def get_information_about_product(self, product: str) -> dict:
        """
        Returns dictionary with information about product.

        Args:
            product (str): name of product.

        Returns:
            dict: dictionary with keys: link, name, price, photo.
        """
        product_url = self.parser.get_ozon_product_link(product)
        self.parser.update_session()
        info = self.parser.get_ozon_product_info(product_url)
        self.parser.update_session()
        return info
