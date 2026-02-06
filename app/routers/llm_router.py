from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlmodel import Session, select

from dotenv import load_dotenv

from app.databases.session import get_session
from app.schemas.llm_schema import LLMRequest
from app.services.llm_service import process_llm_request
from app.core.config import settings


GEMINI_API_KEY = settings.GEMINI_API_KEY
GEMINI_MODEL_NAME = settings.GEMINI_MODEL_NAME


router = APIRouter(prefix="/llm", tags=["LLM"])


@router.post("/process", response_model=LLMRequest)
async def llm_process_request(
    llm_request: LLMRequest,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        process_llm_request(llm_request)
        return llm_request
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"An error occured while processing the LLM request: {str(e)}"
        )
        