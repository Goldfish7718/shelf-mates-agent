import requests
from config import cookies, API_URL

def delete_address(address_id):
    url = f"{API_URL}/address/{address_id}"
    response = requests.delete(url, cookies=cookies)

    response = response.json()
    return response["message"]

delete_address_interface = {
    "type": "function",
    "function": {
        "name": "delete_address",
        "description": "Use this whenever the user asks to delete or remove an address. You must use get_addresses tool to fetch the ID of the address that the user wants to delete.",
        "parameters": {
            "type": "object",
            "properties": {
                "address_id": {
                    "type": "string",
                    "description": "ID of the address to delete."
                }
            },
            "required": [
                "address_id"
            ]
        }
    }
}