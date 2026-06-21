import os
import json
from openrouter import OpenRouter
from tools import product, cart, address, order, review
from config import MODELS

MAX_AGENT_STEPS = 20

SYSTEM_MESSAGE = {
    "role": "system",
    "content": """
        You are an e-commerce grocery assistant.
        Your name is Shelf-mates AI.
        DO NOT use emojis in responses.
        Keep the responses simple and casual/professional.
        ALWAYS use table for displaying information about products.
        ALWAYS respond in MARKDOWN.
        """
}

tools_interface = [
    # PRODUCT OPS
    product.get_by_category_interface,
    product.get_product_detail_interface,

    # CART OPS
    cart.add_to_cart_interface,
    cart.get_cart_interface,
    cart.decrement_quantity_interface,

    # ADDRESS OPS
    address.add_address_interface,
    address.get_addresses_interface,
    address.update_address_interface,
    address.delete_address_interface,

    # ORDER OPS
    order.place_order_interface,

    # REVIEW OPS
    review.add_review_interface,
    review.get_reviews_interface
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

    # ORDER OPS
    "place_order": order.place_order,

    # REVIEWS
    "add_review": review.add_review,
    "get_reviews": review.get_reviews
}

def get_loading_phrase(tool_name: str, tool_args: dict) -> str:
    match tool_name:
        case "get_products_by_category":
            category = tool_args.get("category", "products")
            return f"Searching for products in category: {category}..."
        case "get_product_detail":
            product_name = tool_args.get("product_name", "product")
            return f"Looking up details for '{product_name}'..."
        case "add_to_cart":
            products = tool_args.get("products", [])
            if len(products) == 1:
                p = products[0]
                return f"Adding {p.get('quantity', 1)} {p.get('name', 'product')}(s) to your cart..."
            elif len(products) > 1:
                return f"Adding {len(products)} items to your cart..."
            return "Adding items to your cart..."
        case "get_cart":
            return "Retrieving your cart items..."
        case "decrement_quantity":
            products = tool_args.get("products", [])
            if len(products) == 1:
                p = products[0]
                return f"Removing {p.get('quantity', 1)} {p.get('name', 'product')}(s) from your cart..."
            elif len(products) > 1:
                return f"Removing items from your cart..."
            return "Updating cart items..."
        case "add_address":
            return "Saving new delivery address..."
        case "get_addresses":
            return "Retrieving your delivery addresses..."
        case "update_address":
            return "Updating your delivery address..."
        case "delete_address":
            return "Deleting address from your profile..."
        case "place_order":
            payment_method = tool_args.get("payment_method", "selected payment method")
            return f"Placing your order using {payment_method}..."
        case "add_review":
            product_name = tool_args.get("product_name", "product")
            return f"Adding review for '{product_name}'..."
        case "get_reviews":
            product_name = tool_args.get("product_name", "product")
            return f"Retrieving reviews for '{product_name}'..."
        case _:
            return "Executing task..."

