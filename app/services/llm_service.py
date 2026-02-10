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
#--------------------- LLM REQUEST FUNCTION ----------------------#
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
                {"name": "plastic bottle", "description": "A clear plastic water bottle", "recycle": "Rinse and place in plastic bin.", "is_reusable": true, "is_recyclable": true, "is_hazardous": false, "category_id": 2}
                
                No markdown, no extra text.
                """
            ]
        )

        return response.text

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
        return llm_check_result
    
        # llm_check_data = extract_json_check(llm_check_result)

        # if not llm_check_data or 'name' not in llm_check_data:
        #     print("Failed to extract valid JSON from LLM response: {llm_check_result}")
        #     return None
        
        # detected_item_name = llm_check_data['name'].strip().lower()
        # print(f"Detected item name: {detected_item_name}")

        # check_statement = select(Item).where(Item.name == detected_item_name)
        # existing_item = session.exec(check_statement).first()

        # if existing_item:
        #     print("Cache HIT! Returning data from DB")
        #     return {
        #         "item_name": existing_item.name,
        #         "description": existing_item.description,
        #         "recycle": existing_item.recycle
        #     }
        # else:
        #     print("Cache MISS! No matching item found in DB")
        #     return {
        #         "item_name": detected_item_name,
        #         "description": None,
        #         "recycle": None
        #     }

    except Exception as e:
        print(f"Error processing uploaded file: {str(e)}")
        raise e
    

#---------------------------------------------------------------#
#----------------- EXTRACT JSON CHECK FUNCTION -----------------#
#---------------------------------------------------------------#
async def extract_json_check(text: str):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_str = match.group()
            return json.loads(json_str)
        else:
            return None
    
    except json.JSONDecodeError:
        return None
