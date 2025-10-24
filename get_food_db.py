"""
Get food nutritional info from: https://world.openfoodfacts.org
"""
import json
import logging

import requests

logger = logging.getLogger(__name__)


def get_website_food_db(food_barcode):
    """
    function to get food info from the website
    """
    food_barcode = str(food_barcode)
    url = "https://world.openfoodfacts.org/api/v2/product/" + food_barcode + ".json"
    try:
        response = requests.get(url, timeout=10) # timeout = 10 seconds
        data = response.json()
        with open(
            "json_hist/raw_openfoodfacts_data_" + food_barcode + ".json", "w"
        ) as f:
            json.dump(data, f, indent=4)
        logger.info("Successfully fetched data from website")
    except requests.exceptions.SSLError as ssl_err:
        logger.error("SSL error when fetching food data: %s",ssl_err)
        logger.error("Check your network or certificate settings.")
    except requests.exceptions.RequestException as req_err:
        logger.error("Network error when fetching food data: %s",req_err)
        logger.error("Failed to retrieve data from website. Check network security.")
    except Exception as err:
        logger.error("Unexpected error when fetching food data: %s",err)


def retrieve_nutrition_data(food_barcode=None):
    """
    function to retrieve only the nutrition info from a json
    :param food_barcode:
    :return: nutritional_info_dict
    """

    try:
        with open(
            "json_hist/raw_openfoodfacts_data_" + food_barcode + ".json", "r"
        ) as f:
            food_barcode_data = json.load(f)
            nutritional_info_dict = {}

            # extract all essential characteristics
            nutritional_info_dict["image_url"] = food_barcode_data["product"][
                "image_url"
            ]
            nutritional_info_dict["serving_size"] = food_barcode_data["product"][
                "serving_size"
            ]
            nutritional_info_dict["product_name_en"] = food_barcode_data["product"][
                "product_name_en"
            ]
            nutritional_info_dict["nutriments"] = food_barcode_data["product"][
                "nutriments"
            ]
            nutritional_info_dict["nutrient_levels"] = food_barcode_data["product"][
                "nutrient_levels"
            ]
            nutritional_info_dict["nutrient_levels_tags"] = food_barcode_data[
                "product"
            ]["nutrient_levels_tags"]
            logger.info("Successfully fetched data from website")
            return nutritional_info_dict

    except FileNotFoundError:
        logger.error("File not found for - %s",food_barcode)
        return None
