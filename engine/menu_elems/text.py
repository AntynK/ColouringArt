import pygame

from engine.colours import BLACK_COLOUR
from engine.static_variables import Fonts
from engine.assets import load_font


class Text:
    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        font_size: int = 26,
    ) -> None:
        self.x, self.y = x, y

        self.text = text
        self.font_size = font_size
        self.font = load_font(Fonts.SILKSCREEN_REGULAR, font_size)

        self._render_text()

    def _render_text(self):
        self.rendered_text = self.font.render(self.text, True, BLACK_COLOUR)

    def update_text(self, text: str):
        self.text = text
        self._render_text()

    def draw(self, display: pygame.surface.Surface):
        display.blit(self.rendered_text, (self.x, self.y))

    def __repr__(self) -> str:
        x = self.x
        y = self.y
        text = self.text
        font_size = self.font_size
        return f"Text({x=}, {y=}, {text=}, {font_size=})"
