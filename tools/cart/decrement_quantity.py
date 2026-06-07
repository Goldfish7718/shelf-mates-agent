import os
import requests
from utils import find_product_id
from openrouter import OpenRouter
from config import API_URL, cookies, MODELS

def decrement_quantity(products):
    for product in products:
        product_IDs = []

        product_id = find_product_id(product["name"])
        product_IDs.append(product_id)

    final_products = [
        {
            "product_id": product_id,
            "quantity": int(product["quantity"])
        }

        for product, product_id in zip(products, product_IDs)
    ]

    payload = {
        "operation":"decrement"
    }

    for product in final_products:
        for _ in range(0, int(product["quantity"])):
            url = f"{os.getenv('API_URL')}/cart/decrement/{product['_id']}"
            response = requests.post(url, cookies=cookies, json=payload)

            data = response.json()

    return data["message"]

decrement_quantity_interface = {
    "type": "function",
    "function": {
        "name": "decrement_quantity",
        "description": "Decrease the quantity of one or more products in the user's shopping cart. Use this when the user asks to remove, decrease, reduce, subtract, or take products out of their cart.",
        "parameters": {
            "type": "object",
            "properties": {
                "products": {
                    "type": "array",
                    "description": "List of products whose quantities should be decreased.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the product to remove"
                            },
                            "quantity": {
                                "type": "integer",
                                "description": "Amount by which to decrease the quantity."
                            }
                        },
                        "required": ["name", "quantity"]
                    }
                }
            },
            "required": ["products"]
        }
    }
}