"""
UI code
"""

import flet as ft


def main(page: ft.Page):
    page.title = "Nutritional Info"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_name = ft.TextField(label="Enter Barcode ... ")
    nutr = ft.Text()

    def display_nutrition(e):
        nutr.value = "Nutritional Info - xxx"
        page.update()

    page.add(
        txt_name,
        ft.ElevatedButton("Display Nutritional Info ... ", on_click=display_nutrition),
        nutr,
    )


ft.app(target=main)
