"""
This module contains the main FastAPI application.
"""

import uvicorn
from fastapi import FastAPI

from chat_buy.api.constants import LOG_LEVEL
from chat_buy.api.utils import get_logger

logger = get_logger("api", LOG_LEVEL)


app = FastAPI()

def run_api(host: str = "localhost", port: int = 8000, reload: bool = True) -> None:
    """
    Run the API server.

    Args:
        host (str): The host IP address to bind the server to. Defaults to "localhost".
        port (int): The port number to bind the server to. Defaults to 8000.
        reload (bool): Whether to enable auto-reloading of the server. Defaults to True.
    """
    logger.info("Starting API server on %s:%s", host, port)
    uvicorn.run("chat_buy.api.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    run_api()
