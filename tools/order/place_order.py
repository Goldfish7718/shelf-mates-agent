import requests
from config import API_URL, cookies
from urllib.parse import urlparse, parse_qs
from utils import find_address_id

def place_order(payment_method, address):
    response = find_address_id(query=address)

    if not response["success"]:
        return response["message"]
    
    address_id = response["message"]["_id"]
    checkout_url = f"{API_URL}/order/checkout"

    response_1 = requests.post(checkout_url, cookies=cookies, json={
        "paymentMethod": payment_method,
        "address": address_id
    })

    if response_1.status_code != 200:
        return response_1.json()["message"]

    response_1 = response_1.json()

    if payment_method == "COD":
        parsed_url = urlparse(response_1["url"])

        encodedOrderDetails = parse_qs(parsed_url.query).get("orderId", [None])[0]

        confirm_url = f"{API_URL}/order/confirmorder/{encodedOrderDetails}"
        response = requests.post(confirm_url, cookies=cookies)

        if response.status_code != 200:
            return response.json()["message"]
        
        response = response.json()

        final_response = {
            "message": f"{response['message']} Total: INR {response['orderObject']['subtotal']}"
        }

        return final_response["message"]

    else:
        return f"Card Payments cannot be completed here. Please click this link to open the payment page. {response_1['url']}"
    
place_order_interface = {
    "type": "function",
    "function": {
        "name": "place_order",
        "description": (
            "Place an order using a selected payment method and delivery address. "
            "Use this when the user wants to checkout, place an order, buy the items "
            "in their cart, or complete a purchase."
            "DO NOT use the get_addresses tool to fetch addresses. Just put whatever information you have about the address to be delivered on in the 'address' parameter. This tool will automatically resolve addresses."
            "For example if the user says 'deliver it to my home' you will put 'home' as the address parameter. If the user says 'deliver it to my san fransisco address' you will put 'san fransisco' in the address parameter."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "payment_method": {
                    "type": "string",
                    "description": (
                        "Payment method to use. "
                        "Valid values are 'COD' (Cash on Delivery) and 'CARD'."
                    ),
                    "enum": ["COD", "Card"]
                },
                "address": {
                    "type": "string",
                    "description": (
                        "search query of the address the user provides as their delivery address."
                    )
                }
            },
            "required": [
                "payment_method",
                "address"
            ]
        }
    }
}