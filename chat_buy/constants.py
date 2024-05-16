import os
from dotenv import load_dotenv

try:
    load_dotenv(".env")
except FileNotFoundError:
    pass

API_KEY = os.getenv("API_KEY")
API_BASE = os.getenv("API_BASE")
