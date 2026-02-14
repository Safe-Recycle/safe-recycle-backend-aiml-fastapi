from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_model import User
    from app.models.item_model import Item
    
class History(SQLModel, table=True):
    __tablename__ = "histories"
    
    id: int | None = Field(default=None, primary_key=True) 
    
    user_id: int | None = Field(foreign_key="users.id", index=True)
    item_id: int | None = Field(foreign_key="items.id", index=True)
    
    viewed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: "User" = Relationship(back_populates="history")
    item: "Item" = Relationship(back_populates="history")