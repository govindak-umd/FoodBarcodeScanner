"""
UI code
"""

import re
import flet as ft
from flet.core import page
from utils import *
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
            logger.info(f"Barcode Updated to {self.barcode}")
            return True
        else:
            logger.error("Barcode Validation Error")
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
        """
        Function to retrieve all food data from the website.
        :return:
        """
        if check_json_file(self.barcode):
            logger.info("File found from history - will use that")
            pass
        else:
            logger.warning(
                "File not found from history - retrieving data from internet"
            )
            try:
                # Retrieve food info from nutrition website
                get_website_food_db(self.barcode)
            except Exception as err:
                logger.error(err)
        self.processed_nutritional_info = retrieve_nutrition_data(self.barcode)
        logger.info(f"New Barcode Data processed for {self.barcode}")

    def display_nutrition(self, e):
        """
        function to parse correct nutrients and display the nutritional info
        :param e: Mouse Event Click
        """

        """
        function to update the text after the user clicks it
        :param e: Mouse Event Click
        """

        # blank out the previous nutrition info text
        # self.txt_name.update()
        spans = []
        self.nutr.spans = spans

        # update barcode
        if self.barcode_update():
            # happy path - incase the barcode is correct format
            # after updating barcode, retrieve all food data
            self.retrieve_all_data()
            # update the text box after data has been retrieved
            self.txt_name.value = self.barcode
            self.txt_name.color = "white"
            self.food_image.src = self.processed_nutritional_info["image_url"]
        else:
            # exception case - incase the barcode is NOT correct format
            self.txt_name.value = "Invalid Barcode - Please enter a numerical barcode"
            self.txt_name.color = "red"
            self.food_image.src = "https://via.placeholder.com/300x200?text=No+Image"
        self.page.update()
        logger.info(f"Successfully showed image for {self.barcode}")

        # Initialize a span
        spans = []

        # if else case for when barcode is valid and when its not
        if barcode_validity_checker(self.txt_name.value):
            self.txt_name.value = self.barcode
            self.page.update()
            spans.append(
                ft.TextSpan(
                    f"{self.processed_nutritional_info["product_name_en"]}\n",
                    style=ft.TextStyle(color="white", size=16),
                )
            )
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
            logger.info(f"Successfully updated nutritional info for {self.barcode}")

        else:

            spans.append(
                ft.TextSpan(
                    f"Cannot display nutritional info for an invalid barcode",
                    style=ft.TextStyle(color="red", size=16),
                )
            )

            self.nutr.spans = spans
            self.page.update()

            logger.error("Cannot display nutritional info for an invalid barcode")
