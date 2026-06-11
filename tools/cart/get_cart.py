import requests
from config import API_URL, cookies

def get_cart():
    print("Fetching Cart...\n")
    url = f"{API_URL}/cart"

    response = requests.get(url, cookies=cookies)
    
    if response.status_code != 200:
                return response.json()["message"]

    data = response.json()

    EXCLUDED_FIELDS = [
        "image",
        "productId",
        "_id"
    ]

    transformed_cart = {
        "items": [],
        "subtotal": data["subtotal"]
    }

    for item in data.get("transformedCart", []):
        filtered_item = {
            k: v
            for k, v in item.items()
            if k not in EXCLUDED_FIELDS
        }

        transformed_cart["items"].append(filtered_item)

    return transformed_cart

get_cart_interface = {
    "type": "function",
    "function": {
        "name": "get_cart",
        "description": "Fetch the user's current shopping cart, including all items and the cart subtotal. Use this whenever the user asks to view, show, check, inspect, or review their cart.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}