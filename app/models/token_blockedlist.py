from sqlmodel import SQLModel, Field
from datetime import datetime

class TokenBlockedList(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jti: str 
    expired_at: datetime