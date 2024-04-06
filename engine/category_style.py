import json
from typing import Any
from pathlib import Path

from engine.static_variables import ARTS_DIR
from engine.logger import logger
from engine.colours import CATEGORY_COLOUR, GRAY_COLOUR


class Style:
    def __init__(self, category_name: str) -> None:
        self.path = Path(ARTS_DIR, category_name, "style.json")
        self.category_name = category_name
        self._data = {}
        self._load()

    def _load(self):
        CATEGORY_COLOUR.update(GRAY_COLOUR)
        try:
            self._data: dict[str, Any] = json.loads(self.path.read_text("utf-8"))
            self._parse()
        except Exception as error:
            logger.error(f"Cannot load style: '{self.path}', error: {error}.")

    def _parse(self):
        if not isinstance(self._data, dict):
            raise ValueError("Style config file must start with dict object.")
        colour = self._data.get("bg")
        if not isinstance(colour, list) or len(colour) not in {3, 4}:
            raise ValueError(f"Wrong colour format: {colour}.")

        for c in colour:
            if c < 0 or c > 255:
                raise ValueError(f"Wrong colour format: {colour}.")
        CATEGORY_COLOUR.update(colour)
