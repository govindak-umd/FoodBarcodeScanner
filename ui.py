"""
UI code
"""

import flet as ft
from flet.core import page

from barcode_read import *
from get_food_db import *


class DisplayHMI:

    def __init__(self, new_page, processed_nutritional_info):
        self.page = new_page
        self.page.title = "Nutritional Info"
        self.processed_nutritional_info = processed_nutritional_info
        self.ui_colors = {"low": "green", "moderate": "orange", "high": "red"}
        self.txt_name = ft.TextField(
            label=str(processed_nutritional_info["product_name_en"])
        )
        self.nutr = ft.Text()

        self.display_main_ui()

    def display_main_ui(self):
        """
        function to display the UI and basic info
        :param page:
        :param processed_nutritional_info: nutritional info from generated JSON file
        :return:
        """

        # add the image of the food item
        img_url = self.processed_nutritional_info["image_url"]

        # retrieve the food image
        food_image = ft.Image(
            src=img_url,
            width=300,
            height=200,
            fit=ft.ImageFit.CONTAIN,
        )

        # alignment of the image to be top and center of the page
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.add(
            ft.Row(
                [food_image],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        # TODO - change the name in the text bar to the barcode
        # txt_name = ft.TextField(label=str(self.processed_nutritional_info["product_name_en"]))
        self.txt_name = ft.TextField(
            label=str(self.processed_nutritional_info["product_name_en"])
        )

        self.page.add(
            self.txt_name,
            ft.ElevatedButton(
                "Display Nutritional Info", on_click=self.display_nutrition
            ),
            self.nutr,
        )

    def display_nutrition(self, e):
        """
        function to get nutritional value upon click of the elevated button
        :param e:  Event - mouse click
        :return:
        """

        # Initialize a span
        spans = []

        spans.append(
            ft.TextSpan(
                f"{"Serving Size"} - {self.processed_nutritional_info["serving_size"]}\n",
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
