from glob import glob
from hashlib import md5
from pathlib import Path
from zipfile import ZipFile

from engine.static_variables import FILE_HASHES, ASSETS_DIR, ASSETS_BAK
from engine.logger import logger


def get_file_hash(filename: Path):
    with open(filename, "rb") as file:
        return md5(file.read()).hexdigest()


def check_file_hash(filename: Path) -> bool:
    file_hash: str = get_file_hash(filename)
    return file_hash == FILE_HASHES.get(filename)


def check_assets_file(filename: Path):
    if not filename.is_file():
        logger.error(f"File: '{filename}' does not exist.")
        extract_file(filename)

    if not check_file_hash(filename):
        logger.error(f"File: '{filename}' is corrupted.")
        extract_file(filename)


def extract_file(filename: Path):
    try:
        with ZipFile(ASSETS_BAK) as file:
            file.extract(str(filename).replace("\\", "/"))
            logger.info(f"Extracted file: '{filename}'.")
    except Exception as e:
        logger.critical(f"Cannot load '{ASSETS_BAK}', error:{e}.")


def generate_hashes():
    res = {
        file: get_file_hash(Path(file))
        for file in glob(f"{ASSETS_DIR}/**/*.*", recursive=True)
    }
    print(res)
