from dotenv import load_dotenv
from tools.product import get_by_category, get_product_detail
from tools.cart import add_to_cart, get_cart, decrement_quantity
from tools.address import add_address, get_addresses, update_address, delete_address
from tools.order import place_order
from utils import find_product_id, find_address_id

load_dotenv()

message = \
"Select script to execute:\n" \
"1. get_by_category\n" \
"2. get_product_detail\n" \
"3. add_to_cart\n" \
"4. get_cart\n" \
"5. decrement_quantity\n" \
"6. add_address\n" \
"7. get_addresses\n" \
"8. update_address\n" \
"9. delete_address\n" \
"10. place_order\n" \
"11. find_product_id\n" \
"12. find_address_id\n" \

selection = input(message)

match int(selection):
    case 1:
        category = input("Enter category")
        get_by_category(category)

    case 2:
        product_name = input("Product Name: ")
        get_product_detail(product_name)

    case 3:
        add_to_cart()

    case 4:
        get_cart()

    case 5:
        decrement_quantity()

    case 6:
        add_address()

    case 7:
        get_addresses()

    case 8:
        update_address()

    case 9:
        address_id = input("Address ID: ")
        delete_address(address_id)

    case 10:
        place_order("COD", "6a1f147ddebb1232f56fe6ba")        

    case 11:
        query = input("Search query: ")
        find_product_id(query=query)

    case 12:
        query = input("Search query: ")
        find_address_id(query=query)


