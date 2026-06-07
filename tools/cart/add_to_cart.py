import requests
from config import API_URL, cookies
from utils import find_product_id

def add_to_cart(products):
    for product in products:
        product_IDs = []

        product_id = find_product_id(product["name"])
        product_IDs.append(product_id)

    final_products = [
        {
            "product_id": product_id,
            "quantity": product["quantity"]
        }

        for product, product_id in zip(products, product_IDs)
    ]

    print("Adding to Cart...\n")
    for product in final_products:
        for _ in range(0, product["quantity"]):
            add_to_cart_url = f"{API_URL}/cart/add/{product['product_id']}"

            response = requests.post(add_to_cart_url, cookies=cookies)
            response.raise_for_status()

            data = response.json()

    return data["message"]
    
add_to_cart_interface = {
    "type": "function",
    "function": {
        "name": "add_to_cart",
        "description": "Add products directly to the user's shopping cart. This function automatically finds the correct products and quantities. Do not call get_products_by_category before using this function. Use this whenever the user wants to add, buy, put, include, or place products in their cart.",
        "parameters": {
            "type": "object",
            "properties": {
                "products": {
                    "type": "array",
                    "description": "List of products to add to the cart.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the product."
                            },
                            "quantity": {
                                "type": "integer",
                                "description": "Quantity of the product to add."
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