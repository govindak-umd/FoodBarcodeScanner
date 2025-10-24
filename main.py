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

    try:
        # Retrieve food info from nutrition website
        food_data = get_website_food_db(sample_barcode)
        nutritional_info = retrieve_nutrition_data(sample_barcode)
        get_website_food_db(sample_barcode_2)
        nutritional_info_2 = retrieve_nutrition_data(sample_barcode_2)
    except Exception as err:
        print(err)

    if check_json_file(sample_barcode):
        try:
            ft.app(
                target=lambda page: DisplayHMI(
                    page, nutritional_info, nutritional_info_2
                )
            )
        except Exception as err:
            print(err)
    else:
        print("JSON file not found - Please try again")
