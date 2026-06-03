import requests
from config import API_URL, cookies

def get_by_category(category="fruits"):
    url = f"{API_URL}/products/getByCat/{category}"

    response = requests.get(url, cookies=cookies)

    response.raise_for_status()

    data = response.json()

    transformed_products = []

    EXCLUDED_FIELDS = {
        "image",
        "__v",
        "stock",
        "reviews"
    }

    for product in data.get("transformedProducts", []):

        filtered_product = {
            key: value
            for key, value in product.items()
            if key not in EXCLUDED_FIELDS
        }

        transformed_products.append(filtered_product)

    return transformed_products


get_by_category_interface = {
    "type": "function",
    "function": {
        "name": "get_products_by_category",
        "description": "Fetch products from API based on category name",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Category name used to fetch products from the API. Elgible categories are fruits, millets, vegetables, spices ONLY."
                }
            },
            "required": ["category"]
        }
    }
}