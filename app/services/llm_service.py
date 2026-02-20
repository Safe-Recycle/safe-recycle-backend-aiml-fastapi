import json
import os
from uuid import uuid4

from fastapi import UploadFile
from google import genai
from google.genai import types
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.models.item_model import Item
from app.models.category_model import Category
from app.routers.item_router import BASE_STORAGE

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
            model=settings.GEMINI_MODEL_NAME_PROCESS,
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
                

                If the item was not a trash item or could not be identified, return name as "Wasted Not Identified".

                Example for identified trash item: 
                {"name": "plastic bottle", "description": "A clear plastic water bottle", "recycle": "**First choice** Before throwing it, see if it can be reused as DIY thing. Easy reuse ideas: - Refill for water\n - Use as a plant watering can\n - Cut and use as a funnel\n\n **How to recycle properly** Most plastic bottle are reusable, especially those marked with PET, PPE, or #1\n Steps:\n - Empty the bottle completely\n - Remove the cap and label\n - Rinse the bottle\n - Place it in the recycling bin", "is_reusable": true, "is_recyclable": true, "is_hazardous": false, "category_id": 2}

                Example for non-trash item:
                {"name": "Wasted Not Identified", "description": "Item could not be identified as trash", "recycle": "N/A", "is_reusable": false, "is_recyclable": false, "is_hazardous": false, "category_id": 12}
                
                No markdown, no extra text.
                """
            ]
        )

        llm_request_result = response.text

        llm_request_json_extract = json.loads(llm_request_result)
        extract_name = llm_request_json_extract.get("name", "Unknown item")
        extract_description = llm_request_json_extract.get("description", "Unknown description")
        extract_recycle = llm_request_json_extract.get("recycle", "Unknown recycle")
        extract_is_reusable = llm_request_json_extract.get("is_reusable", "Unknown status")
        extract_is_recyclable = llm_request_json_extract.get("is_recyclable", "Unknown status")
        extract_is_hazardous = llm_request_json_extract.get("is_hazardous", "Unknown status")
        raw_category_id = llm_request_json_extract.get("category_id", 12)
        extract_category_id = int(raw_category_id)

        if extract_name == "Wasted Not Identified":
            status = {
                "status": "failed",
                "message": "Item could not be identified as trash"
            }
            return status
        
        else:

            filename = f"{uuid4().hex}_{upload_file.filename}"
            filepath = os.path.join(BASE_STORAGE, filename)
            with open(filepath, "wb") as f:
                f.write(image_bytes)
                f.close()

            new_item = Item(
                name=extract_name,
                description=extract_description,
                image_link=str(filepath),
                recycle=extract_recycle,
                is_reusable=extract_is_reusable,
                is_recyclable=extract_is_recyclable,
                is_hazardous=extract_is_hazardous,
                category_id=extract_category_id
            )

            try:
                session.add(new_item)
                session.commit()
                session.refresh(new_item)

                data = {
                    "id": new_item.id,
                    "name": new_item.name,
                    "description": new_item.description,
                    "recycle": new_item.recycle,
                    "is_reusable": new_item.is_reusable,
                    "is_recyclable": new_item.is_recyclable,
                    "is_hazardous": new_item.is_hazardous,
                    "category_id": new_item.category_id
                }

                return data

            except SQLAlchemyError as e:
                session.rollback()
                ValueError(f"ERROR DATABASE: {str(e)}")

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
            model=settings.GEMINI_MODEL_NAME_CHECK,
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
        
        if selected_item := session.exec(
            select(Item).where(Item.name == json_extract_result)
        ).first():
            json_extract_result = {
                "id": selected_item.id,
                "name": selected_item.name,
                "description": selected_item.description,
                "recycle": selected_item.recycle,
                "is_reusable": selected_item.is_reusable,
                "is_recyclable": selected_item.is_recyclable,
                "is_hazardous": selected_item.is_hazardous,
                "category_id": selected_item.category_id
            }

            return json_extract_result
        
        else:
            json_extract_result = {
                "name": "Item not found in database"
            }

            return json_extract_result

    except Exception as e:
        print(f"Error processing uploaded file: {str(e)}")
        raise e
