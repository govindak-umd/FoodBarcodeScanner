"""
Commonly used utilities file
"""

import json
import re


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
        print(f"File not found in history for - {food_barcode}")
        return False


def barcode_validity_checker(barcode_input):
    """
    Function to check if a barcode is valid numerical input
    :param barcode_input: Barcode input from user in the text box
    :return: True if Yes, False if No
    """
    if re.fullmatch(r"\d+", barcode_input):
        print(f"Barcode Updated - {barcode_input} is a valid numerical barcode")
        return True
    else:
        print(f"Barcode Update Failed - {barcode_input} is not a number")
        return False
