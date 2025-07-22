import os
from pathlib import Path

DELIVERY_MIN_DISTANT = 10
DEFAULT_TAX_LIMIT = 50000
HIRE_PRICE = 370

TAX_LIMIT: int = int(os.environ.get("TAX_LIMIT", DEFAULT_TAX_LIMIT))
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "static"