def _run_agent_stream(message: str, history: list = None):
    """
    Executes the e-commerce grocery agent and yields event dictionaries during execution.
    Yields events:
      - {"type": "content", "delta": str}
      - {"type": "tool_call", "index": int, "name": str, "name_delta": str, "arguments_delta": str}
      - {"type": "tool_execute_start", "name": str, "arguments": str}
      - {"type": "tool_execute_end", "name": str, "arguments": str, "result": Any}
      - {"type": "error", "content": str}
      - {"type": "done", "response": str, "history": list}
    """
    if history is None:
        messages = [SYSTEM_MESSAGE]
    else:
        # Copy history list to avoid mutating the input parameter
        messages = list(history)
        # Verify if system message exists, otherwise prepend it
        has_system = any(msg.get("role") == "system" for msg in messages)
        if not has_system:
            messages.insert(0, SYSTEM_MESSAGE)

    # Append user message
    messages.append({
        "role": "user",
        "content": message
    })

    final_response = "No response generated by the agent."
    formatted_messages = []

    try:
        with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
            for _ in range(MAX_AGENT_STEPS):
                response_stream = client.chat.send(
                    models=MODELS,
                    messages=messages,
                    tools=tools_interface,
                    stream=True,
                    retries=2
                )

                accumulated_content = ""
                active_tool_calls = {}

                for chunk in response_stream:
                    if not chunk.choices:
                        continue
                    choice = chunk.choices[0]
                    delta = choice.delta
                    if not delta:
                        continue

                    # 1. Handle content delta
                    if delta.content is not None and isinstance(delta.content, str) and delta.content != "":
                        accumulated_content += delta.content
                        yield {
                            "type": "content",
                            "delta": delta.content
                        }

                    # 2. Handle tool calls delta
                    if delta.tool_calls:
                        for tool_call in delta.tool_calls:
                            idx = tool_call.index
                            if idx not in active_tool_calls:
                                active_tool_calls[idx] = {
                                    "id": "",
                                    "name": "",
                                    "arguments": ""
                                }

                            name_delta = ""
                            args_delta = ""

                            if tool_call.id:
                                active_tool_calls[idx]["id"] = tool_call.id
                            if tool_call.function:
                                if tool_call.function.name:
                                    active_tool_calls[idx]["name"] += tool_call.function.name
                                    name_delta = tool_call.function.name
                                if tool_call.function.arguments:
                                    active_tool_calls[idx]["arguments"] += tool_call.function.arguments
                                    args_delta = tool_call.function.arguments

                            yield {
                                "type": "tool_call",
                                "index": idx,
                                "name": active_tool_calls[idx]["name"],
                                "name_delta": name_delta,
                                "arguments_delta": args_delta
                            }

                # Construct assistant message and append to messages history
                assistant_msg = {
                    "role": "assistant",
                    "content": accumulated_content if accumulated_content else None
                }
                if active_tool_calls:
                    assistant_msg["tool_calls"] = [
                        {
                            "id": tc["id"],
                            "type": "function",
                            "function": {
                                "name": tc["name"],
                                "arguments": tc["arguments"]
                            }
                        }
                        for tc in active_tool_calls.values()
                    ]
                messages.append(assistant_msg)

                # Execute tool calls if any, then loop back
                if active_tool_calls:
                    skip_generation = False
                    skip_response = ""
                    for tc in active_tool_calls.values():
                        tool_name = tc["name"]
                        tool_args_str = tc["arguments"]
                        tool_id = tc["id"]

                        # Parse arguments first to generate a contextual step message
                        try:
                            tool_args = json.loads(tool_args_str) if tool_args_str else {}
                        except Exception as e:
                            tool_args = {}
                            print(f"Failed to parse tool arguments: {e}")

                        yield {
                            "type": "tool_execute_start",
                            "name": tool_name,
                            "arguments": tool_args_str,
                            "step": get_loading_phrase(tool_name, tool_args)
                        }

                        if tool_name in TOOL_MAPPING:
                            try:
                                tool_response = TOOL_MAPPING[tool_name](**tool_args)
                            except Exception as e:
                                tool_response = f"Error executing tool '{tool_name}': {str(e)}"
                        else:
                            tool_response = f"Error: Tool '{tool_name}' is not supported."

                        yield {
                            "type": "tool_execute_end",
                            "name": tool_name,
                            "arguments": tool_args_str,
                            "result": tool_response
                        }

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_id,
                            "content": json.dumps(tool_response)
                        })

                        if tool_name == "place_order" and tool_args.get("payment_method", "").lower() == "card":
                            skip_generation = True
                            skip_response = tool_response

                    if skip_generation:
                        yield {
                            "type": "content",
                            "delta": skip_response
                        }
                        messages.append({
                            "role": "assistant",
                            "content": skip_response
                        })
                        final_response = skip_response
                        break
                else:
                    # Final text response finished generating
                    final_response = accumulated_content
                    break
            else:
                final_response = f"Agent stopped after {MAX_AGENT_STEPS} steps (possible infinite loop)."
                yield {
                    "type": "error",
                    "content": final_response
                }

    except Exception as e:
        print(f"\nERROR: {e}\n")
        yield {
            "type": "error",
            "content": f"An error occurred: {str(e)}"
        }
        raise e
    finally:
        for msg in messages:
            if hasattr(msg, "model_dump"):
                formatted_messages.append(msg.model_dump())
            elif hasattr(msg, "dict"):
                formatted_messages.append(msg.dict())
            else:
                formatted_messages.append(msg)

        try:
            with open("debug_messages.json", "w") as f:
                json.dump(
                    formatted_messages,
                    f,
                    indent=4,
                    default=str
                )
            print("\n**MESSAGE HISTORY DUMPED**\n\n")
        except Exception as log_err:
            print(f"Failed to write debug log: {log_err}")

        yield {
            "type": "done",
            "response": final_response,
            "history": formatted_messages
        }


class ContextVarIterator:
    def __init__(self, generator, token):
        self.generator = generator
        self.token = token

    def __next__(self):
        from config import request_token
        token_token = request_token.set(self.token)
        try:
            return next(self.generator)
        finally:
            request_token.reset(token_token)

    def __iter__(self):
        return self


def run_agent_stream(message: str, history: list = None, token: str = None):
    generator = _run_agent_stream(message, history)
    return ContextVarIterator(generator, token)


def run_agent(message: str, history: list = None, token: str = None) -> dict:
    """
    Synchronous wrapper for run_agent_stream to keep compatibility with existing non-streaming consumers.
    """
    stream = run_agent_stream(message, history, token=token)
    result = None
    for event in stream:
        if event["type"] == "done":
            result = {
                "response": event["response"],
                "history": event["history"]
            }
    return result
