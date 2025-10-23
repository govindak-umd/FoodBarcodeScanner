"""
Get food nutritional info from: https://world.openfoodfacts.org
"""

import requests
import pandas as pd
import json


def get_website_food_db(food_barcode):
    """
    function to get food info from the website
    random barcodes for testing:
    737628064502
    722252153258
    """
    food_barcode = str(food_barcode)
    api_key = "YOUR_KEY"
    # GET https://world.openfoodfacts.org/api/v2/product/737628064502.json
    url = f"https://world.openfoodfacts.org/api/v2/product/" + food_barcode + ".json"
    response = requests.get(url)
    data = response.json()
    with open("json_hist/raw_openfoodfacts_data_" + food_barcode + ".json", "w") as f:
        json.dump(data, f, indent=4)
    return data


def retrieve_nutrition_data(food_barcode=None):
    """
    function to retrieve only the nutrition info from a json
    :param food_barcode:
    :return: nutritional_info_dict
    """
    with open("json_hist/raw_openfoodfacts_data_" + food_barcode + ".json", "r") as f:
        food_barcode_data = json.load(f)
    nutritional_info_dict = dict()

    # extract all essential characteristics
    nutritional_info_dict["image_url"] = food_barcode_data["product"]["image_url"]
    nutritional_info_dict["serving_size"] = food_barcode_data["product"]["serving_size"]
    nutritional_info_dict["product_name_en"] = food_barcode_data["product"][
        "product_name_en"
    ]
    nutritional_info_dict["nutriments"] = food_barcode_data["product"]["nutriments"]
    nutritional_info_dict["nutrient_levels"] = food_barcode_data["product"][
        "nutrient_levels"
    ]
    nutritional_info_dict["nutrient_levels_tags"] = food_barcode_data["product"][
        "nutrient_levels_tags"
    ]
    return nutritional_info_dict


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


# Retrieve food info from nutrition website
sample_barcode = "859213005001"
get_website_food_db(sample_barcode)
nutritional_info = retrieve_nutrition_data(sample_barcode)

sample_barcode_2 = "722252153258"
get_website_food_db(sample_barcode_2)
nutritional_info_2 = retrieve_nutrition_data(sample_barcode_2)
# convert json to csv (for viz)
# convert_json_to_csv(website_food_db)
# parse through the DB

# display info for a specific barcode
