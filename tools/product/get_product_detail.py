import requests
from config import API_URL, cookies
import json
from openai import OpenAI

def get_product_detail(product_name):
    print("Fetching products...\n")
    products_url = f"{API_URL}/products/all"

    response = requests.get(products_url, cookies=cookies)
    response.raise_for_status()

    products_data = response.json()

    messages = [
        {
            "role": "system",
            "content": f"You are given the following product name {product_name} and the database containing the IDs of all products. Return the corresponding ID of the product name given to you WITHOUT attaching bactics or any extra characters. EXAMPLE RESPONSE: 65300858022e0de3fd4a4814"
        },
        {
            "role": "user",
            "content": str(products_data)
        }
    ]

    print("Extracting ID...\n")

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

    response = client.chat.completions.create(
        model="qwen2.5:3b",
        messages=messages,
    )

    product_id = response.choices[0].message.content
    
    url = f"{API_URL}/products/getProduct/{product_id}"
    response = requests.get(url, cookies=cookies)

    response.raise_for_status()

    data = response.json()

    product = data["transformedProduct"]

    EXCLUDED_FIELDS = {
        "image",
        "__v"
    }

    product = {
        key: value
        for key, value in product.items()
        if key not in EXCLUDED_FIELDS
    }

    print(json.dumps(product, indent = 4))
    return product


get_product_detail_interface = {
    "type": "function",
    "function": {
        "name": "get_product_detail",
        "description": "Use this when the customer asks more information about one or more products. This tool will automatically fetch the IDs of the product.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product to fetch details of"
                }
            },
            "required": ["product_name"]
        }
    }
}