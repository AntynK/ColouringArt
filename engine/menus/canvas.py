import datetime
import pygame

from .menu import Menu

from ..pickart.pickart_file import PickartFile, Color
from ..menu_elems.text import Text
from ..menu_elems.sidebar import SideBar
from ..menu_elems.palette import Palette
from ..thumbnail import load_thumbnail, delete_thumbnail
from ..static_variables import EXPORTS_DIR
from ..image.load import load_from_assets
from ..colors import WHITE_COLOR


class Canvas(Menu):
    def __init__(self, path: str):
        super().__init__()
        self.pickart_file = PickartFile(path)
        self.color_palette: dict[int, Color] = self.pickart_file.get_palette()

        self.block_size = 12
        self.selected_color = 0
        self.x_shift = 100
        self.y_shift = 100
        self.palette = Palette(self.color_palette)

        self.selected_color_img: pygame.surface.Surface = load_from_assets(
            "assets\\selected_color_img.png"
        )
        self.side_bar = SideBar(
            460,
            50,
            {"exit": self.close, "save": self.pickart_file.save, "export": self.export},
        )

        self.set_background_color(WHITE_COLOR)
        self.generate_palettes_text()
        self.get_colors_left()
        self._calculate_game_zone()

        self.palette.select_color(0)

        self.on_key_pressed(pygame.K_ESCAPE, self.close)
        self.on_key_pressed(pygame.K_s, self.pickart_file.save)
        self.on_key_pressed(pygame.K_LEFT, self.palette.move_cursor, -1)
        self.on_key_pressed(pygame.K_RIGHT, self.palette.move_cursor, 1)

    def _calculate_game_zone(self):
        width, height = self.pickart_file.get_size()

        self.game_zone = pygame.rect.Rect(
            self.x_shift,
            self.y_shift,
            width * self.block_size,
            height * self.block_size,
        )

    def export(self):
        data = datetime.datetime.now()
        file_path = self.pickart_file.filepath
        EXPORTS_DIR.mkdir(exist_ok=True)
        pygame.image.save(
            load_thumbnail(file_path),
            f"{EXPORTS_DIR}\\{data:%Y-%m-%d_%H.%M.%S}.png",
        )

        delete_thumbnail(file_path)

    def get_colors_left(self):
        self.completed_colors = []

        self.colors_left = {index: 0 for index in self.color_palette}

        for col in self.pickart_file.get_pixels():
            for row in col:
                color_id = row[0]
                if color_id is None or row[1]:
                    continue
                if color_id in self.colors_left:
                    self.colors_left[color_id] += 1
                    continue
        self.update_compled_colors()

    def generate_palettes_text(self):
        self.text_palette = {
            index: Text(0, 0, str(index + 1), font_size=11)
            for index in self.color_palette.keys()
        }

    def event_handler(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                m_x, m_y = event.pos
                if not self.game_zone.collidepoint(m_x, m_y):
                    return

                self.pickart_file.set_painted(
                    (m_x - self.x_shift) // (self.block_size),
                    (m_y - self.y_shift) // (self.block_size),
                    self.selected_color,
                    self.colors_left,
                )
                self.update_compled_colors()

            if event.buttons[2]:
                self.x_shift += event.rel[0]
                self.y_shift += event.rel[1]
                self._calculate_game_zone()

        if event.type == pygame.MOUSEWHEEL:
            if self.block_size + event.y > 20 or self.block_size + event.y < 11:
                return

            self.block_size += event.y
            self._calculate_game_zone()

    def update_compled_colors(self):
        for key, value in self.colors_left.items():
            if value == 0 and key not in self.completed_colors:
                self.completed_colors.append(key)
                self.palette.set_completed_color(key)
                self.palette.show = len(self.completed_colors) != len(
                    self.color_palette
                )

    def display_updated(self):
        self.draw_pixels()
        self.draw_palette()
        self.side_bar.draw(self.display)

    def draw_palette(self):
        response = self.palette.draw(self.display)
        if response is not None:
            self.selected_color = response

    def close(self):
        super().close()
        self.pickart_file.save()

    def draw_pixels(self):
        for y_, col in enumerate(self.pickart_file.get_pixels()):
            for x_, row in enumerate(col):
                color_index = row[0]
                if color_index is None:
                    continue

                color = self.color_palette[color_index]

                color = color.color if row[1] else color.grayscale
                x = x_ * self.block_size + self.x_shift
                y = y_ * self.block_size + self.y_shift
                self.draw_block(color, x, y, row, color_index)

    def draw_block(
        self,
        color: tuple[int, ...],
        x: int,
        y: int,
        row: tuple[int, bool],
        color_index: int,
    ):
        pygame.draw.rect(
            self.display,
            color,
            (
                x,
                y,
                self.block_size,
                self.block_size,
            ),
        )
        if self.selected_color == color_index and not row[1]:
            self.display.blit(
                pygame.transform.scale(
                    self.selected_color_img, (self.block_size, self.block_size)
                ),
                (x, y),
            )
            return
        if not row[1] and self.block_size >= 16:
            self.display.blit(self.text_palette[color_index].rendered_text, (x + 5, y))
