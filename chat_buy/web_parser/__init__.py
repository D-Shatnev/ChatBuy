"""This module contains the interfaces for the web parser."""

from chat_buy.web_parser.constants import CHROME, FIREFOX
from chat_buy.web_parser.parser import WebParser

__all__ = [
    "CHROME",
    "FIREFOX",
    "WebParser",
]
