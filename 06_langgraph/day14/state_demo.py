state = {
    "messages": [],
    "user_name": None
}


def add_message(state, role, content):
    state["messages"].append({"role": role, "content": content})


add_message(
    state,
    "user",
    "我叫 小明"
)

state["user_name"] = "小明"

add_message(
    state,
    "assistant",
    "你好，小明！"
)

print(state)
