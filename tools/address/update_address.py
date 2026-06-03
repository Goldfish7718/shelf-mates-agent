import requests
from config import API_URL, cookies

address = {
    "_id": "6a1f17c8debb1232f56fe6ca",
    "addressLine1": "Flat no 4, Shri darshan apartment",
    "landmark": "Near Navkar Hospital, Govind Nagar",
    "city": "Nashik",
    "state": "Maharashtra",
    "userId": "6a16d72fc1b01b4f66ce29ab",
    "type": "Home"
}

def update_address(address=address):
    url = f"{API_URL}/address/updateaddress"
    response = requests.put(url, cookies=cookies, json={ "address": address })

    response = response.json()
    return response["message"]

update_address_interface = {
    "type": "function",
    "function": {
        "name": "update_address",
        "description": (
            "Update an exisiting delivery address. "
            "Use this whenever the user wants to update or change one of their exisiting delivery addresses"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "address": {
                    "type": "object",
                    "properties": {
                        "_id": {
                            "type": "string",
                            "description": "ID of the address in the database. To fetch the ID, you will first need to call get_addresses tool and extract the ID with whatever relevant information provided by the user."
                        },
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
                        "_id",
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