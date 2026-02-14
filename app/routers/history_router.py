from sqlmodel import Session
from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.services.authentication_service import get_current_user
from app.services.history_service import get_recommendations
from app.schemas.history_schema import ResponseRecommendations
from app.models.user_model import User
from app.databases.session import get_session

router = APIRouter(prefix="/histories", tags=["history"])

@router.get("/recommendation/{id}")
def get_recommendation_endpoint(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session)
):
    if current_user.id != id:
        HTTPException(403, "You are not authenticated with this id")
    
    recommendations = get_recommendations(
        session=session,
        user_id=id
    )
    
    return ResponseRecommendations(
        status="success",
        message="Recommendations fetched successfully",
        data=recommendations
    )