"""
Commonly used utilities file
"""

import json
import re
import logging
from pathlib import Path
import yaml


# Load UI YAML file
with open("config/ui_config.yml", "r", encoding="utf-8") as file:
    ui_config = yaml.safe_load(file)


logger = logging.getLogger(__name__)


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
            logger.info(f"JSON file {food_barcode} exists in history directory.")
            return True
    except FileNotFoundError:
        logger.warning(
            f"File not found in history for - {food_barcode}",
        )
        return False


def barcode_validity_checker(barcode_input):
    """
    Function to check if a barcode is valid numerical input
    :param barcode_input: Barcode input from user in the text box
    :return: True if Yes, False if No
    """
    if re.fullmatch(r"\d+", barcode_input):
        logger.info(f"Barcode Updated - {barcode_input} is a valid numerical barcode")
        return True
    else:
        logger.error(f"Barcode Update Failed - {barcode_input} is not a number")
        return False


def check_and_retrieve_history(food_barcode=None):
    """
    Function to manage history, add barcode search to history
    :param food_barcode:
    :return: top n history barcodes
    """
    Path("history").mkdir(exist_ok=True)  # ensure folder exists

    def compute_top_n_history_barcodes(history_dict):
        """
        function computes the top 'n' history barcodes
        :return: sorted keys of all the historical barcodes
        """
        max_history = ui_config["max_history"]

        # get a sorted dictionary and then sort it in reverse order (descending) and then parse it only until max_hisory size
        sorted_history = dict(
            sorted(history_dict.items(), key=lambda item: item[1], reverse=True)[
                : min(max_history, len(history_dict))
            ]
        )
        logger.info(f"Top {max_history} history barcodes : {sorted_history} ")

        return list(sorted_history.keys())

    try:
        with open("history/history.json", "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        logger.debug("History file loaded")
    except FileNotFoundError:
        logger.error(logger.error("No History JSON file found"))
        newly_created_data = {food_barcode: 1}
        json.dump(newly_created_data, f, indent=4)
    except json.JSONDecodeError:
        logger.error("JSON Error detected - creating a new JSON file")
        loaded_data = {}

    if food_barcode is not None:

        # increment the count if the barcode is in there
        if food_barcode in loaded_data:
            loaded_data[food_barcode] += 1
            logger.debug("Incremented count for %s", food_barcode)
        # add the count of 1 if the barcode is new
        else:
            loaded_data[food_barcode] = 1
            logger.debug("Added new food barcode %s to history", food_barcode)

    # save the JSON file
    with open("history/history.json", "w", encoding="utf-8") as f:
        json.dump(loaded_data, f, indent=4, ensure_ascii=False)

    top_n_history_barcodes = compute_top_n_history_barcodes(loaded_data)
    print(top_n_history_barcodes)
    logger.info("History updated successfully.")

    return top_n_history_barcodes


def clear_history():
    """
    Function to manage history, add barcode search to history
    :param food_barcode:
    :return:
    """
    Path("history").mkdir(exist_ok=True)  # ensure folder exists

    try:
        with open("history/history.json", "r", encoding="utf-8") as f:
            logger.debug("History JSON file loaded")
    except FileNotFoundError:
        logger.error(
            logger.error("FileNotFoundError detected - No History file file found")
        )
    except json.JSONDecodeError:
        logger.error("JSONDecodeError detected - creating a new JSON file")

    loaded_data = {}

    # make a history_json file
    with open("history/history.json", "w", encoding="utf-8") as f:
        json.dump(loaded_data, f, indent=4, ensure_ascii=False)

    logger.error("History cleared successfully.")
    logger.error("No more history barcodes in the database")
