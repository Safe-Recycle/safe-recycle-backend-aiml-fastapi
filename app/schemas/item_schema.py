from typing import List
from pydantic import BaseModel
from datetime import datetime, timezone

from app.schemas.category_schema import ReadCategory
from app.schemas.pagination_schema import PaginationMeta
from app.schemas.base_response_schema import BaseResponse

class CreateItem(BaseModel):
    name: str
    description: str
    image_link: str
    recycle: str
    
    is_reusable: bool
    is_recyclable: bool
    is_hazardous: bool
    
    category_name: str

class ReadItem(BaseModel):
    id: int
    name: str
    description: str
    image_link: str
    recycle: str
    
    is_reusable: bool
    is_recyclable: bool
    is_hazardous: bool
    
    category: ReadCategory
    
    model_config = {
        "from_attributes": True
    }
    
class SingleItemResponse(BaseResponse):
    data: ReadItem
    
class ShowItem(BaseModel):
    id: int
    name: str
    image_link: str

class ItemListResponse(BaseModel):
    status: str
    data: List[ShowItem]
    meta: PaginationMeta
    
class UpdateItem(BaseModel):
    name: str | None
    description: str | None
    image_link: str | None
    recycle: str | None
    
    is_reusable: bool | None
    is_recyclable: bool | None
    is_hazardous: bool | None
    
    category_name: str | None
    
    updated_at: datetime = datetime.now(timezone.utc)