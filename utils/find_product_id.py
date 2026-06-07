from rapidfuzz import process, fuzz
from config import API_URL, cookies
import requests

def find_product_id(query, threshold=70):
    print("Fetching products...\n")
    products_url = f"{API_URL}/products/all"

    response = requests.get(products_url, cookies=cookies)
    response.raise_for_status()

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
        return None

    matched_name, score, index = result

    if score < threshold:
        return None

    print(products_data[index]["_id"])
    return products_data[index]["_id"]