from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Form
from typing import Annotated, List
from sqlmodel import Session, select

from dotenv import load_dotenv

from app.databases.session import get_session
from app.schemas.llm_schema import LLMRequest, LLMResponse
from app.services.llm_service import process_llm_request, llm_check_request
from app.core.config import settings


router = APIRouter(prefix="/llm", tags=["LLM"])


@router.post("/process", response_model=LLMResponse)
async def llm_process_request(
    file: Annotated[UploadFile, File(...)],
    session: Session = Depends(get_session)
):
    try:
        process_result = await process_llm_request(
            upload_file=file,
            session=session
        )
        
        return {
            "output_message": process_result
        }

    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Validation Error: {str(e)}"
        )
    
@router.post("/check", response_model=LLMResponse)
async def llm_check(
    file: Annotated[UploadFile, File(...)],
    session: Session = Depends(get_session)
):
    try:
        check_result = await llm_check_request(
            upload_file=file,
            session=session
        )
        
        return {
            "output_message": check_result
        }

    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Validation Error: {str(e)}"
        )
