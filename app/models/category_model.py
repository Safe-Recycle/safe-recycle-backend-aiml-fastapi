from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

class Category(SQLModel, table=True):
    __tablename__ = "categories"
    
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    image_link: str
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))