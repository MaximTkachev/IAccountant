from typing import List, Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    email: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class UserData(BaseUser):
    id: int

    class Config:
        orm_mode = True


class UserEdit(BaseModel):
    username: Optional[str]
    email: Optional[str]
    name: Optional[str]
    password: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
