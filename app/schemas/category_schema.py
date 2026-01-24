from pydantic import BaseModel

class CreateCategory(BaseModel):
    name: str
    image_link: str
    
class ReadCategory(BaseModel):
    id: int
    name: str
    image_link: str