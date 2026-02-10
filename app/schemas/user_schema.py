from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone
from typing import List

from app.schemas.base_response_schema import BaseResponse
from app.schemas.pagination_schema import PaginationMeta

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
    name: str | None = None
    email: str | None = None
    old_password: str | None = None
    password: str | None = None
    password_confirm: str| None = None
    
class UserAll(BaseModel):
    id: int
    name: str
    email: str
    disabled: bool | None   
    
class SingleUserDeleteResponse(BaseResponse):
    data: UserAll
    
class UserListResponse(BaseResponse):
    status: str
    data: List[UserAll]
    meta: PaginationMeta