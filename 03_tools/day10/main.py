from agent import run_agent


def main():
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = run_agent(user_input)

        print(f"Agent: {response}")


if __name__ == "__main__":
    main()
