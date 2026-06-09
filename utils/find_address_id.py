import requests
from config import API_URL, cookies
from rapidfuzz import process, fuzz
import re

def find_address_id(query, threshold=60):
    url = f"{API_URL}/address/getaddresses"
    response = requests.get(url, cookies=cookies)

    if response.status_code != 200:
        return {
            "success": False,
            "message": response.json()["message"]
        }


    address_data = response.json()["addresses"]

    print("Extracting ID...")
    query = query.lower()

    search_strings = []

    for address in address_data:
        search_text = " ".join([
            address["type"],
            address["addressLine1"],
            address["landmark"],
            address["city"],
            address["state"]
        ]).lower()

        search_text = re.sub(r"[^\w\s]", "", search_text)
        search_strings.append(search_text)

    result = process.extractOne(
        query,
        search_strings,
        scorer=fuzz.token_set_ratio
    )

    print(result)

    if result is None:
        return {
            "success": False,
            "message": "No address found"
        }

    _, score, index = result

    if score < threshold:
        return {
            "success": False,
            "message": "No product found in database"
        }

    print(address_data[index]["_id"])
    return {
        "success": True,
        "message": address_data[index]
    }