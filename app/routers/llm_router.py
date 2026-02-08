from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Form
from typing import Annotated, List
from sqlmodel import Session, select

from dotenv import load_dotenv

from app.databases.session import get_session
from app.schemas.llm_schema import LLMRequest
from app.services.llm_service import process_llm_request
from app.core.config import settings


router = APIRouter(prefix="/llm", tags=["LLM"])


@router.post("/process", response_model=LLMRequest)
async def llm_process_request(

    model_name: Annotated[str, Form(...)],
    file: Annotated[UploadFile, File(...)],
    session: Session = Depends(get_session)
):
    try:
        result_model = await process_llm_request(
            model_name=model_name,
            prompt=prompt,
            upload_file=file,
            session=session
        )

        return result_model

    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Validation Error: {str(e)}"
        )
