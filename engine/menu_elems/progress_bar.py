import pygame

from ..colors import CATEGORY_COLOR, LIGHT_GRAY_COLOR


class ProgressBar:
    def __init__(self, x: int, y: int, progress: float, width: int = 100) -> None:
        self.x, self.y = x, y

        self.width = width
        self._active = True
        self.set_progress(progress)

    def set_progress(self, progress: float):
        if progress <= 100 and progress >= 0:
            self.progress = progress
            self.progress_width = round(self.progress * self.width / 100)
            self._active = self.progress != 100

    def draw(self, display: pygame.surface.Surface):
        if not self._active:
            return

        pygame.draw.rect(
            display,
            LIGHT_GRAY_COLOR,
            (self.x, self.y, self.width, 10),
            border_radius=10,
        )

        pygame.draw.rect(
            display,
            CATEGORY_COLOR,
            (self.x, self.y, self.progress_width, 10),
            border_radius=10,
        )
