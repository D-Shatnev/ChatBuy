"""
This module contains the constants of the API.
"""

import logging
import os

LOG_LEVEL = logging.DEBUG if os.getenv("LOG_LEVEL") == "DEBUG" else logging.INFO

