from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_model import User
    from app.models.item_model import Item
    
class History(SQLModel, table=True):
    __tablename__ = "history"
    
    id: int | None = Field(default=None, primary_key=True) 
    
    user_id: int | None = Field(foreign_key="user.id", index=True)
    item_id: int | None = Field(foreign_key="item.id", index=True)
    
    viewed_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    user: "User" = Relationship(back_populates="history")
    item: "Item" = Relationship(back_populates="history")