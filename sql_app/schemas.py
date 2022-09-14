# This file contains the Pydantic models
from pydantic import BaseModel


class Race(BaseModel):
    id : int
    year : int
    round : int
    circuit_id : int
    name : str
    date : str
    time : str
    url : str

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
