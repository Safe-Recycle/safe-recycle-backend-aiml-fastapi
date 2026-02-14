from fastapi import UploadFile
from pydantic import BaseModel

from app.schemas.base_response_schema import BaseResponse

class LLMRequest(BaseModel):
    id: int
    image_filename: str

class SingleLLMResponse(BaseResponse):
    data: dict