import datetime
from pathlib import Path
from functools import partial

import pygame
from pickart import PickartFile, Colour

from engine.menus import Menu
from engine.menu_elems import Text, SideBar, Palette
from engine.thumbnail import load_thumbnail, delete_thumbnail
from engine.static_variables import EXPORTS_DIR, Icons, AssetsFiles
from engine.assets import load_image
from engine.colours import WHITE_COLOUR


class Canvas(Menu):
    def __init__(self, path: Path):
        super().__init__()
        self.pickart_file = PickartFile(path)
        self.colour_palette: dict[int, Colour] = self.pickart_file.get_palette()
        self.finished = False

        self.block_size = 12
        self.selected_colour = 0
        self.x_shift = 100
        self.y_shift = 100
        self.palette = Palette(self.colour_palette)

        self.selected_colour_img: pygame.surface.Surface = load_image(
            AssetsFiles.SELECTED_COLOUR_IMG
        )
        self.side_bar = SideBar(
            460,
            50,
            {
                Icons.EXIT: self.close,
                Icons.SAVE: self.pickart_file.save,
                Icons.EXPORT: self.export,
            },
        )

        self.set_background_colour(WHITE_COLOUR)
        self.generate_palettes_text()
        self.get_colours_left()
        self._calculate_game_zone()

        self.palette.select_colour(0)

        self.on_key_pressed(pygame.K_ESCAPE, self.close)
        self.on_key_pressed(pygame.K_s, self.pickart_file.save)
        self.on_key_pressed(pygame.K_LEFT, partial(self.palette.move_cursor, -1))
        self.on_key_pressed(pygame.K_RIGHT, partial(self.palette.move_cursor, 1))

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
        self.pickart_file.save()
        file_path = self.pickart_file.filepath
        EXPORTS_DIR.mkdir(exist_ok=True)
        pygame.image.save(
            load_thumbnail(file_path),  # type: ignore
            Path(EXPORTS_DIR, f"{data:%Y-%m-%d_%H.%M.%S}.png"),
        )

        delete_thumbnail(file_path)  # type: ignore

    def get_colours_left(self):
        self.completed_colours = []

        self.colours_left = {index: 0 for index in self.colour_palette}

        for col in self.pickart_file.get_pixels():
            for row in col:
                colour_id = row[0]
                if colour_id is None or row[1]:
                    continue
                if colour_id in self.colours_left:
                    self.colours_left[colour_id] += 1
                    continue
        self.update_compled_colours()

    def generate_palettes_text(self):
        self.text_palette = {
            index: Text(0, 0, str(index + 1), font_size=11)
            for index in self.colour_palette.keys()
        }

    def event_handler(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0] and not self.finished:
                m_x, m_y = event.pos
                if not self.game_zone.collidepoint(m_x, m_y):
                    return

                is_painted = self.pickart_file.set_painted(
                    (m_x - self.x_shift) // (self.block_size),
                    (m_y - self.y_shift) // (self.block_size),
                    self.selected_colour,
                )

                if is_painted:
                    self.colours_left[self.selected_colour] -= 1

                self.update_compled_colours()

            if event.buttons[2]:
                self.x_shift += event.rel[0]
                self.y_shift += event.rel[1]
                self._calculate_game_zone()

        if event.type == pygame.MOUSEWHEEL:
            if self.block_size + event.y > 20 or self.block_size + event.y < 11:
                return

            self.block_size += event.y
            self._calculate_game_zone()

    def update_compled_colours(self):
        for key, value in self.colours_left.items():
            if value == 0 and key not in self.completed_colours:
                self.completed_colours.append(key)
                self.palette.set_completed_colour(key)
                self.finished = len(self.completed_colours) == len(self.colour_palette)
                if self.finished:
                    self.pickart_file.save()

    def display_updated(self):
        self.draw_pixels()
        self.draw_palette()
        self.side_bar.draw(self.display)

    def draw_palette(self):
        if self.finished:
            return
        colour_index = self.palette.draw(self.display)
        if colour_index is not None:
            self.selected_colour = colour_index

    def close(self):
        super().close()
        self.pickart_file.save()

    def draw_pixels(self):
        for y_rel, col in enumerate(self.pickart_file.get_pixels()):
            for x_rel, row in enumerate(col):
                colour_index = row[0]
                if colour_index is None:
                    continue

                colour = self.colour_palette[colour_index]

                colour = colour.colour if row[1] else colour.grayscale
                x = x_rel * self.block_size + self.x_shift
                y = y_rel * self.block_size + self.y_shift
                self.draw_block(colour, x, y, row, colour_index)

    def draw_block(
        self,
        colour: tuple[int, ...],
        x: int,
        y: int,
        row: tuple[int, bool],
        colour_index: int,
    ):
        pygame.draw.rect(
            self.display,
            colour,  # type: ignore
            (
                x,
                y,
                self.block_size,
                self.block_size,
            ),
        )
        if self.selected_colour == colour_index and not row[1]:
            self.display.blit(
                pygame.transform.scale(
                    self.selected_colour_img, (self.block_size, self.block_size)
                ),
                (x, y),
            )
            return
        if not row[1] and self.block_size >= 16:
            self.display.blit(self.text_palette[colour_index].rendered_text, (x + 5, y))
