import pygame

from engine.menu_elems import Text
from engine.colours import LIGHT_GRAY_COLOUR


class PaletteColour:
    def __init__(self, colour: tuple[int, ...], index: int, x: int, y: int) -> None:
        self.colour = colour
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
        pygame.draw.rect(display, self.colour, self.rect)  # type: ignore
        if not self._completed:
            self.text.draw(display)
        if self.selected:
            pygame.draw.rect(display, LIGHT_GRAY_COLOUR, self.rect, 2)

        if (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and pygame.mouse.get_pressed()[0]
        ):
            return self.index

    def __repr__(self) -> str:
        colour = self.colour
        index = self.index
        selected = self.selected
        completed = self._completed
        return f"PaletteColour({colour=}, {index=}, {selected=}, {completed=})"
