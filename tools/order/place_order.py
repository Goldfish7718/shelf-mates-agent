import requests
from config import API_URL, cookies
from urllib.parse import urlparse, parse_qs

def place_order(payment_method, address_id):
    checkout_url = f"{API_URL}/order/checkout"

    response_1 = requests.post(checkout_url, cookies=cookies, json={
        "paymentMethod": payment_method,
        "address": address_id
    })

    response_1 = response_1.json()

    if payment_method == "COD":
        parsed_url = urlparse(response_1["url"])

        encodedOrderDetails = parse_qs(parsed_url.query).get("orderId", [None])[0]

        confirm_url = f"{API_URL}/order/confirmorder/{encodedOrderDetails}"
        response = requests.post(confirm_url, cookies=cookies)

        print("ORDER CONFIRMATION RESPONSE\n\n", response)
        
        response = response.json()

        final_response = {
            "message": f"{response['message']} Total: INR {response['orderObject']['Subtotal']}"
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
                "address_id": {
                    "type": "string",
                    "description": (
                        "The ID of the delivery address where the order should be shipped."
                    )
                }
            },
            "required": [
                "payment_method",
                "address_id"
            ]
        }
    }
}