import pygame
from pickart import Colour

from engine.menu_elems import PaletteColour, ArrowButton, ButtonResponses
from engine.colours import GRAY_COLOUR


class Palette:
    def __init__(self, palette: dict[int, Colour]) -> None:
        self.palette = palette
        self.palette_size = 20

        self._show = True
        self._arrow_button = ArrowButton(10, 430, width=390, draw_bg=False)

        self._load_pages()

        self._selected_page_index = 0
        self._selected_colour = 0
        self._selected_colour_page = 0
        self._selected_page: list[PaletteColour] = self.pages[self._selected_page_index]

    def _load_pages(self):
        self.pages = [[] for _ in range(len(self.palette) // self.palette_size + 1)]

        for index, colour in self.palette.items():
            y, x = divmod(index % self.palette_size, (self.palette_size // 2))

            self.pages[index // self.palette_size].append(
                PaletteColour(colour.colour, index, x, y)
            )
        if len(self.pages[-1]) == 0:
            del self.pages[-1]

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, val: bool):
        if not isinstance(val, bool):
            raise ValueError(f"Argument must be bool type, not {type(val)}")
        self._show = val

    def move_cursor(self, step: int):
        index = self._check_colour_index(self._selected_colour + step)
        while self._selected_page[index % self.palette_size].completed:
            index = self._check_colour_index(index + step)
            if all(colour.completed for colour in self._selected_page):
                break
        self.select_colour(index)

    def _check_colour_index(self, index: int) -> int:
        if index == -1:
            index = len(self.palette) - 1
        elif index == len(self.palette):
            index = 0
        self.set_page(index)
        return index

    def set_page(self, index: int):
        self._selected_page_index = index // self.palette_size
        self._selected_page = self.pages[index // self.palette_size]

    def set_completed_colour(self, index: int):
        page, colour = divmod(index, self.palette_size)
        self.pages[page][colour].completed = True

    def _arrow_button_handler(self, response: ButtonResponses):
        if response == ButtonResponses.LEFT_BTN:
            self._scroll_page(-1)
        elif response == ButtonResponses.RIGHT_BTN:
            self._scroll_page(1)

    def _scroll_page(self, step: int):
        self._selected_page_index += step

        if self._selected_page_index < 0:
            self._selected_page_index = len(self.pages) - 1
        elif self._selected_page_index >= len(self.pages):
            self._selected_page_index = 0

        self._selected_page = self.pages[self._selected_page_index]

    def draw(self, display: pygame.surface.Surface):
        if not self._show:
            return
        pygame.draw.rect(display, GRAY_COLOUR, (0, 400, 500, 100))
        for colour in self._selected_page:
            response = colour.draw(display)
            if response is None:
                continue
            self.select_colour(response)
        if response := self._arrow_button.draw(display):
            self._arrow_button_handler(response)

        return self._selected_colour

    def select_colour(self, index: int):
        colour_index = abs(index) % self.palette_size
        colour = self._selected_page[colour_index]
        if colour.completed:
            return
        page_index = self._selected_colour % self.palette_size

        self.pages[self._selected_colour_page][page_index].selected = False
        self._selected_colour = index
        self._selected_colour_page = self._selected_page_index
        page_index = self._selected_colour % self.palette_size
        self._selected_page[page_index].selected = True
