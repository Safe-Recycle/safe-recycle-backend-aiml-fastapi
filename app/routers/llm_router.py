from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Form
from typing import Annotated, List
from sqlmodel import Session, select

from dotenv import load_dotenv

from app.databases.session import get_session
from app.schemas.llm_schema import SingleLLMResponse
from app.services.authentication_service import get_current_active_user
from app.services.llm_service import process_llm_request, llm_check_request
from app.models.user_model import User
from app.core.config import settings


router = APIRouter(prefix="/llm", tags=["LLM"])


@router.post("/process", response_model=SingleLLMResponse)
async def llm_process_request(
    file: Annotated[UploadFile, File(...)],
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    try:
        process_result = await process_llm_request(
            upload_file=file,
            session=session,
        )
        
        return {
            "status": "success",
            "message": "LLM request processed successfully",
            "data": process_result
        }

    except Exception as e:
        if str(e) == "ERROR DATABASE":
            raise HTTPException(
                status_code=500,
                detail="Database error occurred while processing the request"
            )
        
        else:
            raise HTTPException(
                status_code=422,
                detail=f"Validation Error: {str(e)}"
            )

@router.post("/check", response_model=SingleLLMResponse)
async def llm_check(
    file: Annotated[UploadFile, File(...)],
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    try:
        check_result = await llm_check_request(
            upload_file=file,
            session=session,
        )
        
        return {
            "status": "success",
            "message": "LLM request processed successfully",
            "data": check_result
        }

    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Validation Error: {str(e)}"
        )
