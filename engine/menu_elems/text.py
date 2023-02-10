import pygame

from ..colors import BLACK_COLOR
from ..static_variables import FONTS_DIR
from ..image.load import extract_file


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
        try:
            self.font = pygame.font.Font(
                f"{FONTS_DIR}\\Silkscreen-Regular.ttf", font_size
            )
        except Exception:
            extract_file(f"{FONTS_DIR}\\Silkscreen-Regular.ttf")
            self.font = pygame.font.Font(
                f"{FONTS_DIR}\\Silkscreen-Regular.ttf", font_size
            )

        self.render_text()

    def render_text(self):
        self.rendered_text = self.font.render(self.text, True, BLACK_COLOR)

    def update_text(self, text: str):
        self.text = text
        self.render_text()

    def draw(self, display: pygame.surface.Surface):
        display.blit(self.rendered_text, (self.x, self.y))

    def __repr__(self) -> str:
        x = self.x
        y = self.y
        text = self.text
        font_size = self.font_size
        return f"Text({x=}, {y=}, {text=}, {font_size=})"
