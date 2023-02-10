import sys
from typing import Callable

import pygame

from ..static_variables import FPS, clock
from ..colors import BLACK_COLOR


class Menu:
    def __init__(self) -> None:
        self.set_background_color(BLACK_COLOR)
        self._alive = True
        self._registered_keys: dict[int, tuple] = {}

        self.init()

    def set_background_color(self, color: tuple[int, int, int]) -> None:
        if isinstance(color, tuple) and len(color) == 3:
            self._bg_color = color
        else:
            raise ValueError("Background must be a tuple with 3 int values.")

    def init(self):
        """
        Called after code in __init__ executed.

        You can modify this method in child classes.
        """

        pass

    def event_handler(self, event: pygame.event.Event):
        """
        Called when event received.

        You can modify this method in child classes.
        """

        pass

    def display_updated(self):
        """
        Called after display filled.

        You can modify this method in child classes.
        """

        pass

    def on_key_pressed(self, key: int, callback: Callable, *arg):
        """
        If key is pressed, callback is called.

        Args:
            key: int = use pygame.KEYNAME or pygame.key.key_code('KEY').
            callback: Callable = any callable object.
        """

        self._registered_keys[key] = (callback, arg)

    def show(self, display: pygame.surface.Surface):
        self.display = display
        while self._alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if callback := self._registered_keys.get(event.key):
                        func = callback[0]
                        func(*callback[1])

                self.event_handler(event)

            if self._bg_color:
                display.fill(self._bg_color)

            self.display_updated()

            pygame.display.update()
            clock.tick(FPS)

    def close(self):
        self._alive = False
