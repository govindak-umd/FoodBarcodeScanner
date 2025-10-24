"""
main script
"""

import flet as ft
from ui import DisplayHMI

import logging
import colorlog
from pathlib import Path
from datetime import datetime

Path("logs").mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"logs/app_{timestamp}.log"

logger = colorlog.getLogger()

if logger.hasHandlers():
    logger.handlers.clear()

console = colorlog.StreamHandler()
console.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
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

file_handler = logging.FileHandler(log_filename, mode="a", encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)

logger.addHandler(console)
logger.addHandler(file_handler)

logger.setLevel(logging.INFO)  # <-- DEBUG so your test line appears

logger.debug("Logger initialized")  # will go to console + file
logger.info("Logs will be saved to %s", log_filename)


if __name__ == "__main__":

    ft.app(target=lambda page: DisplayHMI(page))
