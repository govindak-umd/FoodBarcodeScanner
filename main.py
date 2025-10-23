"""
main script
"""

from ui import *
from barcode_read import *
from get_food_db import *


if __name__ == "__main__":
    ft.app(target=lambda page: display_main_ui(page, nutritional_info))
