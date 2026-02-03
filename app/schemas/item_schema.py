from pydantic import BaseModel
from datetime import datetime

class CreateItem(BaseModel):
    name: str
    description: str
    image_link: str
    recycle: str
    
    is_reusable: bool
    is_recyclable: bool
    is_hazardous: bool
    
class ReadItem(BaseModel):
    id: int
    name: str
    description: str
    image_link: str
    recycle: str
    
    is_reusable: bool
    is_recyclable: bool
    is_hazardous: bool
    
class UpdateItem(BaseModel):
    name: str
    description: str
    image_link: str
    recycle: str
    
    is_reusable: bool
    is_recyclable: bool
    is_hazardous: bool
    
    updated_at: datetime