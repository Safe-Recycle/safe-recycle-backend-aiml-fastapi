from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)