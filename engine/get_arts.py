from pathlib import Path
from typing import Optional

from .static_variables import ARTS_DIR


def get_arts(category: Optional[str]) -> list:
    """Returns list of all .pickart files in 'arts/category.'"""
    return list(Path(f"{ARTS_DIR}\\{category}").glob("*.pickart"))
