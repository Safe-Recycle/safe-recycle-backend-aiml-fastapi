from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone

from app.schemas.base_response_schema import BaseResponse

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    
class SingleUserResponse(BaseResponse):
    data: UserRead
    
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    
class UserUpdate(BaseModel):
    name: str | None
    email: str | None
    password: str | None