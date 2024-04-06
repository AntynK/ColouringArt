import pygame

from engine.menus.main_menu import MainMenu
from engine.logger import logger
from engine.assets import load_image
from engine.static_variables import (
    ASSETS_DIR,
    ASSETS_BAK,
    ICONS_DIR,
    GAME_TITLE,
    WIDTH,
    HEIGHT,
    AssetsFiles,
)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_icon(load_image(AssetsFiles.LOGO))

    def start(self):
        if not ASSETS_BAK.is_file():
            logger.warn(f"File: '{ASSETS_BAK}' does not exist.")

        self.load_assets()

        MainMenu().show(self.display)

    def load_assets(self):
        for file in ASSETS_DIR.glob("*.png"):
            load_image(file)
        for file in ICONS_DIR.glob("*.png"):
            load_image(file)
