import datetime
import logging
from pathlib import Path

from engine.static_variables import LOGS_DIR


LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)

FORMAT = "[%(asctime)s] [%(filename)s:%(levelname)s]: %(message)s"
formatter = logging.Formatter(fmt=FORMAT, datefmt="%H:%M:%S")

file_handler = logging.FileHandler(
    Path(LOGS_DIR, f"{datetime.datetime.now():%d.%m.%Y_%H-%M-%S}.log"),
    encoding="utf-8",
    delay=False,
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
