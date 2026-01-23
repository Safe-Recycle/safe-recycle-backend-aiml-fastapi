from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_model import User

class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"
    
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(foreign_key="users.id", index=True)
    
    token_hash: str = Field(index=True)
    expires_at: datetime
    revoked: bool = False
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: "User" = Relationship(back_populates="refresh_token")