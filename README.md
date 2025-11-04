[![Build Status](https://app.travis-ci.com/govindak-umd/FoodBarcodeScanner.svg?token=RyccV32Ghg6vrVDxC5nU&branch=main)](https://app.travis-ci.com/govindak-umd/FoodBarcodeScanner)

# FoodBarcodeScanner
Food Barcode retrieval app that can then produce nutritional information 

## Features (DONE)

- Retrieve Nutritional Information with a barcode
  - User types a barcode in the texbox
  - results are retrieved from the barcode
- Logs user input and outputs
- Can change barcode upon request
- Auto search and retrieve when 'enter' is hit on the text box
- Product History feature
  - show history of products that were searched 
  - configurable in a larger yml file on how many past searches
  - user can click on a past search and see the nutritional information 
  - clear search history, add a new button for this
- workflows 
  - pylint check
  - black check
  - isort check

## Feature Requests (future TODO)

- asyncio
  - in the future, always search for healthier alternatives along with originally requested products health information

- workflows
  - auto merge workflow 
    - should run only when the other workflows are done

- Machine Learning aspect of the project
  - Suggest healthier alternatives
    - Machine learning
    - all food database info
    - rank food based on health

### Running 

    python main.py

### Generating requirements.txt helper command

    pip list --format=freeze > requirements.txt

### Test Barcode

    sample_barcode = "859213005001"
    sample_barcode_2 = "722252153258"
    sample_barcode_3 = "8445290728791"
    sample_barcode_4 = "3017624010701