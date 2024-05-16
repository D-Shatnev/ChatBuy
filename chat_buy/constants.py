"""
This module contains the general constants of the project and load environment variables.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

try:
    load_dotenv(".env")
except FileNotFoundError:
    pass

API_KEY = os.getenv("API_KEY")
API_BASE = os.getenv("API_BASE")
AGENT_CONFIG = Path(os.getenv("AGENT_CONFIG"))
