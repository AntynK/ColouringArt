import pickle
from typing import Union
from pathlib import Path
from gzip import GzipFile
from dataclasses import asdict

from .pickart_file_data import PickartFileData
from .restricted_unpickler import RestrictedUnpickler
from .color import Color
from .color_formats import ColorFormats

from ..logger import logger
from ..static_variables import PICKART_VERSON


class PickartFile:
    def __init__(self, filepath: Union[str, Path]):
        self.filepath = str(filepath)
        self._data = PickartFileData()
        self.color_palette: dict[int, Color] = {}
        self.valid = True
        self.load()

    def _load_file(self):
        try:
            with GzipFile(self.filepath) as file:
                self._data = PickartFileData(**RestrictedUnpickler(file).load())
                version: int = self._data.info.get("version", 404)
                if version != PICKART_VERSON:
                    raise ValueError(f"File version: '{version}' isn't supported")
                if any(i <= 0 for i in self._data.info.get("size", (0, 0))):
                    raise ValueError("Art size must be positive")

                self.fmt = (
                    ColorFormats.RGBA
                    if len(self._data.palette[0]) == 4
                    else ColorFormats.RGB
                )

        except Exception as error:
            self.valid = False
            logger.error(f"Cannot load file '{self.filepath}', error: {error}.")

    def check_color(self, color: tuple[int, ...]) -> bool:
        return len(color) == self.fmt.value and all(
            (c <= 255 and c >= 0 for c in color)
        )

    def load(self):
        self._load_file()

        if not self.valid:
            return

        for key, color in enumerate(self._data.palette):
            if not self.check_color(color):
                self.valid = False
                logger.error(f"Bad pixel format in file: '{self.filepath}'.")
                break

            self.color_palette[key] = Color(color)

    def set_painted(
        self, x: int, y: int, color_index: int, colors_left: dict[int, int]
    ):
        if self._data.pixels[y][x][0] != color_index or self._data.pixels[y][x][1]:
            return
        self._data.pixels[y][x][1] = True

        colors_left[color_index] -= 1

    def get_pixels(self) -> list[list]:
        return self._data.pixels

    def get_size(self) -> tuple[int, int]:
        return self._data.info["size"]

    def get_palette(self):
        return self.color_palette

    def save(self):
        with GzipFile(self.filepath, "w") as file:
            file.write(pickle.dumps(asdict(self._data)))
            logger.info(f"Saved file: '{self.filepath}'")

    def __repr__(self) -> str:
        filepath = self.filepath
        size = self.get_size()
        return f"PickartFile({filepath=}), art {size=}"
