"""
This module contains endpoints for provision processing.
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from chat_buy.agents import search_query_agent
from chat_buy.api.models import Product

provision_router = APIRouter()


@provision_router.post("/v1/provision/")
async def process_provision(product: Product) -> StreamingResponse:
    """
    Searches for product information on marketplaces and returns results to the user.
    """
    pass
