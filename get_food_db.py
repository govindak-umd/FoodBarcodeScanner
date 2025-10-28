"""
Get food nutritional info from: https://world.openfoodfacts.org
"""

import json
import logging

import requests

logger = logging.getLogger(__name__)


class FoodDB:
    """
    Class to access food info from the database
    """

    def __init__(self, food_barcode):
        self.food_barcode = food_barcode
        self.nutritional_info_dict = {}
        self.url = ""

    def get_website_food_db(self):
        """
        function to get food info from the website
        """
        self.food_barcode = str(self.food_barcode)
        self.url = (
            "https://world.openfoodfacts.org/api/v2/product/"
            + self.food_barcode
            + ".json"
        )
        try:
            response = requests.get(self.url, timeout=10)  # timeout = 10 seconds
            data = response.json()
            with open(
                "json_hist/raw_openfoodfacts_data_" + self.food_barcode + ".json", "w"
            ) as f:
                json.dump(data, f, indent=4)
            logger.info("Successfully fetched data from website")
        except requests.exceptions.SSLError as ssl_err:
            logger.error("SSL error when fetching food data: %s", ssl_err)
            logger.error("Check your network or certificate settings.")
        except requests.exceptions.RequestException as req_err:
            logger.error("Network error when fetching food data: %s", req_err)
            logger.error(
                "Failed to retrieve data from website. Check network security."
            )
        except Exception as err:
            logger.error("Unexpected error when fetching food data: %s", err)

    def retrieve_nutrition_data(self):
        """
        function to retrieve only the nutrition info from a json
        :param food_barcode:
        :return: nutritional_info_dict
        """

        try:
            with open(
                "json_hist/raw_openfoodfacts_data_" + self.food_barcode + ".json", "r"
            ) as f:
                food_barcode_data = json.load(f)
                # extract all essential characteristics
                self.nutritional_info_dict["image_url"] = food_barcode_data["product"][
                    "image_url"
                ]
                self.nutritional_info_dict["serving_size"] = food_barcode_data[
                    "product"
                ]["serving_size"]
                self.nutritional_info_dict["product_name_en"] = food_barcode_data[
                    "product"
                ]["product_name_en"]
                self.nutritional_info_dict["nutriments"] = food_barcode_data["product"][
                    "nutriments"
                ]
                self.nutritional_info_dict["nutrient_levels"] = food_barcode_data[
                    "product"
                ]["nutrient_levels"]
                self.nutritional_info_dict["nutrient_levels_tags"] = food_barcode_data[
                    "product"
                ]["nutrient_levels_tags"]
                logger.info("Successfully fetched data from website")
                return self.nutritional_info_dict

        except FileNotFoundError:
            logger.error("File not found for - %s", self.food_barcode)
            return None
