import requests
from config import API_URL, cookies
from utils import find_product_id

def add_review(product_name, review, stars):
    product_res = find_product_id(product_name)
    if not product_res["success"]:
        return product_res["message"]
    
    product_id = product_res["message"]
    url = f"{API_URL}/review/post/{product_id}"
    
    try:
        response = requests.post(url, cookies=cookies, json={
            "review": review,
            "stars": int(stars)
        })
        return response.json().get("message", "Review request finished.")
    except Exception as e:
        return f"Error adding review: {str(e)}"

add_review_interface = {
    "type": "function",
    "function": {
        "name": "add_review",
        "description": "Add/post a product review with a rating in stars and written review text. Use this when the user explicitly requests to review, rate, write a review, or leave feedback for a product. DO NOT write a review yourself, just ask user and post it",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The name of the product to review."
                },
                "review": {
                    "type": "string",
                    "description": "The text content of the review."
                },
                "stars": {
                    "type": "integer",
                    "description": "The rating/stars given to the product (from 1 to 5).",
                    "minimum": 1,
                    "maximum": 5
                }
            },
            "required": ["product_name", "review", "stars"]
        }
    }
}
