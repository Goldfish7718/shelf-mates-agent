import os
import requests
import ast
from config import API_URL, cookies
from openai import OpenAI

def decrement_quantity(products):
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
    
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

    response = client.chat.completions.create(
        model="qwen2.5:3b",
        messages=messages,
    )

    product_IDs = ast.literal_eval(response.choices[0].message.content)
    print(f"Extracted IDs: {product_IDs}")

    final_products = [
        {
            "_id": product_id,
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
            print(data["message"])

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
                                "type": "string",
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