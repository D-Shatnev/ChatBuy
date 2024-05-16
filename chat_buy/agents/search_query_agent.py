"""
This module contains the SearchQueryAgent class.
"""
import re
from chat_buy.web_parser import WebParser
from chat_buy.web_parser.constants import CHROME
from chat_buy.agents.base_agent import BaseAgent

class SearchQueryAgent(BaseAgent):
    def __init__(self):
        self.parser = WebParser(CHROME)

    def parse_neuroweb_answer(self, text: str) -> list[str]:
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
            return [line.strip() for line in content.split('\n') if line.strip()]
        return None

    def get_information_about_product(self, product : str) -> dict:
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