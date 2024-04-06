from typing import Union
from pathlib import Path

import pygame


clock = pygame.time.Clock()
FPS = 60

GAME_TITLE = "Colouring art"
GAME_VERSION = "1.0.1"

WIDTH = 500
HEIGHT = 500

IMAGE_SIZE = 32

strOrPath = Union[str, Path]

THUMBNAILS_DIR = Path("thumbnails")
ARTS_DIR = Path("arts")
ASSETS_DIR = Path("assets")
ICONS_DIR = Path(ASSETS_DIR, "icons")
FONTS_DIR = Path(ASSETS_DIR, "fonts")
EXPORTS_DIR = Path("exports")
LOGS_DIR = Path("logs")
ASSETS_BAK = Path("assets.bak")


class AssetsFiles:
    LOGO = Path(ASSETS_DIR, "logo.png")
    SELECTED_COLOUR_IMG = Path(ASSETS_DIR, "selected_colour_img.png")
    DEFAULT_IMG = Path(ASSETS_DIR, "default_image.png")


class Icons:
    ARROW = Path(ICONS_DIR, "arrow.png")
    EXIT = Path(ICONS_DIR, "exit.png")
    EXPORT = Path(ICONS_DIR, "export.png")
    SAVE = Path(ICONS_DIR, "save.png")


class Fonts:
    SILKSCREEN_REGULAR = Path(FONTS_DIR, "Silkscreen-Regular.ttf")


FILE_HASHES: dict[Path, str] = {
    AssetsFiles.DEFAULT_IMG: "f136c6e9ee46abe026101d5cc6343beb",
    AssetsFiles.LOGO: "be5f2629ed2fea6d26e6b802e8d8bb43",
    AssetsFiles.SELECTED_COLOUR_IMG: "6b660643e1a9820eec94f41a932d5bd3",
    Fonts.SILKSCREEN_REGULAR: "5bed8502768fedf857a0ec8b81350f39",
    Icons.ARROW: "85f36af303478d929a2f0f476992c7b5",
    Icons.EXIT: "0fc10ed81c809b39b251e6d92c491ec4",
    Icons.EXPORT: "6daf045fdf69f785d208106166287ca9",
    Icons.SAVE: "a3ecea4c31a02b2c2b119c15df64b82c",
}
