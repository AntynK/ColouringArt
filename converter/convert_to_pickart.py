import pygame
import struct
import pickle
from gzip import GzipFile
from io import BytesIO
from dataclasses import asdict
from pathlib import Path

from engine.pickart.pickart_file_data import PickartFileData


def convert_to_pickart(filename: Path, output_dir: Path):
    image = pygame.image.load(filename)
    file_data = BytesIO(image.get_buffer().raw)  # type: ignore

    byte_size = image.get_bytesize()
    format_ = byte_size * "B"

    width, height = image.get_size()

    data = []
    palette = {}

    info = {
        "size": (width, height),
        "version": 1,
    }

    for _ in range(height):
        row_list = []
        for _ in range(width):
            color = struct.unpack_from(format_, file_data.read(byte_size))
            if len(color) == 4 and color[3] == 0:
                row_list.append([None, False])
                continue

            if color not in palette:
                palette[color] = len(palette)

            color_index = palette[color]
            row_list.append([color_index, False])

        data.append(row_list)

    result = PickartFileData(info, list(palette.keys()), data)

    with GzipFile(f"{output_dir}/{Path(filename).stem}.pickart", "wb") as file:
        file.write(pickle.dumps(asdict(result)))
