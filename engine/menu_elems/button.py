from typing import Callable

import pygame

from ..static_variables import ICONS_DIR
from ..image.load import load_from_assets


class Button:
    def __init__(self, x: int, y: int, icon_name: str, callback: Callable) -> None:
        self.x, self.y = x, y

        self.icon: pygame.surface.Surface = load_from_assets(
            f"{ICONS_DIR}\\{icon_name}.png"
        )
        self.callback = callback
        self.rect = pygame.Rect(x, y, *self.icon.get_size())
        self.pressed = False

    def draw(self, display: pygame.surface.Surface):
        display.blit(self.icon, (self.x, self.y))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.icon.set_alpha(100)
            if pygame.mouse.get_pressed()[0] and not self.pressed:
                self.pressed = True
                self.callback()
            return

        self.icon.set_alpha(255)
        self.pressed = False
