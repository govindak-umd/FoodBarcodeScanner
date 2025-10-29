"""
UI code
"""

import logging
import flet as ft
import yaml
from utils import (
    check_json_file,
    barcode_validity_checker,
    clear_history,
    add_and_retrieve_history,
)
from get_food_db import FoodDB


# Load UI YAML file
with open("config/ui_config.yml", "r", encoding="utf-8") as file:
    ui_config = yaml.safe_load(file)

logger = logging.getLogger(__name__)


class DisplayHMI:
    """
    Class to Display HMI
    """

    def __init__(self, new_page):

        # barcode related
        self.top_n_historical_barcodes = None
        self.barcode = None

        # UI related variables and initialize UI
        self.nutritional_info = None
        self.text_color_severity = None
        self.txt_name = None
        self.food_image = None
        self.processed_nutritional_info = None
        self.history_row = None
        self.page = new_page
        self.initialize_ui()

        # query food information from the database upon UI initialization
        self.food_database_query = FoodDB(self.barcode)

    def initialize_ui(self):
        """
        Calling this function will initialize the UI.
        It will bring up all the text boxes, image,and title.

        :return:
        """
        self.page.title = "Nutritional Info"
        self.processed_nutritional_info = None
        # placeholder image
        # alignment of the image to be top and center of the page
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # placeholder image, this is just to have an image object. Does not
        # display anything
        self.food_image = ft.Image(
            src="https://via.placeholder.com/300x200?text=No+Image",
            width=ui_config["display_img"]["width"],
            height=ui_config["display_img"]["height"],
            fit=ft.ImageFit.CONTAIN,
        )
        self.page.add(
            ft.Row(
                [self.food_image],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        # text box
        self.txt_name = ft.TextField(
            label="Enter Barcode here ...", on_submit=self.display_nutrition
        )

        # colors of data based on severity
        # colors are taken from the ui_config
        self.text_color_severity = ui_config["text_color"][
            "severity_colors_nutrition_levels"
        ]

        # the label is the text on top of the text box
        self.txt_name.label = "Enter food here ... "
        self.nutritional_info = ft.Text()

        # row with all history information
        self.history_row = ft.Row(
            [],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        # stacking buttons, text boxes and text sections on the page
        self.page.add(
            self.txt_name,
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Display Nutritional Info",
                        on_click=self.display_nutrition,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            self.nutritional_info,
            self.history_row,
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Clear history",
                        on_click=lambda e: clear_history(),
                        color=ui_config["button_colors"]["clear_history_button_color"],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

    def barcode_update(self):
        """
        updates the barcode parameter when called
        :return: True (No barcode validation error),  False (barcode validation error)
        """
        if barcode_validity_checker(self.txt_name.value):
            self.barcode = self.txt_name.value  # read text from TextField
            self.txt_name.value = self.barcode

            self.page.update()
            # update the history and retrieve the barcodes
            self.top_n_historical_barcodes = add_and_retrieve_history(self.barcode)
            return True
        logger.error("Barcode Validation Error")
        return False

    def retrieve_all_data(self):
        """
        Function to retrieve all food nutritional data from the website.
        """
        if check_json_file(self.barcode):
            logger.info("File found from history - will use that")
        else:
            logger.warning(
                "File not found from history - retrieving data from internet"
            )
            try:
                # Retrieve food info from nutrition website
                self.food_database_query.get_website_food_db()
            except Exception as err:
                logger.error(err)
        self.processed_nutritional_info = (
            self.food_database_query.retrieve_nutrition_data()
        )

        logger.info("New Barcode Data processed for %s", self.barcode)

    def display_nutrition(self, e):
        """
        calling this function should display all the nutritional
        information from the website. It will automatically update the
        barcode with whatever is in the text box (if its valid) and then
        display the nutritional information.
        :param e: Mouse Event Click
        """
        # blank out the previous nutrition info text
        spans = []
        self.nutritional_info.spans = spans

        # update barcode
        if self.barcode_update():
            self.food_database_query = FoodDB(self.barcode)
            # happy path - incase the barcode is correct format
            # after updating barcode, retrieve all food data
            self.retrieve_all_data()
            # update the text box after data has been retrieved
            self.txt_name.value = self.barcode
            self.txt_name.color = ui_config["text_color"]["regular_text"]
            self.food_image.src = self.processed_nutritional_info["image_url"]
        else:
            # exception case - incase the barcode is NOT correct format
            self.txt_name.value = "Invalid Barcode - Please enter a numerical barcode"
            self.txt_name.color = ui_config["text_color"]["error_text"]
            self.food_image.src = "https://via.placeholder.com/300x200?text=No+Image"
        self.page.update()
        logger.info("Successfully showed image for %s", self.barcode)

        # Initialize a span
        spans = []

        # if else case for when barcode is valid and when it's not
        if barcode_validity_checker(self.txt_name.value):
            self.txt_name.value = self.barcode
            self.page.update()
            spans.append(
                ft.TextSpan(
                    f"{self.processed_nutritional_info['product_name_en']}\n",
                    style=ft.TextStyle(
                        color=self.txt_name.color, size=ui_config["common_text_size"]
                    ),
                )
            )
            spans.append(
                ft.TextSpan(
                    f"\nServing Size - {self.processed_nutritional_info['serving_size']}\n",
                    style=ft.TextStyle(
                        color=self.txt_name.color, size=ui_config["common_text_size"]
                    ),
                )
            )

            try:
                for nutrient_key, nutrient_val in self.processed_nutritional_info[
                    "nutrient_levels"
                ].items():

                    # adding nutrient information on the UI
                    ## retrieve unit of the nutrient measurement from the nutriments dictionary
                    nutrient_unit = self.processed_nutritional_info["nutriments"][
                        str(nutrient_key + "_unit")
                    ]
                    ## add text and set color for the text based on value
                    color = ui_config["text_color"]["severity_colors_nutrition_levels"][
                        nutrient_val
                    ]

                    spans.append(
                        ft.TextSpan(
                            f"{nutrient_key.capitalize()} - {nutrient_val} - "
                            f"{self.processed_nutritional_info['nutriments'][nutrient_key]} "
                            f"{nutrient_unit}\n",
                            style=ft.TextStyle(
                                color=color, size=ui_config["common_text_size"]
                            ),
                        )
                    )

            except AttributeError as err:
                logger.error(err)
                color = ui_config["text_color"]["error_text"]
                spans.append(
                    ft.TextSpan(
                        f"No data available",
                        style=ft.TextStyle(
                            color=color, size=ui_config["common_text_size"]
                        ),
                    )
                )
            try:

                ## add text and set color for the text based on value
                color = ui_config["text_color"]["nutri_score_color_grade"][
                    self.processed_nutritional_info["nutriscore_grade"]
                ]

                spans.append(
                    ft.TextSpan(
                        f"\n Nutri grade - {self.processed_nutritional_info[
                        "nutriscore_grade"
                    ].capitalize()} ",
                        style=ft.TextStyle(
                            color=color, size=ui_config["common_text_size"]
                        ),
                    )
                )

                self.nutritional_info.spans = spans
                self.page.update()
                logger.info(
                    "Successfully updated nutritional info for %s", self.barcode
                )

            except KeyError as err:
                color = ui_config["text_color"]["error_text"]
                spans.append(
                    ft.TextSpan(
                        f"No data available",
                        style=ft.TextStyle(
                            color=color, size=ui_config["common_text_size"]
                        ),
                    )
                )
                logger.error(err)

        else:

            spans.append(
                ft.TextSpan(
                    "Cannot display nutritional info for an invalid barcode",
                    style=ft.TextStyle(
                        color=self.txt_name.color, size=ui_config["common_text_size"]
                    ),
                )
            )

            self.nutritional_info.spans = spans
            self.page.update()

            logger.error("Cannot display nutritional info for an invalid barcode")

    def show_all_history(self):
        """
        placeholder function to display the history of all the
        previously scanned barcodes. The user should be able
        to click on the previously scanned barcodes and bring
        that product up to show nutritional information.
        :return:
        """
        pass
