"""
This module contains the SearchQueryAgent class.
"""

import asyncio
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
            await asyncio.sleep(0.1)
            yield product

    def get_information_about_product(self, product: str) -> dict:
        """
        Returns dictionary with information about product.

        Args:
            product (str): name of product.

        Returns:
            dict: dictionary with keys: link, name, price, photo.
        """
        urls = self.parser.get_wildberries_products_links(product)
        if len(urls) == 3:
            info = {"link1": urls[0], "link2": urls[1], "link3": urls[2]}
        elif len(urls) == 2:
            info = {"link1": urls[0], "link2": urls[1]}
        elif len(urls) == 1:
            info = {"link1": urls[0]}
        else:
            info = {}
        return info
