import json
from dotenv import load_dotenv
from tools.product import get_by_category, get_product_detail
from tools.cart import add_to_cart, get_cart, decrement_quantity
from tools.address import add_address, get_addresses, update_address, delete_address
from tools.order import place_order
from tools.review import add_review, get_reviews
from utils import find_product_id, find_address_id

load_dotenv()

message = (
    "Select script to execute:\n"
    "1. get_by_category\n"
    "2. get_product_detail\n"
    "3. add_to_cart\n"
    "4. get_cart\n"
    "5. decrement_quantity\n"
    "6. add_address\n"
    "7. get_addresses\n"
    "8. update_address\n"
    "9. delete_address\n"
    "10. place_order\n"
    "11. find_product_id\n"
    "12. find_address_id\n"
    "13. add_review\n"
    "14. get_reviews\n"
    "Selection: "
)

selection = input(message)

def print_result(result):
    print("\n--- RESULT ---")
    if isinstance(result, (dict, list)):
        print(json.dumps(result, indent=4))
    else:
        print(result)
    print("--------------\n")

try:
    choice = int(selection)
except ValueError:
    print("Invalid selection. Please enter a number.")
    exit(1)

match choice:
    case 1:
        category = input("Enter category [fruits]: ") or "fruits"
        res = get_by_category(category)
        print_result(res)

    case 2:
        product_name = input("Product Name [apple]: ") or "apple"
        res = get_product_detail(product_name)
        print_result(res)

    case 3:
        products_str = input('Products JSON [[{"name": "apple", "quantity": 1}]]: ') or '[{"name": "apple", "quantity": 1}]'
        try:
            products = json.loads(products_str)
        except Exception as e:
            print(f"Invalid JSON: {e}. Using default.")
            products = [{"name": "apple", "quantity": 1}]
        res = add_to_cart(products)
        print_result(res)

    case 4:
        res = get_cart()
        print_result(res)

    case 5:
        products_str = input('Products JSON [[{"name": "apple", "quantity": 1}]]: ') or '[{"name": "apple", "quantity": 1}]'
        try:
            products = json.loads(products_str)
        except Exception as e:
            print(f"Invalid JSON: {e}. Using default.")
            products = [{"name": "apple", "quantity": 1}]
        res = decrement_quantity(products)
        print_result(res)

    case 6:
        address_str = input('Address JSON [{"addressLine1": "123 Main St", "landmark": "Near Park", "city": "Nashik", "state": "Maharashtra", "type": "Home"}]: ') or '{"addressLine1": "123 Main St", "landmark": "Near Park", "city": "Nashik", "state": "Maharashtra", "type": "Home"}'
        try:
            address = json.loads(address_str)
        except Exception as e:
            print(f"Invalid JSON: {e}. Using default.")
            address = {"addressLine1": "123 Main St", "landmark": "Near Park", "city": "Nashik", "state": "Maharashtra", "type": "Home"}
        res = add_address(address)
        print_result(res)

    case 7:
        res = get_addresses()
        print_result(res)

    case 8:
        address_str = input('Address JSON [default]: ')
        if address_str:
            try:
                address = json.loads(address_str)
                res = update_address(address)
            except Exception as e:
                print(f"Invalid JSON: {e}. Using default.")
                res = update_address()
        else:
            res = update_address()
        print_result(res)

    case 9:
        address = input("Address to delete [123 main st, near park, nashik, maharashtra]: ") or "123 main st, near park, nashik, maharashtra"
        res = delete_address(address)
        print_result(res)

    case 10:
        payment_method = input("Payment Method [COD]: ") or "COD"
        address = input("Address Search Query [Home]: ") or "Home"
        res = place_order(payment_method, address)
        print_result(res)

    case 11:
        query = input("Search query [apple]: ") or "apple"
        res = find_product_id(query=query)
        print_result(res)

    case 12:
        query = input("Search query [Home]: ") or "Home"
        res = find_address_id(query=query)
        print_result(res)

    case 13:
        product_name = input("Product Name [apple]: ") or "apple"
        review_text = input("Review text [Great product!]: ") or "Great product!"
        stars = input("Stars [5]: ") or "5"
        res = add_review(product_name, review_text, stars)
        print_result(res)

    case 14:
        product_name = input("Product Name [apple]: ") or "apple"
        res = get_reviews(product_name)
        print_result(res)

    case _:
        print("Selection not implemented.")
