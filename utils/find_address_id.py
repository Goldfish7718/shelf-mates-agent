import requests
from config import API_URL, cookies
from rapidfuzz import process, fuzz

def find_address_id(query, threshold=60):
    url = f"{API_URL}/address/getaddresses"
    response = requests.get(url, cookies=cookies)

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

        search_strings.append(search_text)

    result = process.extractOne(
        query,
        search_strings,
        scorer=fuzz.token_set_ratio
    )

    print(result)

    if result is None:
        return "No product Found"

    _, score, index = result

    if score < threshold:
        return "No product found in the database"

    print(address_data[index]["_id"])
    return address_data[index]["_id"]