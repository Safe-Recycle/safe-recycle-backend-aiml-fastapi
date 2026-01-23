from pydantic import BaseModel, EmailStr

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str