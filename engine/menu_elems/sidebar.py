from typing import Callable
from pathlib import Path

import pygame

from engine.menu_elems import Button
from engine.colours import LIGHT_GRAY_COLOUR


class SideBar:
    def __init__(self, x: int, y: int, btns_data: dict[Path, Callable]) -> None:
        self.x, self.y = x, y
        self.buttons: list[Button] = []
        self.buttons.extend(
            Button(self.x + 5, self.y + 40 * index + 5, *btn_data)
            for index, btn_data in enumerate(btns_data.items())
        )
        self.rect = pygame.Rect(x, y, 40 + 5, 40 * len(self.buttons))

    def draw(self, display: pygame.surface.Surface):
        pygame.draw.rect(display, LIGHT_GRAY_COLOUR, self.rect, border_radius=5)
        for btn in self.buttons:
            btn.draw(display)
