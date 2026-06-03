import requests
from config import API_URL, cookies

def get_addresses():
    url = f"{API_URL}/address/getaddresses"
    response = requests.get(url, cookies=cookies)

    response = response.json()
    return response["addresses"]

get_addresses_interface = {
    "type": "function",
    "function": {
        "name": "get_addresses",
        "description": (
            "Fetch all delivery addresses saved by the user. "
            "Use this whenever the user asks to view, list, show, "
            "check, inspect, or review their saved addresses."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}