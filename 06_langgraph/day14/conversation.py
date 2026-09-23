messages = []


def add_user_message(message):
    messages.append({"role": "user", "content": message})


def add_assistant_message(message):
    messages.append({"role": "assistant", "content": message})


add_user_message("我叫小明")
add_assistant_message("你好 小明")

add_user_message("今天天气怎么样")

for message in messages:
    print(
        f"{message['role']}: {message['content']}"
    )
