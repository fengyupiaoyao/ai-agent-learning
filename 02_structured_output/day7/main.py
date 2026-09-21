from tutor import PythonTutor
from dotenv import load_dotenv

load_dotenv(".env")


def main():
    tutor = PythonTutor()

    question = input(
        "请输入你想学习的 Python 问题："
    )

    result = tutor.ask(question)

    print("\n========== 概念 ==========")
    print(result.explanation)

    print("\n========== 示例 ==========")
    print(result.example)

    print("\n========== 常见错误 ==========")

    for mistake in result.common_mistakes:
        print(f"- {mistake}")

    print("\n========== 练习 ==========")
    print(result.exercise)
    print("\n========== 解释 ==========")


if __name__ == "__main__":
    main()
