import requests
from openrouter import OpenRouter
import ast
from config import API_URL, cookies
import os

def add_to_cart(products = []):
    print("Fetching products...\n")
    products_url = f"{API_URL}/products/all"

    response = requests.get(products_url, cookies=cookies)
    response.raise_for_status()

    products_data = response.json()
    product_names = [product["name"] for product in products]

    messages = [
        {
            "role": "system",
            "content": f"You are given the following product names {product_names} and the database containing the IDs of all products. Return the corresponding IDs of the product names given to you in a python list format WITHOUT attaching bactics or any extra characters. EXAMPLE RESPONSE: ['65300858022e0de3fd4a4814', '65a575190359a6c5cb58737a']"
        },
        {
            "role": "user",
            "content": str(products_data)
        }
    ]

    print("Extracting IDs...\n")
    with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
        response = client.chat.send(
            models=["openai/gpt-oss-120b:free", "z-ai/glm-4.5-air:free"],
            messages = messages,
        )

        product_IDs = ast.literal_eval(response.choices[0].message.content)

    final_products = [
        {
            "product_id": product_id,
            "quantity": int(product["quantity"])
        }

        for product, product_id in zip(products, product_IDs)
    ]

    print("Adding to Cart...\n")
    for product in final_products:
        for _ in range(0, product["quantity"]):
            add_to_cart_url = f"{os.getenv('API_URL')}/cart/add/{product['product_id']}"

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
                                "type": "string",
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