from pathlib import Path
from typing import Optional

from engine.static_variables import ARTS_DIR


def check_colour_format(colour):
    return isinstance(colour, (tuple, list)) and len(colour) in {3, 4}


def get_arts(category: Optional[str]) -> list[Path]:
    """Returns list of all .pickart files in category folder."""
    return list(Path(ARTS_DIR, f"{category}").glob("*.pickart"))
