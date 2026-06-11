import requests
from config import API_URL, cookies
from utils import find_product_id

def add_to_cart(products):
    product_IDs = []

    for product in products:
        result = find_product_id(product["name"])

        if not result["success"]:
            return result["message"]

        product_IDs.append(result["message"])

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
            add_to_cart_url = f"{API_URL}/cart/increment/{product['product_id']}"

            response = requests.patch(add_to_cart_url, cookies=cookies)

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