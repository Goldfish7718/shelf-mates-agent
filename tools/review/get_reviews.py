import requests
from config import API_URL, cookies
from utils import find_product_id

def get_reviews(product_name, limit=10, skip=0):
    product_res = find_product_id(product_name)
    if not product_res["success"]:
        return product_res["message"]
    
    product_id = product_res["message"]
    url = f"{API_URL}/review/{product_id}"
    
    try:
        response = requests.get(url, cookies=cookies, params={"limit": limit, "skip": skip})
        if response.status_code != 200:
            return response.json().get("message", "Failed to retrieve reviews.")
            
        data = response.json()
        reviews = data.get("transformedReviews", [])
        
        clean_reviews = []
        for r in reviews:
            clean_reviews.append({
                "reviewer": f"{r.get('fName', '')} {r.get('lName', '')}".strip() or "Anonymous",
                "stars": r.get("stars"),
                "review": r.get("review")
            })
        return clean_reviews
    except Exception as e:
        return f"Error fetching reviews: {str(e)}"

get_reviews_interface = {
    "type": "function",
    "function": {
        "name": "get_reviews",
        "description": "Retrieve existing reviews/ratings for a specific product. Use this when the user asks to see, check, read, or get reviews/feedback for a product.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The name of the product to fetch reviews for."
                },
                "limit": {
                    "type": "integer",
                    "description": "Optional maximum number of reviews to return (default is 10)."
                },
                "skip": {
                    "type": "integer",
                    "description": "Optional number of reviews to skip for pagination (default is 0)."
                }
            },
            "required": ["product_name"]
        }
    }
}
