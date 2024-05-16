"""
This module contains the agents for the ChatBuy project.
"""

from chat_buy.agents.consultant_agent import ConsultantAgent
from chat_buy.agents.dialog_control_agent import DialogControlAgent
from chat_buy.agents.search_query_agent import SearchQueryAgent
from chat_buy.web_parser import CHROME

consultant_agent = ConsultantAgent()
dialog_control_agent = DialogControlAgent()
search_query_agent = SearchQueryAgent(browser=CHROME)
