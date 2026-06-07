import requests
from config import API_URL, cookies, MODELS
import json
from utils import find_product_id

def get_product_detail(product_name):
    product_id = find_product_id(product_name)
    
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