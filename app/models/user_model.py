from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.refresh_token_model import RefreshToken

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    
    hashed_password: str
    disabled: bool | None = None
    
    refresh_token: List["RefreshToken"] = Relationship(back_populates="user")