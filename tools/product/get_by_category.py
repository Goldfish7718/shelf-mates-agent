import requests
from config import API_URL, cookies

def get_by_category(category="fruits"):
    url = f"{API_URL}/products/getByCat/{category}"

    response = requests.get(url, cookies=cookies)

    if response.status_code != 200:
        return response.json()["message"]

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
        "description": "Fetch products from API based on category name. Use this ONLY when user asks or requests to view products from one or more categories.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Category of the products to fetch",
                    "enum": ["fruits, vegetables, millets, spices"]
                }
            },
            "required": ["category"]
        }
    }
}