from openai import OpenAI
from tools import product, cart, address, order
from config import MODEL
import json

messages = [
    {
        "role": "system",
        "content": """
        You are Shelf-Mates AI, a grocery shopping assistant.

        IMPORTANT RULES:

        1. NEVER make up information.
        2. NEVER guess product IDs, address IDs, cart contents, prices, quantities, or order details.
        3. If information is needed and a tool exists to obtain it, CALL THE TOOL.
        4. Use ONLY the tool arguments defined in the tool schema.
        5. NEVER invent extra arguments.
        6. NEVER rename arguments.
        7. NEVER call a tool with missing required arguments.
        8. If required information is missing, ask the user a question instead of guessing.

        TOOL USAGE RULES:

        PRODUCTS
        - To browse products by category, use get_products_by_category.
        - To see details of a specific product, use get_product_detail.

        CART
        - To add items, use add_to_cart.
        - If the user asks to empty their cart, first use get_cart tool to fetch cart information and pass the relevant parameters to the decrement_quantity tool
        - Never assume a product exists.

        ADDRESSES
        - To view saved addresses, use get_addresses.
        - To create an address, use add_address.
        - To modify an address, use update_address.
        - To remove an address, use delete_address.

        ORDERS
        - Before placing an order, verify that the user has items in the cart.
        - If the user refers to an address by name (home, office, flat 201, etc.) and the address ID is unknown, first call get_addresses.
        - Never invent an address ID.
        - Never invent an order ID.

        TOOL CALLING BEHAVIOR

        When a tool can answer the user's request:
        - Call the tool immediately.
        - Do not explain what tool you will call.
        - Do not ask for confirmation unless necessary.
        - Do not provide a final answer until tool results are received.

        After receiving tool results:
        - Use the results.
        - If another tool is needed, call it.
        - Continue until the task is complete.

        OUTPUT RULES

        - Be concise.
        - Do not expose internal reasoning.
        - Do not describe tool schemas.
        - Do not hallucinate.
        - When uncertain, use a tool or ask a question.

        Your goal is to successfully complete shopping tasks using the available tools.
        """
    }
]

tools_interface = [
    # PRODUCT OPS
    product.get_by_category_interface,
    product.get_product_detail_interface,

    #CART OPS
    cart.add_to_cart_interface,
    cart.get_cart_interface,
    cart.decrement_quantity_interface,

    # ADDRESS OPS
    address.add_address_interface,
    address.get_addresses_interface,
    address.update_address_interface,
    address.delete_address_interface,

    #ORDER OPS
    order.place_order_interface
]

TOOL_MAPPING = {
    # PRODUCTS
    "get_products_by_category": product.get_by_category,
    "get_product_detail": product.get_product_detail,
    
    # CART
    "add_to_cart": cart.add_to_cart,
    "get_cart": cart.get_cart,
    "decrement_quantity": cart.decrement_quantity,

    # ADDRESS
    "add_address": address.add_address,
    "get_addresses": address.get_addresses,
    "update_address": address.update_address,
    "delete_address": address.delete_address,

    #ORDER OPS
    "place_order": order.place_order
}

MAX_AGENT_STEPS = 20

def main():
    try:
        while True:
            prompt = input("YOU: ")

            if prompt.lower() in ["exit", "quit", "bye"]:
                print("Goodbye!")
                break

            messages.append({
                "role": "user",
                "content": prompt
            })

            client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama"
            )

            for _ in range(MAX_AGENT_STEPS):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=tools_interface,
                    tool_choice="auto",
                    temperature=0.1
                )

                print("\nModel used for completion:", MODEL)
                message = response.choices[0].message
                messages.append(message)

                # Final answer reached
                if not message.tool_calls:
                    print("CHATBOT:", message.content, "\n")
                    break

                # Execute all tool calls
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    print(f"\n[TOOL] {tool_name}")

                    tool_args = json.loads(tool_call.function.arguments)
                    print("ARGS:", tool_args)

                    tool_response = TOOL_MAPPING[tool_name](**tool_args)
                    print("RESULT:", tool_response)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_response)
                    })

            else:
                print(
                    f"\nAgent stopped after "
                    f"{MAX_AGENT_STEPS} steps "
                    f"(possible infinite loop).\n"
                )

    except Exception as e:
        print(f"\nERROR: {e}\n")
        raise

    finally:
        formatted_messages = []

        for msg in messages:
            if hasattr(msg, "model_dump"):
                formatted_messages.append(msg.model_dump())
            else:
                formatted_messages.append(msg)

        with open("debug_messages.json", "w") as f:
            json.dump(
                formatted_messages,
                f,
                indent=4,
                default=str
            )

        print("\nMESSAGE HISTORY:\n\n", json.dumps(formatted_messages, indent=4, default=str))


if __name__ == "__main__":
    main()