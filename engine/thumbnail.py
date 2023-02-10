import contextlib
import struct
import os

import pygame

from .pickart.pickart_file import PickartFile, Color

from .image.load import load_image
from .image.cache import ImageCacher

from .static_variables import THUMBNAILS_DIR
from .file_checker import get_file_hash


def create_dir():
    if not THUMBNAILS_DIR.exists():
        THUMBNAILS_DIR.mkdir(parents=True)


def load_thumbnail(path: str) -> pygame.surface.Surface:
    create_dir()
    file_hash: str = get_file_hash(path)
    thumb_path = f"{THUMBNAILS_DIR}\\{file_hash}.png"
    try:
        return load_image(thumb_path)
    except Exception:
        create_thumbnail(path)

    return load_image(thumb_path)


def delete_thumbnail(path: str):
    file_hash: str = get_file_hash(path)
    filename = f"{THUMBNAILS_DIR}\\{file_hash}.png"
    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)
        ImageCacher.delete_cache(filename)


def create_thumbnail(path: str):
    file_hash: str = get_file_hash(path)
    file = PickartFile(path)

    buffer = b""
    palette: dict[int, Color] = file.get_palette()
    fmt: str = ">" + "B" * file.fmt.value

    for col in file.get_pixels():
        row_ = b""
        for row in col:
            if row[0] is None:
                row_ += struct.pack(fmt, 0, 0, 0, 0)
                continue

            color = palette[row[0]]
            color = color.color if row[1] else color.grayscale
            row_ += struct.pack(fmt, *color)
        buffer += row_
    surf = pygame.image.fromstring(buffer, file.get_size(), file.fmt.name)  # type: ignore

    pygame.image.save(surf, f"{THUMBNAILS_DIR}\\{file_hash}.png")
