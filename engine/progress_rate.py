import pickle
from pathlib import Path

from .file_checker import get_file_hash
from .pickart.pickart_file import PickartFile, RestrictedUnpickler
from .static_variables import ARTS_DIR

DB_FILE = Path(f"{ARTS_DIR}\\progress.dat")


def load_progress() -> dict[str, float]:
    try:
        with open(DB_FILE, "rb") as file:
            return RestrictedUnpickler(file).load()
    except Exception:
        save_progress_rate({})
        return {}


def save_progress_rate(data: dict):
    with open(DB_FILE, "wb") as file:
        pickle.dump(data, file)


def delete_progress_rate(filepath: str):
    db_data: dict[str, float] = load_progress()
    file_hash: str = get_file_hash(filepath)
    if file_hash not in db_data:
        return
    db_data.pop(file_hash)
    save_progress_rate(db_data)


def get_progress_rate(filepath: str) -> float:
    db_data: dict[str, float] = load_progress()

    file_hash: str = get_file_hash(filepath)
    if file_hash in db_data:
        return db_data[file_hash]

    pickart_file = PickartFile(filepath)
    total_pixels = 0
    completed_pixels = 0

    for col in pickart_file.get_pixels():
        for row in col:
            if row[0] is None:
                continue
            total_pixels += 1
            if row[1]:
                completed_pixels += 1
    rate: float = round(completed_pixels / total_pixels * 100, 1)
    db_data[file_hash] = rate

    save_progress_rate(db_data)
    return rate
