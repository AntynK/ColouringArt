import json
from typing import Any
from pathlib import Path

from .static_variables import ARTS_DIR
from .logger import logger
from .colors import CATEGORY_COLOR, GRAY_COLOR


class Style:
    def __init__(self, category_name: str) -> None:
        self.path = Path(f"{ARTS_DIR}\\{category_name}\\style.json")
        self.category_name = category_name
        self._data = {}
        self._load()

    def _load(self):
        CATEGORY_COLOR.update(GRAY_COLOR)
        try:
            self._data: dict[str, Any] = json.loads(self.path.read_text("utf-8"))
            self._parse()
        except Exception as error:
            logger.error(
                f"Cannot load file '{self.category_name}\\style.json', error: {error}."
            )

    def _parse(self):
        if not isinstance(self._data, dict):
            raise ValueError()
        color = self._data.get("bg")
        if not isinstance(color, list) or len(color) != 3:
            raise ValueError()

        for c in color:
            if c < 0 or c > 255:
                raise ValueError()
        CATEGORY_COLOR.update(color)
