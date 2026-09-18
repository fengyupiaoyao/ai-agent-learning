from pydantic import BaseModel


class UserInfo(BaseModel):
    name: str
    age: int
    accupation: str
