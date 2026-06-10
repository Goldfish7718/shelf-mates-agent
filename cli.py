import sys

# Reconfigure stdout to use UTF-8 to prevent charmap encoding errors on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from agent import run_agent_stream

def main():
    history = None
    print("Welcome to Shelf-mates AI!")
    print("Type 'exit', 'quit', or 'bye' to leave.\n")

    while True:
        try:
            prompt = input("YOU: ")

            if prompt.strip() == "":
                continue

            if prompt.lower() in ["exit", "quit", "bye"]:
                print("Goodbye!")
                break

            # Start streaming the agent response
            stream = run_agent_stream(prompt, history)
            
            active_tools_printed = set()
            print("CHATBOT: ", end="", flush=True)

            for event in stream:
                if event["type"] == "content":
                    print(event["delta"], end="", flush=True)
                elif event["type"] == "tool_call":
                    idx = event["index"]
                    if idx not in active_tools_printed:
                        active_tools_printed.add(idx)
                        print(f"\n[TOOL CALL] {event['name']} args: ", end="", flush=True)
                    if event["arguments_delta"]:
                        print(event["arguments_delta"], end="", flush=True)
                elif event["type"] == "tool_execute_start":
                    print(f"\n[EXECUTING] {event['name']}...", flush=True)
                elif event["type"] == "tool_execute_end":
                    print(f"[RESULT] {event['result']}", flush=True)
                elif event["type"] == "error":
                    print(f"\nERROR: {event['content']}", flush=True)
                elif event["type"] == "done":
                    history = event["history"]
                    print()  # Final newline for clean spacing

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nCLI Error: {e}\n")

if __name__ == "__main__":
    main()
