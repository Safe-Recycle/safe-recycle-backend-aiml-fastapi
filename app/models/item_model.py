from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.category_model import Category
    
class Item(SQLModel, table=True):
    __tablename__ = "items"
    
    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    description: str 
    image_link: str
    recycle: str
    
    is_reusable: bool
    is_recyclable: bool
    is_hazardous: bool
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    
    category_id: int = Field(foreign_key="categories.id", index=True)
    category: "Category" = Relationship(back_populates="item")