import os
from pathlib import Path

DELIVERY_MIN_DISTANT = 10
DEFAULT_TAX_LIMIT = 50000
DEFAULT_FACTORY_NAME_LIMIT = 20
HIRE_PRICE = 370

TAX_LIMIT: int = int(os.environ.get("TAX_LIMIT", DEFAULT_TAX_LIMIT))
DEBUG: bool = os.environ.get("DEBUG") != "False"
FACTORY_NAME_LENGTH_LIMIT: int = int(
    os.environ.get("FACTORY_NAME_LIMIT", DEFAULT_FACTORY_NAME_LIMIT)
)
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "static"
