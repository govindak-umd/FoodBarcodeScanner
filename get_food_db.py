"""
Get food nutritional info from: https://world.openfoodfacts.org
"""

import json
import logging
import yaml
import requests

logger = logging.getLogger(__name__)

# Load nutrient config YAML file
with open("config/nutrient_config.yml", "r", encoding="utf-8") as file:
    nutrient_config = yaml.safe_load(file)


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
                try:
                    logger.info("Successfully fetched image from website")
                    self.nutritional_info_dict["image_url"] = food_barcode_data[
                        "product"
                    ]["image_url"]
                except KeyError:
                    logger.error("Image not available on the website")
                    self.nutritional_info_dict["image_url"] = (
                        "https://via.placeholder.com/300x200?text=No+Image"
                    )

                product = food_barcode_data.get("product", {})

                all_necessary_fields = nutrient_config["all_display_fields"]

                for key, label in all_necessary_fields.items():
                    value = product.get(key)
                    if value is None:
                        value = f"{label} Unavailable from source"
                        logger.error(f"{label} not available on the website")
                    self.nutritional_info_dict[key] = value

                logger.info(
                    "Successfully fetched all available and requested from website"
                )
                print(self.nutritional_info_dict)
                return self.nutritional_info_dict

        except FileNotFoundError:
            logger.error("File not found for - %s", self.food_barcode)
            return None
