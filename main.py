from openai import OpenAI
from tools import product, cart, address, order
from config import MODELS
import os
import json

messages = [
    {
        "role": "system",
        "content": """
            You are an e-commerce grocery assistant.
            
            IMPORTANT:
            - Never guess cart contents.
            - Never guess available products.
            - Never guess addresses.
            - When information is available through a tool, ALWAYS call the appropriate tool.

            Do not answer from memory.
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

            with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:

                for _ in range(MAX_AGENT_STEPS):
                    response = client.chat.send(
                        # model="openai/gpt-oss-120b:free",
                        # model="z-ai/glm-4.5-air:free",
                        models=MODELS,
                        messages=messages,
                        tools=tools_interface,
                        retries=2
                    )

                    print("Model used for completion:", response.model)
                    message = response.choices[0].message
                    messages.append(message)

            for _ in range(MAX_AGENT_STEPS):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=tools_interface
                )

                print("Model used for completion:", response.model)
                message = response.choices[0].message
                messages.append(message)

                # Final answer reached
                if not message.tool_calls:
                    print("\nCHATBOT:", message.content, "\n")
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

        print(
            "\nMESSAGE HISTORY:\n\n",
            json.dumps(
                formatted_messages,
                indent=4,
                default=str
            )
        )


if __name__ == "__main__":
    main()