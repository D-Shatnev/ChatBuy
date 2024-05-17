"""
This module contains endpoints for provision processing.
"""

from fastapi import APIRouter

from chat_buy.agents import search_query_agent
from chat_buy.api.models import Product

provision_router = APIRouter()


@provision_router.post("/v1/provision/")
def process_provision(product: Product) -> dict:
    """
    Searches for product information on marketplaces and returns results to the user.
    Returns dictionary with keys: link, name, price, photo.
    """
    return search_query_agent.get_information_about_product(product.name)
