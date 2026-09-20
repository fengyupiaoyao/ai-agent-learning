from pydantic import BaseModel


class UserInfo(BaseModel):
    name: str
    age: int
    accupation: str


user_info = UserInfo(name="John", age=30, accupation="Engineer")

print(user_info)
print(user_info.name)
print(user_info.age)
