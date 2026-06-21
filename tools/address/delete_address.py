import requests
from config import cookies, API_URL
from utils import find_address_id

def delete_address(address):
    response = find_address_id(query=address)

    if not response["success"]:
        return response["message"]
    
    address_id = response["message"]["_id"]

    url = f"{API_URL}/address/{address_id}"
    response = requests.delete(url, cookies=cookies)

    if response.status_code != 200:
        return response.json()["message"]

    response = response.json()
    return response["message"]

delete_address_interface = {
    "type": "function",
    "function": {
        "name": "delete_address",
        "description": (
            "Use this whenever the user asks to delete or remove an address."
            "DO NOT use the get_addresses tool to fetch addresses. Just put whatever information you have about the address to be delivered on in the 'address' parameter. This tool will automatically resolve addresses."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "address": {
                    "type": "string",
                    "description": (
                        "search query of the address the user wants to delete."
                    )
                }
            },
            "required": [
                "address"
            ]
        }
    }
}