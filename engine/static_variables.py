from pathlib import Path

import pygame

clock = pygame.time.Clock()
FPS = 60

GAME_TITLE = "Colouring art"
GAME_VERSION = "1.0.0"

PICKART_VERSON = 1
WIDTH = 500
HEIGHT = 500

IMAGE_SIZE = 32

THUMBNAILS_DIR = Path("thumbnails")
ARTS_DIR = Path("arts")
ASSETS_DIR = Path("assets")
ICONS_DIR = Path("assets/icons")
FONTS_DIR = Path("assets/fonts")
EXPORTS_DIR = Path("exports")


FILE_HASHES: dict[str, str] = {
    "assets\\default_image.png": "f136c6e9ee46abe026101d5cc6343beb",
    "assets\\logo.png": "be5f2629ed2fea6d26e6b802e8d8bb43",
    "assets\\selected_color_img.png": "6b660643e1a9820eec94f41a932d5bd3",
    "assets\\fonts\\Silkscreen-Regular.ttf": "5bed8502768fedf857a0ec8b81350f39",
    "assets\\icons\\arrow.png": "85f36af303478d929a2f0f476992c7b5",
    "assets\\icons\\exit.png": "0fc10ed81c809b39b251e6d92c491ec4",
    "assets\\icons\\export.png": "6daf045fdf69f785d208106166287ca9",
    "assets\\icons\\save.png": "a3ecea4c31a02b2c2b119c15df64b82c",
}
