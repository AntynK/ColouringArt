from typing import Optional
from pathlib import Path

import pygame

from engine.assets import ImageCacher
from engine.logger import logger
from engine.file_checker import check_assets_file
from engine.static_variables import AssetsFiles


@ImageCacher()
def load_image(
    filename: Path, image_size: Optional[int] = None, is_external=False
) -> pygame.surface.Surface:
    if not is_external:
        check_assets_file(filename)

    try:
        image: pygame.surface.Surface = pygame.image.load(filename).convert_alpha()
    except Exception as e:
        logger.error(f"Cannot load image: '{filename}', error: {e}.")
        image = load_image(AssetsFiles.DEFAULT_IMG)

    if image_size:
        image = pygame.transform.scale(image, (image_size, image_size))
    return image


def load_font(filename: Path, font_size: int) -> pygame.font.Font:
    check_assets_file(filename)
    try:
        font = pygame.font.Font(filename, font_size)
    except Exception as e:
        logger.error(f"Cannot load font: '{filename}', error: {e}.")
        font = pygame.font.SysFont("Arial", font_size)
    return font
