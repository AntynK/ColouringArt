import os
import contextlib
from pathlib import Path

import pygame
from pickart.converter import convert_to_png

from engine.assets import load_image, ImageCacher
from engine.static_variables import THUMBNAILS_DIR
from engine.file_checker import get_file_hash


def load_thumbnail(path: Path) -> pygame.surface.Surface:
    THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)

    file_hash: str = get_file_hash(path)
    thumb_path = Path(THUMBNAILS_DIR, f"{file_hash}.png")
    if thumb_path.is_file():
        image = load_image(thumb_path, is_external=True)
    else:
        create_thumbnail(path)

    image = load_image(thumb_path, is_external=True)
    return image


def delete_thumbnail(path: Path):
    file_hash: str = get_file_hash(path)
    filename = Path(THUMBNAILS_DIR, f"{file_hash}.png")
    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)
        ImageCacher.delete_cache(filename)


def create_thumbnail(path: Path):
    file_hash: str = get_file_hash(path)
    convert_to_png(path, THUMBNAILS_DIR, f"{file_hash}.png")
