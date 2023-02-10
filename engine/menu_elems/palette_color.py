import pygame

from .text import Text
from ..colors import LIGHT_GRAY_COLOR


class PaletteColor:
    def __init__(self, color: tuple[int, ...], index: int, x: int, y: int) -> None:
        self.color = color
        self.index = index
        self._completed = False
        self.selected = False

        self.x = x * 40 + 50
        self.y = y * 40 + 410
        self.text = Text(self.x + 5, self.y, str(index + 1))
        self.rect = pygame.Rect(self.x, self.y, 40, 40)

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, val: bool):
        if not isinstance(val, bool):
            raise ValueError(f"Argument must be bool type, not {type(val)}")
        self._completed = val

    def draw(self, display: pygame.surface.Surface):
        pygame.draw.rect(display, self.color, self.rect)
        if not self._completed:
            self.text.draw(display)
        if self.selected:
            pygame.draw.rect(display, LIGHT_GRAY_COLOR, self.rect, 2)

        if (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and pygame.mouse.get_pressed()[0]
        ):
            return self.index

    def __repr__(self) -> str:
        color = self.color
        index = self.index
        selected = self.selected
        completed = self._completed
        return f"{self.__class__.__name__}: ({color=}, {index=}, {selected=}, {completed=})"
