import datetime
import logging
from pathlib import Path

Path("logs/").mkdir(exist_ok=True)

logger = logging.getLogger(__name__)

FORMAT = "[%(asctime)s] [%(filename)s:%(levelname)s]: %(message)s"
formatter = logging.Formatter(fmt=FORMAT, datefmt="%H:%M:%S")

file_handler = logging.FileHandler(
    f"logs/{datetime.datetime.now():%d.%m.%Y_%H-%M-%S}.log",
    encoding="utf-8",
    delay=False,
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)