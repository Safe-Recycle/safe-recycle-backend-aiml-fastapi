from google import genai
from google.genai import types

import requests
from app.schemas.llm_schema import LLMRequest
from app.models.llm_model import LLMModel


def process_llm_request(llm_request: LLMRequest):
    
    image_path = "app/OIP.jpg"
    image_bytes = requests.get(image_path).content
    image = types.Part.from_bytes(
        data=image_bytes, mime_type="image/jpg/jpeg"
    )

    llm_request.model_name = "gemini-1.5-pro"
    llm_request.prompt = f"Generate a detailed description for an image of a recyclable item to help users identify it for proper recycling. The image shows: {image}"


    client = genai.Client()

    response = client.models.generate_content(

        model=llm_request.model_name,
        prompt=types.Prompt(
            text=llm_request.prompt,
            images=[image]
        )
    
    )

    llm_request.output_message = response.md
