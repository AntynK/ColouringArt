import sys
from typing import Callable

import pygame

from engine.static_variables import FPS, clock
from engine.colours import BLACK_COLOUR
from engine.handlers import check_colour_format


class Menu:
    def __init__(self) -> None:
        self.set_background_colour(BLACK_COLOUR)
        self._active = True
        self._registered_keys: dict[int, Callable] = {}

        self.init()

    def set_background_colour(self, colour: tuple[int, int, int]) -> None:
        if check_colour_format(colour):
            self._bg_colour = colour
        else:
            raise ValueError(f"Wrong colour format:{colour}")

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

    def on_key_pressed(self, key: int, callback: Callable):
        """
        If key is pressed, callback is called.

        Args:
            key: int = use pygame.KEYNAME or pygame.key.key_code('KEY').
            callback: Callable = any callable object.
        """

        self._registered_keys[key] = callback

    def show(self, display: pygame.surface.Surface):
        self.display = display
        while self._active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if callback := self._registered_keys.get(event.key):
                        callback()

                self.event_handler(event)

            if self._bg_colour:
                display.fill(self._bg_colour)

            self.display_updated()

            pygame.display.update()
            clock.tick(FPS)

    def close(self):
        self._active = False
