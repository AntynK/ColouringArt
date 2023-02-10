import os
from glob import glob

import pygame

from .menus.main_menu import MainMenu
from .logger import logger
from .image.load import load_from_assets
from .static_variables import ASSETS_DIR, GAME_TITLE, WIDTH, HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        
        pygame.display.set_icon(load_from_assets(f"{ASSETS_DIR}\\logo.png"))
        
    def start(self):
        logger.info("Starting the game...")
        logger.debug(f"Pygame version: {pygame.version.ver}")

        if not os.path.isfile("assets.bak"):
            logger.warn("File: 'assets.bak', does not exist.")

        self.load_assets()

        MainMenu().show(self.display)

    def load_assets(self):
        logger.info("Loading assets")
        for file in glob(f"{ASSETS_DIR}/**/*.png", recursive=True):
            load_from_assets(file)
