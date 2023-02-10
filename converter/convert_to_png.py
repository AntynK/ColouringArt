import struct
from pathlib import Path


import pygame

from engine.pickart.pickart_file import PickartFile


def convert_to_png(filename: Path, output_dir: Path):
    file = PickartFile(filename)

    buffer = b""
    palette = file.get_palette()
    fmt = ">" + "B" * file.fmt.value

    for col in file.get_pixels():
        row_ = b""
        for row in col:
            if row[0] is None:
                row_ += struct.pack(fmt, 0, 0, 0, 0)
                continue

            color = palette[row[0]]
            color = color.color if row[1] else color.grayscale
            row_ += struct.pack(fmt, *color)
        buffer += row_
    surf = pygame.image.fromstring(buffer, file.get_size(), file.fmt.name)  # type: ignore

    pygame.image.save(surf, f"{output_dir}\\{Path(filename).stem}.png")
