from rapidfuzz import process, fuzz
from config import API_URL, cookies
import requests

def find_product_id(query, threshold=60):
    print("Fetching products...\n")
    products_url = f"{API_URL}/products/all"

    response = requests.get(products_url, cookies=cookies)

    if response.status_code != 200:
        return {
            "success": False,
            "message": response.json()["message"]
        }

    products_data = response.json()["products"]

    print("Extracting ID...")
    query = query.lower()
    product_names = [product["name"].lower() for product in products_data]

    result = process.extractOne(
        query,
        product_names,
        scorer=fuzz.token_set_ratio
    )

    print(result)

    if result is None:
        return {
            "success": False,
            "message": "No product found"
        }

    _, score, index = result

    if score < threshold:
        return {
            "success": False,
            "message": "No product found in database"
        }

    print(products_data[index]["_id"])
    return {
        "success": True,
        "message": products_data[index]["_id"]
    }