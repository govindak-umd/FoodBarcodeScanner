"""
Get food nutritional info from: https://world.openfoodfacts.org
"""

import requests
import pandas as pd
import json


def get_website_food_db(food_barcode):
    """
    function to get food info from the website
    """
    food_barcode = str(food_barcode)
    url = f"https://world.openfoodfacts.org/api/v2/product/" + food_barcode + ".json"
    try:
        response = requests.get(url)
        data = response.json()
        with open(
            "json_hist/raw_openfoodfacts_data_" + food_barcode + ".json", "w"
        ) as f:
            json.dump(data, f, indent=4)
        return data
    except requests.exceptions.SSLError as ssl_err:
        print(f"SSL error when fetching food data: {ssl_err}")
        print("Check your network or certificate settings.")
    except requests.exceptions.RequestException as req_err:
        print(f"Network error when fetching food data: {req_err}")
        print("Failed to retrieve data from website. Check network security.")
    except Exception as err:
        print(f"Unexpected error when fetching food data: {err}")


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
            nutritional_info_dict = dict()

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
            return nutritional_info_dict

    except FileNotFoundError:
        print(f"File not found for - {food_barcode}")
        return None


def convert_json_to_csv(json_data):
    """
    Concerts JSON to CSV file
    :param json_data:
    :return:
    """
    with open(str(json_data) + ".json") as f:
        data = json.load(f)
    df = pd.json_normalize(data)  # flattens nested JSON
    # df.to_csv(str(json_data)+"_csv.csv", index=False)


def retrieve_food():
    """
    function to retrieve a specific foods nutrition info
    :return:
    """
    pass
