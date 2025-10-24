"""
main script
"""

import flet as ft
from utils import *
from ui import DisplayHMI
from get_food_db import *

if __name__ == "__main__":
    sample_barcode = "859213005001"
    sample_barcode_2 = "722252153258"
    sample_barcode_3 = "8445290728791"  # kitkat

    ft.app(target=lambda page: DisplayHMI(page))
