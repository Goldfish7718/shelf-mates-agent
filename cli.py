import sys
from agent import run_agent

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

            result = run_agent(prompt, history)
            history = result["history"]

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nCLI Error: {e}\n")

if __name__ == "__main__":
    main()
