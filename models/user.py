from typing import Optional
from pydantic import BaseModel


class UserPost(BaseModel):
    name: str
    email: str
    password: str

class User(BaseModel):
    id: Optional[str]
    name: str
    email: str
    password: str