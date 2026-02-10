from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.item_model import Item

class Category(SQLModel, table=True):
    __tablename__ = "categories"
    
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    image_link: str
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    
    item: List["Item"] = Relationship(back_populates="category")
