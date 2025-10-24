"""
Commonly used utilities file
"""

import json


def check_json_file(food_barcode):
    """
    Checks if a JSON file exists in the history directory
    :param food_barcode:
    :return: True or False
    """
    try:
        with open(
            "json_hist/raw_openfoodfacts_data_" + food_barcode + ".json", "r"
        ) as f:
            json.load(f)
            return True
    except FileNotFoundError:
        print(f"File not found for - {food_barcode}")
        return False
