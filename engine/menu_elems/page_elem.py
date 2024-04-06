from pathlib import Path

import pygame

from engine.menu_elems import ProgressBar
from engine.progress_rate import get_progress_rate
from engine.colours import WHITE_COLOUR, GRAY_COLOUR
from engine.static_variables import IMAGE_SIZE


class PageElement:
    def __init__(
        self, thumbnail: pygame.surface.Surface, path: Path, index: int
    ) -> None:
        self.size = (IMAGE_SIZE * 2, IMAGE_SIZE * 2)

        self.thumbnail = pygame.transform.scale(thumbnail, self.size)
        self.path: Path = path
        self.index = index
        y, x = divmod(index, 4)
        self.x = x * 90 + 70
        self.y = y * 100 + 70
        self.rect = pygame.Rect(self.x, self.y, self.size[0] + 20, self.size[1] + 30)
        self.rect_colour = WHITE_COLOUR
        self.progress_bar = ProgressBar(
            self.x + 10, self.y + 80, get_progress_rate(path), width=60
        )

    def __repr__(self) -> str:
        thumbnail = self.thumbnail
        path = self.path
        index = self.index
        return f"PageElement({thumbnail=}, {path=}, {index=})"

    def draw(self, display: pygame.surface.Surface):
        pygame.draw.rect(display, self.rect_colour, self.rect)
        display.blit(self.thumbnail, (self.x + 10, self.y + 5))
        self.progress_bar.draw(display)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.rect_colour = GRAY_COLOUR
            return bool(pygame.mouse.get_pressed()[0])
        self.rect_colour = WHITE_COLOUR
