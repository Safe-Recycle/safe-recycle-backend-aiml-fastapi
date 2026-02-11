import json
import os
import re
import tempfile
import shutil
import requests

from fastapi import UploadFile
from google import genai
from google.genai import types
from sqlmodel import Session, select

from app.core.config import settings
from app.models.item_model import Item
from app.models.category_model import Category

#---------------------------------------------------------------#
#-------------------- LLM REQUEST FUNCTION ---------------------#
#---------------------------------------------------------------#
async def process_llm_request(upload_file: UploadFile, session: Session) -> str:

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    temp_file_path = None

    try:
        
        image_bytes = await upload_file.read()
        mime_type = upload_file.content_type or "image/jpeg" or "image/jpg"


        response = client.models.generate_content(
            model=settings.GEMINI_MODEL_NAME,
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
                """
                Identify the item in this image. Response ONLY with a valid JSON object.
                
                Follow this category_id mapping: 
                [
                    {"id": 1, "name": "Organic"}, {"id": 2, "name": "Plastic"}, 
                    {"id": 3, "name": "Metal"}, {"id": 4, "name": "Glass"}, 
                    {"id": 5, "name": "Paper"}, {"id": 6, "name": "Textiles"}, 
                    {"id": 7, "name": "Hazardous"}, {"id": 8, "name": "E-Waste"}, 
                    {"id": 9, "name": "Batteries"}, {"id": 10, "name": "Styrofoam"}, 
                    {"id": 11, "name": "Mixed Waste"}, {"id": 12, "name": "Other"}
                ]

                Response output format: 
                {
                    "name": "item_name_singular", 
                    "description": "item_description", 
                    "recycle": "item_recycle_instructions", 
                    "is_reusable": true, 
                    "is_recyclable": true, 
                    "is_hazardous": false, 
                    "category_id": 12
                }

                Example: 
                {"name": "plastic bottle", "description": "A clear plastic water bottle", "recycle": "Rinse and place in plastic bin. Otherwise, you can reuse it by creating a DIY things, etc", "is_reusable": true, "is_recyclable": true, "is_hazardous": false, "category_id": 2}
                
                No markdown, no extra text.
                """
            ]
        )

        llm_request_result = response.text
        return llm_request_result

    except Exception as e:
        print(f"Error processing uploaded file: {str(e)}")
        raise e
    
    finally:
        if temp_file_path:
            os.unlink(temp_file_path)

#---------------------------------------------------------------#
#--------------------- LLM CHECK FUNCTION ----------------------#
#---------------------------------------------------------------#
async def llm_check_request(upload_file: UploadFile, session: Session) -> str:

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    temp_file = None

    try:

        image_bytes = await upload_file.read()
        mime_type = "image/jpeg" or "image/jpg"

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL_NAME,
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
                "Identify the item in this image. Response ONLY with a valid JSON object. "
                "Format: {'name': 'item_name_singular'}. "
                "Example: {'name': 'plastic bottle'}. No markdown, no extra text."
            ]
        )

        llm_check_result = response.text
        
        llm_check_json_extract = json.loads(llm_check_result)
        json_extract_result = llm_check_json_extract.get("name", "Unknown item")
        return json_extract_result

    except Exception as e:
        print(f"Error processing uploaded file: {str(e)}")
        raise e
