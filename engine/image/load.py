import pygame
import os
import sys
from zipfile import ZipFile
from typing import Optional

from .cache import ImageCacher

from ..logger import logger
from ..file_checker import check_file_hash
from ..static_variables import IMAGE_SIZE


@ImageCacher()
def load_image(
    filename: str, image_size: Optional[int] = None
) -> pygame.surface.Surface:
    image: pygame.surface.Surface = pygame.image.load(filename).convert_alpha()
    if image_size:
        return pygame.transform.scale(image, (image_size, image_size))
    return image


@ImageCacher()
def load_from_assets(filename: str, is_external=False) -> pygame.surface.Surface:
    if is_external:
        try:
            return load_image(filename, IMAGE_SIZE)

        except Exception:
            logger.error(f"File: '{filename}' is corrupted or does not exist.")
            return load_from_assets("assets\\default_image.png")

    if not os.path.isfile("assets.bak"):
        try:
            return load_image(filename, IMAGE_SIZE)

        except Exception as e:
            logger.critical(
                f"File: '{filename}' is corrupted and backup file is corrupted."
            )
            sys.exit(1)

    if not os.path.isfile(filename):
        logger.error(f"File: '{filename}' does not exist.")
        extract_file(filename)
        return load_image(filename)

    if not check_file_hash(filename):
        logger.error(f"File: '{filename}' is corrupted.")
        extract_file(filename)
        return load_image(filename)
    return load_image(filename, IMAGE_SIZE)


def extract_file(filename: str):
    filename = filename.replace("\\", "/")
    try:
        with ZipFile("assets.bak") as file:
            file.extract(filename)
            logger.info(f"Extracted file: '{filename}'.")
    except Exception as e:
        logger.critical(e)
        sys.exit(1)
