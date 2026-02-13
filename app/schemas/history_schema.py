from pydantic import BaseModel

class CreateHistory(BaseModel):
    user_id: int
    item_id: int