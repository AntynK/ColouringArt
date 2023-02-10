import os
import pygame

from .menu import Menu
from .canvas import Canvas
from ..menu_elems.page_elem import PageElement

from ..thumbnail import load_thumbnail, delete_thumbnail
from ..get_arts import get_arts
from ..static_variables import ARTS_DIR, GAME_VERSION
from ..menu_elems.arrow_btns import ArrowButton, ButtonResponses
from ..menu_elems.text import Text
from ..progress_rate import delete_progress_rate
from ..pickart.pickart_file import PickartFile
from ..colors import LIGHT_GRAY_COLOR
from ..catrgory_style import Style
from ..logger import logger


class MainMenu(Menu):
    def init(self):
        self.set_background_color(LIGHT_GRAY_COLOR)
        self.pages: list[list[PageElement]] = []
        self.categories = []
        self.cur_page = 1
        self.cur_category = 0
        self.page_size = 12
        self.page_arrows = ArrowButton(200, 460, text=str(self.cur_page))
        self.category_arrows = ArrowButton(200, 10)
        self.invalid_arts = []
        self.version_text = Text(359, 480, f"Game version: {GAME_VERSION}", 10)

        self.on_key_pressed(pygame.K_F5, self.update_page)

        self.update_page()

    def update_categories(self):
        if not ARTS_DIR.is_dir():
            ARTS_DIR.mkdir(parents=True)

        self.categories.clear()
        for category in os.listdir(ARTS_DIR):
            if os.path.isdir(f"{ARTS_DIR}\\{category}"):
                self.categories.append(category)
        if len(self.categories) == 1:
            self.cur_category = 0

    def update_page(self):
        self.update_categories()
        if len(self.categories) == 0:
            self.pages.clear()
            return

        category_name: str = self.categories[self.cur_category]
        self.category_arrows.set_image(f"{ARTS_DIR}\\{category_name}\\icon.png")
        Style(category_name)

        arts: list[str] = get_arts(category_name)

        self.pages = [[] for _ in range(len(arts) // self.page_size + 1)]
        arts = self.validate_arts(arts)

        for index, path in enumerate(arts):
            thumbnail: pygame.surface.Surface = load_thumbnail(path)
            page_element = PageElement(thumbnail, str(path), index % self.page_size)
            self.pages[index // self.page_size].append(page_element)

        if len(self.pages[-1]) == 0:
            del self.pages[-1]
        self.check_arrows_activity()

    def validate_arts(self, arts: list[str]) -> list[str]:
        result: list[str] = []
        for art in arts:
            if art in self.invalid_arts:
                continue
            if not PickartFile(art).valid:
                self.invalid_arts.append(art)
                continue
            result.append(art)
        return result

    def check_arrows_activity(self):
        if len(self.pages) <= 1:
            self.page_arrows.set_active(False)
        else:
            self.page_arrows.set_active(True)

        if len(self.categories) <= 1:
            self.category_arrows.set_active(False)
        else:
            self.category_arrows.set_active(True)

    def display_updated(self):
        self.check_page_arrows()
        self.check_category_arrows()
        self.version_text.draw(self.display)
        
        if self.cur_page - 1 >= len(self.pages) or len(self.pages) == 0:
            return
        for elem in self.pages[self.cur_page - 1]:
            if elem.draw(self.display):
                self._show_canvas(elem.path)

    def check_category_arrows(self):
        if not (response := self.category_arrows.draw(self.display)):
            return
        if not self.category_arrows.get_active():
            return
        if response == ButtonResponses.LEFT_BTN:
            self.cur_category -= 1

        if response == ButtonResponses.RIGHT_BTN:
            self.cur_category += 1

        if self.cur_category >= len(self.categories):
            self.cur_category = 0
        elif self.cur_category < 0:
            self.cur_category = len(self.categories) - 1
        self.update_page()

    def check_page_arrows(self):
        if not (response := self.page_arrows.draw(self.display)):
            return
        if not self.page_arrows.get_active():
            return
        if response == ButtonResponses.LEFT_BTN:
            self.cur_page -= 1

        if response == ButtonResponses.RIGHT_BTN:
            self.cur_page += 1

        if self.cur_page > len(self.pages):
            self.cur_page = 1
        elif self.cur_page < 1:
            self.cur_page = len(self.pages)

        self.page_arrows.set_text(str(self.cur_page))

    def _show_canvas(self, path: str):
        if not os.path.exists(path):
            self.update_page()
            return
        delete_thumbnail(path)
        delete_progress_rate(path)
        logger.info(f"Loading '{path}'.")
        Canvas(path).show(self.display)
        self.update_page()
