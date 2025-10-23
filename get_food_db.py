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
    nutritional_info_dict["nutriments"] = food_barcode_data["product"]["nutriments"]
    nutritional_info_dict["nutrient_levels"] = food_barcode_data["product"][
        "nutrient_levels"
    ]
    nutritional_info_dict["nutrient_levels_tags"] = food_barcode_data["product"][
        "nutrient_levels_tags"
    ]

    print(nutritional_info_dict)
    return nutritional_info_dict


def convert_json_to_csv(json_data):
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


if __name__ == "__main__":
    # Retrieve food info from nutrition website
    sample_barcode = "737628064502"
    get_website_food_db(sample_barcode)
    retrieve_nutrition_data(sample_barcode)
    # convert json to csv (for viz)
    # convert_json_to_csv(website_food_db)
    # parse through the DB

    # display info for a specific barcode
