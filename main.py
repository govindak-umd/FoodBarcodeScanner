"""
main script
"""

import flet as ft
from ui import DisplayHMI
from get_food_db import nutritional_info, nutritional_info_2

if __name__ == "__main__":
    ft.app(target=lambda page: DisplayHMI(page, nutritional_info, nutritional_info_2))
