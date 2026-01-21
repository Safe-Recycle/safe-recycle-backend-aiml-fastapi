from typing import Annotated
from sqlmodel import Field
from base_model import BaseModel

class User(BaseModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    password: str