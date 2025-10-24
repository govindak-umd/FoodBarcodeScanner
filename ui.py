"""
UI code
"""

import re
import flet as ft
from flet.core import page
from utils import *
from barcode_read import *
from get_food_db import *


class DisplayHMI:
    """
    Class to Display HMI
    """

    def __init__(self, new_page):
        # BARCODE related
        self.barcode = None

        # UI related
        self.page = new_page
        self.page.title = "Nutritional Info"
        self.processed_nutritional_info = None
        # placeholder image
        # alignment of the image to be top and center of the page
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.food_image = ft.Image(
            src="https://via.placeholder.com/300x200?text=No+Image",
            width=300,
            height=200,
            fit=ft.ImageFit.CONTAIN,
        )
        self.page.add(
            ft.Row(
                [self.food_image],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        # text box
        self.txt_name = ft.TextField(label="Enter Barcode here ...")

        # colors of data based on severity
        self.ui_colors = {"low": "green", "moderate": "orange", "high": "red"}

        # the label is the text on top of the text box
        self.txt_name.label = "Enter food here ... "
        self.nutr = ft.Text()
        self.display_main_ui()

    def barcode_update(self):
        """
        function to manage and maintain barcode
        :return:
        """
        if barcode_validity_checker(self.txt_name.value):
            self.barcode = self.txt_name.value  # read text from TextField
            self.txt_name.value = self.barcode

            self.page.update()
            print(f"Barcode Updated to {self.barcode}")
            return True
        else:
            print("Barcode Validation Error")
            return False

    def display_main_ui(self):
        """
        Main function to display the main UI.
        :return:
        """

        self.page.add(
            self.txt_name,
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Display Nutritional Info", on_click=self.display_nutrition
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            self.nutr,
        )

    def retrieve_all_data(self):

        if check_json_file(self.barcode):
            print("File found from history - will use that")
            pass
        else:
            print("File not found from history - retrieving data from internet")
            try:
                # Retrieve food info from nutrition website
                get_website_food_db(self.barcode)
            except Exception as err:
                print(err)
        self.processed_nutritional_info = retrieve_nutrition_data(self.barcode)
        print(f"New Barcode Data processed for {self.barcode}")

    def display_nutrition(self, e):
        """
        function to parse correct nutrients and display the nutritional info
        :param e: Mouse Event Click
        """
        self.txt_name.value = self.processed_nutritional_info["product_name_en"]
        self.page.update()

        # Initialize a span
        spans = []

        spans.append(
            ft.TextSpan(
                f"{"\nServing Size"} - {self.processed_nutritional_info["serving_size"]}\n",
                style=ft.TextStyle(color="white", size=16),
            )
        )
        for nutrient_key, nutrient_val in self.processed_nutritional_info[
            "nutrient_levels"
        ].items():
            # retrieve unit of the nutrient measurement from the nutriments dictionary
            nutrient_unit = self.processed_nutritional_info["nutriments"][
                str(nutrient_key + "_unit")
            ]

            # add text and set color for the text based on value
            color = self.ui_colors.get(nutrient_val, "white")
            spans.append(
                ft.TextSpan(
                    f"{nutrient_key.capitalize()} - {nutrient_val} - "
                    f"{self.processed_nutritional_info['nutriments'][nutrient_key]} {nutrient_unit}\n",
                    style=ft.TextStyle(color=color, size=16),
                )
            )

        self.nutr.spans = spans
        self.page.update()
