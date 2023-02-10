from glob import glob
from hashlib import md5

from .static_variables import FILE_HASHES, ASSETS_DIR


def get_file_hash(filename: str):
    with open(filename, "rb") as file:
        return md5(file.read()).hexdigest()


def check_file_hash(filename: str) -> bool:
    file_hash: str = get_file_hash(filename)
    return file_hash == FILE_HASHES.get(filename)


def generate_hashes():
    res = {
        file: get_file_hash(file)
        for file in glob(f"{ASSETS_DIR}/**/*.*", recursive=True)
    }
    print(res)
