"""
main script
"""

import flet as ft
from utils import *
from ui import DisplayHMI
from get_food_db import *

import logging
import colorlog

logger = colorlog.getLogger()  # get root logger

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
)

if logger.hasHandlers():
    logger.handlers.clear()

logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.debug("Logger initialized")  # sanity check

if __name__ == "__main__":

    sample_barcode = "859213005001"
    sample_barcode_2 = "722252153258"
    sample_barcode_3 = "8445290728791"  # kitkat

    ft.app(target=lambda page: DisplayHMI(page))
