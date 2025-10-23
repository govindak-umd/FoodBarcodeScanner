"""
main script
"""

from ui import *
from barcode_read import *
from get_food_db import *


if __name__ == "__main__":
    ft.app(target=lambda page: DisplayHMI(page, nutritional_info, nutritional_info))
