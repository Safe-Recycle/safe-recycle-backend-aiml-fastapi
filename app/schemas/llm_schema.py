from pydantic import BaseModel

class LLMRequest(BaseModel):
    id: int
    model_name: str
    prompt: str
    output_message: str