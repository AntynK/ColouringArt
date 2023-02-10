from typing import Optional
from enum import Enum

import pygame

from .text import Text

from ..static_variables import ICONS_DIR, IMAGE_SIZE
from ..image.load import load_from_assets
from ..colors import CATEGORY_COLOR


class ButtonResponses(Enum):
    LEFT_BTN = 0
    RIGHT_BTN = 1


class ArrowButton:
    def __init__(
        self,
        x: int,
        y: int,
        text: Optional[str] = None,
        icon_path: Optional[str] = None,
        width: int = 0,
        draw_bg: bool = True,
    ) -> None:
        self.x, self.y = x, y
        self.width = width
        self.draw_bg = draw_bg
        self._middle = None
        self._active = True

        if text:
            self._middle = Text(x + IMAGE_SIZE + 5, y - 1, text)
        elif icon_path:
            self._middle = load_from_assets(icon_path)

        self._left_arrow: pygame.surface.Surface = load_from_assets(
            f"{ICONS_DIR}\\arrow.png"
        )
        self._right_arrow = pygame.transform.rotate(self._left_arrow, 180)

        self._left_rect = pygame.Rect(x, y, *self._left_arrow.get_size())
        self._right_rect = pygame.Rect(
            x + IMAGE_SIZE * 2 + width, y, *self._right_arrow.get_size()
        )

        self._pressed = False

    def set_active(self, active: bool):
        self._active = active

    def _set_button_active(self, alpha: int):
        self._right_arrow.set_alpha(alpha)
        self._left_arrow.set_alpha(alpha)

    def set_image(self, image_path: str):
        self._middle = load_from_assets(image_path, True)

    def set_text(self, text: str):
        if not isinstance(self._middle, Text):
            raise ValueError("Text must be initialized!")
        self._middle.update_text(text)

    def get_active(self):
        return self._active

    def draw(self, display: pygame.surface.Surface):
        if self.draw_bg:
            pygame.draw.rect(
                display,
                CATEGORY_COLOR,
                (0, self.y - 10, display.get_width(), self._left_rect.width + 20),
            )
        if self._active:
            self._set_button_active(255)
        else:
            self._set_button_active(100)

        if isinstance(self._middle, Text):
            self._middle.draw(display)
        elif isinstance(self._middle, pygame.surface.Surface):
            display.blit(self._middle, (self.x + IMAGE_SIZE, self.y))

        display.blit(self._left_arrow, (self.x, self.y))

        display.blit(self._right_arrow, (self.x + IMAGE_SIZE * 2 + self.width, self.y))

        if pygame.mouse.get_pressed()[0]:
            if (
                self._left_rect.collidepoint(pygame.mouse.get_pos())
                and not self._pressed
            ):
                self._pressed = True
                return ButtonResponses.LEFT_BTN

            if (
                self._right_rect.collidepoint(pygame.mouse.get_pos())
                and not self._pressed
            ):
                self._pressed = True
                return ButtonResponses.RIGHT_BTN
            return

        self._pressed = False
