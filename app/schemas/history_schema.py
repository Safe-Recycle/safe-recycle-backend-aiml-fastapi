from pydantic import BaseModel, ConfigDict
from typing import List

from app.schemas.base_response_schema import BaseResponse
from app.schemas.category_schema import CategoryName

class CreateHistory(BaseModel):
    user_id: int
    item_id: int

class Recommendations(BaseModel):
    item_id: int
    item_name: str
    item_category: str
    item_image_link: str    
    
class ResponseRecommendations(BaseResponse):
    data: List[Recommendations]
    
class PopularItem(BaseModel):
    id: int
    name: str
    image_link: str
    category_id: int
    category: CategoryName

    model_config = ConfigDict(from_attributes=True)

class ResponsePopularItem(BaseResponse):
    data: List[PopularItem]
