import os
from typing import Any, Dict

API_DEBUG = os.getenv("API_DEBUG", "false") == "true"


config: Dict[str, Any] = {"api": {"debug": API_DEBUG}}
