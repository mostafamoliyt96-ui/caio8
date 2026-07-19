"""
CAIO Translate - MCP Server Package
A lightweight, stateless translation service for ChatGPT Apps.
"""

__version__ = "1.0.0"
__author__ = "CAIO Team"
__description__ = "Interactive Translation & Learning Application for ChatGPT"

from .store import store
from .languages import SUPPORTED_LANGUAGES, is_valid_language, get_language_code

__all__ = [
    "store",
    "SUPPORTED_LANGUAGES",
    "is_valid_language",
    "get_language_code",
]
