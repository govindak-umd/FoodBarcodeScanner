[![Build Status](https://app.travis-ci.com/govindak-umd/FoodBarcodeScanner.svg?token=RyccV32Ghg6vrVDxC5nU&branch=main)](https://app.travis-ci.com/govindak-umd/FoodBarcodeScanner)

# FoodBarcodeScanner
Food Barcode retrieval app that can then produce nutritional information 

        Version: V1

User is greeted with this screen to enter the barcode:

![Screenshot 2025-11-13 at 8.13.07 PM.png](images/Screenshot%202025-11-13%20at%208.13.07%E2%80%AFPM.png)

Once the barcode is searched and entered, the nutritional values are displayed:

![Screenshot 2025-11-13 at 8.13.42 PM.png](images/Screenshot%202025-11-13%20at%208.13.42%E2%80%AFPM.png)

The UI also presents the user with options to check back previously searched barcodes

The data also changes color based on health value. For example, green indicates healthy

![Screenshot 2025-11-13 at 8.16.31 PM.png](images/Screenshot%202025-11-13%20at%208.16.31%E2%80%AFPM.png)

### Running 

    python main.py

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

### Generating requirements.txt helper command

    pip list --format=freeze > requirements.txt

### Test Barcode

    sample_barcode = "859213005001"
    sample_barcode_2 = "722252153258"
    sample_barcode_3 = "8445290728791"
    sample_barcode_4 = "3017624010701