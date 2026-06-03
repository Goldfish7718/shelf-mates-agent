import requests
from config import API_URL, cookies

def add_address(address):
    url = f"{API_URL}/address/addaddress"
    response = requests.post(url, cookies=cookies, json=address)

    response = response.json()
    return response["message"]

add_address_interface = {
    "type": "function",
    "function": {
        "name": "add_address",
        "description": (
            "Add a delivery address to the user's account. "
            "Use this whenever the user wants to add, save, create, "
            "or register a new delivery address."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "address": {
                    "type": "object",
                    "properties": {
                        "addressLine1": {
                            "type": "string",
                            "description": "Primary address line including house number, flat number, building name, etc."
                        },
                        "landmark": {
                            "type": "string",
                            "description": "Nearby landmark to help locate the address."
                        },
                        "city": {
                            "type": "string",
                            "description": "City name."
                        },
                        "state": {
                            "type": "string",
                            "description": "State name."
                        },
                        "type": {
                            "type": "string",
                            "description": "Type of Addres (eg. Home, Office, Other). Default will be 'Home'"
                        }
                    },
                    "required": [
                        "addressLine1",
                        "landmark",
                        "city",
                        "state"
                    ]
                }
            },
            "required": ["address"]
        }
    }
}