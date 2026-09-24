from agent import agent
from rich.pretty import pprint


def main():
    response = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "研究一下 Fine-tuning?"}
            ]
        }
    )

    research = response["structured_response"]

    pprint(research.topic)
    pprint(research.summary)

    for point in research.key_points:
        pprint(point)


if __name__ == "__main__":
    main()
